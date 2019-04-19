from nipype import config
cfg = dict(execution={'remove_unnecessary_outputs': False})
config.update_config(cfg)

import nipype.interfaces.fsl as fsl
import nipype.interfaces.afni as afni
import nipype.interfaces.ants as ants
import nipype.interfaces.spm as spm

from nipype.interfaces.utility import IdentityInterface, Function, Select, Merge
from os.path import join as opj
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.pipeline.engine import Workflow, Node, MapNode

import numpy as np
import os, re
import matplotlib.pyplot as plt
from nipype.interfaces.matlab import MatlabCommand
MatlabCommand.set_default_paths('/Users/amr/Downloads/spm12')
MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")

# import nipype.interfaces.matlab as mlab
# mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
# mlab.MatlabCommand.set_default_paths('/home/amr/Documents/MATLAB/toolbox/spm8')

#==========================================================================================================================================================
# In[2]:

experiment_dir = '/media/amr/Amr_4TB/Work/stimulation' 



frequency_list = ['10Hz', 
                  '20Hz', 
                  '40Hz']



zstat_list = ['zstat1', 
              'zstat2',
              'zstat3',
              'zstat4',
              'zstat5',
              'zstat6']

                
output_dir  = 'output_stimulation_proc_3rd_level_post_fitting'
working_dir = 'workingdir_stimulation_proc_3rd_level_post_fitting'


proc_3rd_level = Workflow (name = 'proc_3rd_level')
proc_3rd_level.base_dir = opj(experiment_dir, working_dir)


#==========================================================================================================================================================
# In[3]:
#to prevent nipype from iterating over the anat image with each func run-, you need seperate
#nodes to select the files
#and this will solve the problem I have for almost 6 months
#but notice that in the sessions, you have to iterate also over subject_id to get the {subject_id} var



# Infosource - a function free node to iterate over the list of subject names

infosource = Node(IdentityInterface(fields=['frequencies', 'zstats' ]),
                  name="infosource")
infosource.iterables = [('frequencies', frequency_list),
                        ('zstats', zstat_list)]


#==========================================================================================================================================================
# In[4]:

template_brain = '/media/amr/Amr_4TB/Work/October_Acquistion/Anat_Template_Enhanced.nii.gz' 
template_mask = '/media/amr/Amr_4TB/Work/October_Acquistion/Anat_Template_Enhanced_Mask.nii.gz'

templates = {


          'zstat'           :  '//media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/{frequencies}/flameo/{zstats}.nii.gz',

        }



selectfiles = Node(SelectFiles(templates,
                              base_directory=experiment_dir),
                              name="selectfiles")
#==========================================================================================================================================================
# In[5]:

datasink = Node(DataSink(), name = 'datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_frequencies_', ''),('_zstats_', '_')]

datasink.inputs.substitutions = substitutions

#==========================================================================================================================================================
#Smooth estimation
def smooth_est(zstat):
     import nipype.interfaces.fsl as fsl
     import os
     template_mask = '/media/amr/Amr_4TB/Work/October_Acquistion/Anat_Template_Enhanced_Mask.nii.gz'

     smooth_est = fsl.SmoothEstimate()
     
     smooth_est.inputs.mask_file = template_mask


     if zstat[-25:-21] == '10Hz':
          res4d = '/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/flameo/res4d.nii.gz'
          smooth_est.inputs.dof = 7
     elif zstat[-25:-21] == '20Hz':
          res4d = '/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/flameo/res4d.nii.gz'
          smooth_est.inputs.dof = 7
     elif zstat[-25:-21] == '40Hz':
          res4d = '/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/flameo/res4d.nii.gz'
          smooth_est.inputs.dof = 6

     print(res4d)


     smooth_est.inputs.residual_fit_file = res4d
     smooth_est_outputs = smooth_est.run()

     print(zstat[-25:-21])
     dlh = smooth_est_outputs.outputs.dlh
     volume = smooth_est_outputs.outputs.volume
     resels = smooth_est_outputs.outputs.resels


     return dlh, volume, resels

smooth_est = Node(name = 'smooth_est',
                  interface = Function(input_names = ['zstat'],
                  output_names = ['dlh', 'volume', 'resels'],
                  function = smooth_est))



#==========================================================================================================================================================
#cluster zstats1

