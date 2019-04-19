# In[1]:

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

#============================================================================================================================
# In[2]:
experiment_dir = '/media/amr/Amr_4TB/Work/stimulation' 


subject_list = ['003', '005', '008', '011', 
                '130', '018', '019', '020', 
                '059', '060', '062', '063', 
                '066', '126', '127', '146']

                
session_list = ['run001', 'run002', 'run003']



frequency_list = ['10Hz', '20Hz', '40Hz']
                


output_dir  = 'Stimulation_1st_level_OutputDir'
working_dir = 'Stimulation_1st_level_WorkingDir'

stimulation_1st_level = Workflow(name = 'stimulation_1st_level')
stimulation_1st_level.base_dir = opj(experiment_dir, working_dir)


#============================================================================================================================
# In[3]:
infosource = Node(IdentityInterface(fields=['subject_id','session_id', 'frequency_id']),
                  name="infosource")

infosource.iterables = [('subject_id', subject_list),
                        ('session_id', session_list),
                        ('frequency_id', frequency_list)]


#============================================================================================================================
# In[4]:
# sub-001_task-MGT_run-02_bold.nii.gz, sub-001_task-MGT_run-02_sbref.nii.gz
#/media/amr/Amr_4TB/MGT_poldrack/output_MGT_poldrack_preproc_preproc/preproc_img/run-04sub-119/smoothed_all_maths_filt_maths.nii.gz
#functional runs
templates = {

      'preproc_img' : '/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_OutputDir/preproc_img/{frequency_id}_{session_id}_subj_{subject_id}/smoothed_all_maths_filt_maths.nii.gz',
      'bold_brain'  : '/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_OutputDir/bold_brain/{frequency_id}_{session_id}_subj_{subject_id}/Stim_{subject_id}_??_{frequency_id}_{session_id}_roi_masked.nii.gz',
      'bold_mask'   : '/media/amr/Amr_4TB/Work/stimulation/Data/{subject_id}/EPI_{subject_id}_Mask.nii.gz'
         }



selectfiles = Node(SelectFiles(templates,
                              base_directory=experiment_dir),
                              name="selectfiles")
#============================================================================================================================
# In[5]:
datasink = Node(DataSink(), name = 'datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_subject_id_', '_subj_'),('_session_id_', '_'), ('_frequency_id_', '')]

datasink.inputs.substitutions = substitutions

#============================================================================================================================





design = '/media/amr/Amr_4TB/Work/Stimulation/1st_Level_Designs/design.mat'
t_contrast = '/media/amr/Amr_4TB/Work/Stimulation/1st_Level_Designs/design.con'
f_contrast = '/media/amr/Amr_4TB/Work/Stimulation/1st_Level_Designs/design.fts'

film_gls = Node(fsl.FILMGLS(), name = 'Fit_Design_to_Timeseries')
film_gls.inputs.design_file = design
film_gls.inputs.tcon_file = t_contrast
film_gls.inputs.fcon_file = f_contrast
film_gls.inputs.threshold = 1000.0
film_gls.inputs.smooth_autocorr = True

#============================================================================================================================
#Estimate smootheness of the image
smooth_est = Node(fsl.SmoothEstimate(), name = 'smooth_estimation')
smooth_est.inputs.dof = 147 #453-5 volumes 

#============================================================================================================================
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#============================================================================================================================

mask_zstat = Node(fsl.ApplyMask(), name = 'mask_zstat')
mask_zstat.inputs.out_file = 'thresh_zstat.nii.gz'


#============================================================================================================================
clustering_t = Node(fsl.Cluster(), name = 'clustering_t_contrast')
clustering_t.inputs.threshold = 2.3
clustering_t.inputs.pthreshold = 0.05
clustering_t.inputs.out_threshold_file = 'thresh_zstat.nii.gz'
clustering_t.inputs.out_index_file = 'cluster_mask_zstat'
clustering_t.inputs.out_localmax_txt_file = 'lmax_zstat.txt'
clustering_t.inputs.connectivity = 26

#============================================================================================================================
# In[15]:
#overlay t contrast
overlay_t_contrast = Node(fsl.Overlay(), name = 'overlay_t_contrast')
overlay_t_contrast.inputs.auto_thresh_bg = True
overlay_t_contrast.inputs.stat_thresh = (2.300302,5)
overlay_t_contrast.inputs.transparency = True

#============================================================================================================================
# In[15]:
#slicer 
slicer_t_contrast = Node(fsl.Slicer(), name = 'generate_t_contrast_image')
slicer_t_contrast.inputs.all_axial = True
slicer_t_contrast.inputs.image_width = 500

#============================================================================================================================
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#============================================================================================================================


mask_zfstat = Node(fsl.ApplyMask(), name = 'mask_zfstat')
mask_zfstat.inputs.out_file = 'thresh_zfstat.nii.gz'


#============================================================================================================================
# In[15]:

#clusterin on the statistical output of f-contrast
clustering_f = Node(fsl.Cluster(), name = 'clustering_f_contrast')
clustering_f.inputs.threshold = 2.3
clustering_f.inputs.pthreshold = 0.05
clustering_f.inputs.out_threshold_file = 'thresh_zfstat.nii.gz'
clustering_f.inputs.out_index_file = 'cluster_mask_zfstat'
clustering_f.inputs.out_localmax_txt_file = 'lmax_zfstat.txt'
clustering_f.inputs.connectivity = 26


#============================================================================================================================
# In[15]:
#overlay f contrast
overlay_f_contrast = Node(fsl.Overlay(), name = 'overlay_f_contrast')
overlay_f_contrast.inputs.auto_thresh_bg = True
overlay_f_contrast.inputs.stat_thresh = (2.300302,5)
overlay_f_contrast.inputs.transparency = True


#============================================================================================================================
# In[15]:
#slicer 
slicer_f_contrast = Node(fsl.Slicer(), name = 'generate_f_contrast_image')
slicer_f_contrast.inputs.all_axial = True
slicer_f_contrast.inputs.image_width = 500








stimulation_1st_level.connect([


              (infosource, selectfiles, [('subject_id','subject_id'),
                                         ('session_id','session_id'),
                                         ('frequency_id', 'frequency_id')]),



              (selectfiles, film_gls, [('preproc_img','in_file')]),


              (selectfiles, smooth_est, [('bold_mask','mask_file')]),
              (film_gls, smooth_est, [('residual4d','residual_fit_file')]),


              (selectfiles, mask_zstat, [('bold_mask','mask_file')]),
              (film_gls, mask_zstat, [('zstats','in_file')]),


              (mask_zstat, clustering_t, [('out_file','in_file')]),
              (film_gls, clustering_t, [('copes','cope_file')]),
              (smooth_est, clustering_t, [('dlh','dlh'),
              					('volume','volume')]),

              (selectfiles, overlay_t_contrast, [('bold_brain','background_image')]),
              (clustering_t, overlay_t_contrast, [('threshold_file','stat_image')]),


              (overlay_t_contrast, slicer_t_contrast, [('out_file','in_file')]),
#===================================================================================================

              (selectfiles, mask_zfstat, [('bold_mask','mask_file')]),
              (film_gls, mask_zfstat, [('zfstats','in_file')]),

              (mask_zfstat, clustering_f, [('out_file','in_file')]),
              
              (smooth_est, clustering_f, [('dlh','dlh'),
              					('volume','volume')]),

              (selectfiles, overlay_f_contrast, [('bold_brain','background_image')]),
              (clustering_f, overlay_f_contrast, [('threshold_file','stat_image')]),

              (overlay_f_contrast, slicer_f_contrast, [('out_file','in_file')]),

#===================================================================================================

              (film_gls, datasink, [('copes','copes_1st_level'),
                                    ('varcopes','varcopes_1st_level')]),

              (slicer_t_contrast, datasink, [('out_file','t_contrast_image')]),

              (slicer_f_contrast, datasink, [('out_file','f_contrast_image')]),



              ])

stimulation_1st_level.write_graph(graph2use='colored', format='png', simple_form=True)

stimulation_1st_level.run('MultiProc', plugin_args={'n_procs': 8})