def cluster_zstats(zstat, volume, dlh):

        import nipype.interfaces.fsl as fsl
        import os
        template_mask = '/media/amr/Amr_4TB/Work/October_Acquistion/Anat_Template_Enhanced_Mask.nii.gz'

        cope_no = zstat[-8] #number of the zstat file after taking into account .nii.gz


        if zstat[-25:-21] == '10Hz':
            cope = '/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/flameo/cope{0}.nii.gz'.format(cope_no)
        elif zstat[-25:-21] == '20Hz':
            cope = '/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/flameo/cope{0}.nii.gz'.format(cope_no)
        elif zstat[-25:-21] == '40Hz':
            cope = '/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/flameo/cope{0}.nii.gz'.format(cope_no)


        #mask here not in a seperate node, because I need the original zstat to get the number    
        mask_zstat = fsl.ApplyMask()
        mask_zstat.inputs.in_file = zstat
        mask_zstat.inputs.mask_file = template_mask
        mask_zstat_outputs = mask_zstat.run()
        masked_zstat = mask_zstat_outputs.outputs.out_file



        cluster_zstats = fsl.model.Cluster()

        cluster_zstats.inputs.in_file = masked_zstat
        cluster_zstats.inputs.cope_file = cope
        cluster_zstats.inputs.threshold = 3.1
        cluster_zstats.inputs.pthreshold = 0.05
        cluster_zstats.inputs.connectivity = 26
        cluster_zstats.inputs.volume = volume
        cluster_zstats.inputs.dlh = dlh

        cluster_zstats.inputs.out_threshold_file = 'thresh_zstat.nii.gz'
        cluster_zstats.inputs.out_index_file = 'cluster_mask_zstat'
        cluster_zstats.inputs.out_localmax_txt_file = 'lmax_zstat_std.txt'
        cluster_zstats.inputs.use_mm = True
        cluster_zstats.cmdline


        cluster_zstats_outputs = cluster_zstats.run()

        threshold_file = cluster_zstats_outputs.outputs.threshold_file

        return threshold_file

cluster_zstats = Node(name = 'cluster_zstats',
                  interface = Function(input_names = ['zstat', 'volume', 'dlh'],
                  output_names = ['threshold_file'],
                  function = cluster_zstats))


#=========================================================================================================================================================
#threshold the maps to 3.1 to make it ready for submission
apply_thresh = Node(fsl.Threshold(), name='apply_threshold_3_1')
apply_thresh.inputs.thresh = 3.1
apply_thresh.inputs.out_file = 'threshold_file.nii.gz'

#==========================================================================================================================================================
#overlay thresh_zstat1

overlay_zstat = Node(fsl.Overlay(), name='overlay')
overlay_zstat.inputs.auto_thresh_bg = True
overlay_zstat.inputs.stat_thresh = (3.1,10)
overlay_zstat.inputs.transparency = True
overlay_zstat.inputs.out_file = 'rendered_thresh_zstat.nii.gz'
overlay_zstat.inputs.show_negative_stats = True
overlay_zstat.inputs.background_image = template_brain

#==========================================================================================================================================================
#generate pics thresh_zstat1

slicer_zstat = Node(fsl.Slicer(), name='slicer')
slicer_zstat.inputs.sample_axial = 2
slicer_zstat.inputs.image_width = 2000
slicer_zstat.inputs.out_file = 'rendered_thresh_zstat.png'











proc_3rd_level.connect([


              (infosource, selectfiles, [('frequencies','frequencies'),
                                         ('zstats','zstats')]),



              (selectfiles, smooth_est, [('zstat','zstat')]),



              (selectfiles, cluster_zstats, [('zstat','zstat')]), #I need the original file to get the number and then i mask it inside the function
              (smooth_est, cluster_zstats, [('volume','volume'),
                                            ('dlh','dlh')]),

 

              (cluster_zstats, apply_thresh, [('threshold_file','in_file')]),


              (cluster_zstats, overlay_zstat, [('threshold_file','stat_image')]),

              (overlay_zstat, slicer_zstat, [('out_file','in_file')]),

              (cluster_zstats, datasink, [('threshold_file','unthreshold_file')]),
              (apply_thresh, datasink, [('out_file','threshold_file')]),
              (slicer_zstat, datasink, [('out_file','activation_pic')])


              ])

proc_3rd_level.write_graph(graph2use='colored', format='png', simple_form=True)

proc_3rd_level.run('MultiProc', plugin_args={'n_procs': 8})





