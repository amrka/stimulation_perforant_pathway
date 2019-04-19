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

                
# session_list = ['run001', 'run002', 'run003']



# frequency_list = ['10Hz', '20Hz', '40Hz']
                


output_dir  = 'Stimulation_2nd_level_OutputDir_10Hz'
working_dir = 'Stimulation_2nd_level_WorkingDir_10Hz'

stimulation_2nd_level = Workflow(name = 'stimulation_2nd_level_10Hz')
stimulation_2nd_level.base_dir = opj(experiment_dir, working_dir)


#==========================================================================================================================================================
# In[3]:
infosource = Node(IdentityInterface(fields=['subject_id']),
                  name="infosource")

infosource.iterables = [('subject_id', subject_list)]


#==========================================================================================================================================================
# In[4]:
# sub-001_task-MGT_run--02_bold.nii.gz, sub-001_task-MGT_run--02_sbref.nii.gz
#/preproc_img/run--04sub-119/smoothed_all_maths_filt_maths.nii.gz
#functional run-s


template_brain = '/media/amr/Amr_4TB/Work/October_Acquistion/Anat_Template_Enhanced.nii.gz' 
template_mask = '/media/amr/Amr_4TB/Work/October_Acquistion/Anat_Template_Enhanced_Mask.nii.gz'

TR = 2.0
no_runs = 3
#==========================================================================================================================================================

templates = {


'anat_brain'                :  '/media/amr/Amr_4TB/Work/stimulation/Data/{subject_id}/Anat_{subject_id}_bet.nii.gz',
'mask_brain'                :  '/media/amr/Amr_4TB/Work/stimulation/Data/{subject_id}/Anat_{subject_id}_Mask.nii.gz',
'anat_2_temp_trans'         :  '/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_OutputDir/anat_2_temp_transformations/subj_{subject_id}/transformComposite.h5',

#==========================================================================================================================================================

'func_2_anat_trans_10Hz_r1' :  """/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_WorkingDir/stimulation_preproc/_frequency_id_10Hz_session_id_run001_subject_id_{subject_id}/coreg/bold_2_anat_sub-{subject_id}0GenericAffine.mat""",
'func_2_anat_trans_10Hz_r2' :  """/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_WorkingDir/stimulation_preproc/_frequency_id_10Hz_session_id_run002_subject_id_{subject_id}/coreg/bold_2_anat_sub-{subject_id}0GenericAffine.mat""",
'func_2_anat_trans_10Hz_r3' :  """/media/amr/Amr_4TB/Work/stimulation/Stimulation_Preproc_WorkingDir/stimulation_preproc/_frequency_id_10Hz_session_id_run003_subject_id_{subject_id}/coreg/bold_2_anat_sub-{subject_id}0GenericAffine.mat""",

#==========================================================================================================================================================

'cope1_10Hz_r1'             : '/media/amr/Amr_4TB/Work/stimulation/Stimulation_1st_level_OutputDir/copes_1st_level/10Hz_run001_subj_{subject_id}/cope1.nii.gz',
'cope1_10Hz_r2'             : '/media/amr/Amr_4TB/Work/stimulation/Stimulation_1st_level_OutputDir/copes_1st_level/10Hz_run002_subj_{subject_id}/cope1.nii.gz',
'cope1_10Hz_r3'             : '/media/amr/Amr_4TB/Work/stimulation/Stimulation_1st_level_OutputDir/copes_1st_level/10Hz_run003_subj_{subject_id}/cope1.nii.gz',

#==========================================================================================================================================================

'varcope1_10Hz_r1'          : '/media/amr/Amr_4TB/Work/stimulation/Stimulation_1st_level_OutputDir/varcopes_1st_level/10Hz_run001_subj_{subject_id}/varcope1.nii.gz',
'varcope1_10Hz_r2'          : '/media/amr/Amr_4TB/Work/stimulation/Stimulation_1st_level_OutputDir/varcopes_1st_level/10Hz_run002_subj_{subject_id}/varcope1.nii.gz',
'varcope1_10Hz_r3'          : '/media/amr/Amr_4TB/Work/stimulation/Stimulation_1st_level_OutputDir/varcopes_1st_level/10Hz_run003_subj_{subject_id}/varcope1.nii.gz',

#==========================================================================================================================================================
}



selectfiles = Node(SelectFiles(templates,
                              base_directory=experiment_dir),
                              name="selectfiles")
#==========================================================================================================================================================
# In[5]:

datasink = Node(DataSink(), name = 'datasink')
datasink.inputs.container = output_dir
datasink.inputs.base_directory = experiment_dir

substitutions = [('_subject_id_', '')]

datasink.inputs.substitutions = substitutions


#==========================================================================================================================================================
#Apply transformations to each cope

def copes1_2_anat_func(fixed, cope1_10Hz_r1, cope1_10Hz_r2, cope1_10Hz_r3, func_2_anat_trans_10Hz_r1, func_2_anat_trans_10Hz_r2, func_2_anat_trans_10Hz_r3, mask_brain):
        import os, re
        import nipype.interfaces.ants as ants
        import nipype.interfaces.fsl as fsl

        cwd = os.getcwd()


        copes1 = [cope1_10Hz_r1,cope1_10Hz_r2,cope1_10Hz_r3]
        trans  = [func_2_anat_trans_10Hz_r1, func_2_anat_trans_10Hz_r2, func_2_anat_trans_10Hz_r3]

        copes1_2_anat = []
        FEtdof_t1_2_anat = []
        for i in range(len(copes1)):
              moving = copes1[i]
              transform = trans[i]
              ants_apply = ants.ApplyTransforms()
              ants_apply.inputs.dimension = 3
              ants_apply.inputs.input_image = moving
              ants_apply.inputs.reference_image = fixed
              ants_apply.inputs.transforms = transform
              ants_apply.inputs.output_image = 'cope1_2_anat_10Hz_r{0}.nii.gz'.format(i+1)
              

              ants_apply.run()

              copes1_2_anat.append(os.path.abspath('cope1_2_anat_10Hz_r{0}.nii.gz'.format(i+1)))

              dof = fsl.ImageMaths()
              dof.inputs.in_file = 'cope1_2_anat_10Hz_r{0}.nii.gz'.format(i+1)
              dof.inputs.op_string = '-mul 0 -add 147 -mas'
              dof.inputs.in_file2 = mask_brain
              dof.inputs.out_file = 'FEtdof_t1_2_anat_10Hz_r{0}.nii.gz'.format(i+1)

              dof.run()
              
              FEtdof_t1_2_anat.append(os.path.abspath('FEtdof_t1_2_anat_10Hz_r{0}.nii.gz'.format(i+1)))


        merge = fsl.Merge()
        merge.inputs.dimension = 't'
        merge.inputs.in_files = copes1_2_anat
        merge.inputs.merged_file = 'copes1_2_anat_10Hz.nii.gz'
        merge.run() 

        merge.inputs.in_files = FEtdof_t1_2_anat
        merge.inputs.merged_file = 'dofs_t1_2_anat_10Hz.nii.gz'
        merge.run()

        copes1_2_anat = os.path.abspath('copes1_2_anat_10Hz.nii.gz')
        dofs_t1_2_anat = os.path.abspath('dofs_t1_2_anat_10Hz.nii.gz')
        
        return copes1_2_anat, dofs_t1_2_anat


copes1_2_anat_func = Node(name = 'copes1_2_anat_func',
                          interface = Function(input_names = 
                                              ['fixed', 
                                               'cope1_10Hz_r1', 
                                               'cope1_10Hz_r2', 
                                               'cope1_10Hz_r3', 
                                               'func_2_anat_trans_10Hz_r1', 
                                               'func_2_anat_trans_10Hz_r2', 
                                               'func_2_anat_trans_10Hz_r3',
                                               'mask_brain'],
                           output_names = ['copes1_2_anat', 'dofs_t1_2_anat'],
                           function = copes1_2_anat_func))


#==========================================================================================================================================================

def varcopes1_2_anat_func(fixed, varcope1_10Hz_r1, varcope1_10Hz_r2, varcope1_10Hz_r3, func_2_anat_trans_10Hz_r1, func_2_anat_trans_10Hz_r2, func_2_anat_trans_10Hz_r3):
        import os, re
        import nipype.interfaces.ants as ants
        import nipype.interfaces.fsl as fsl

        cwd = os.getcwd()


        varcopes1 = [varcope1_10Hz_r1,varcope1_10Hz_r2,varcope1_10Hz_r3]
        trans  = [func_2_anat_trans_10Hz_r1, func_2_anat_trans_10Hz_r2, func_2_anat_trans_10Hz_r3]

        varcopes1_2_anat = []

        for i in range(len(varcopes1)):
              moving = varcopes1[i]
              transform = trans[i]
              ants_apply = ants.ApplyTransforms()
              ants_apply.inputs.dimension = 3
              ants_apply.inputs.input_image = moving
              ants_apply.inputs.reference_image = fixed
              ants_apply.inputs.transforms = transform
              ants_apply.inputs.output_image = 'varcope1_2_anat_10Hz_r{0}.nii.gz'.format(i+1)
              
              ants_apply.run()

              varcopes1_2_anat.append(os.path.abspath('varcope1_2_anat_10Hz_r{0}.nii.gz'.format(i+1)))

        merge = fsl.Merge()
        merge.inputs.dimension = 't'
        merge.inputs.in_files = varcopes1_2_anat
        merge.inputs.merged_file = 'varcopes1_2_anat_10Hz.nii.gz'
        merge.run() 

        varcopes1_2_anat = os.path.abspath('varcopes1_2_anat_10Hz.nii.gz')
      


        return varcopes1_2_anat


varcopes1_2_anat_func = Node(name = 'varcopes1_2_anat_func',
                          interface = Function(input_names = 
                                              ['fixed', 
                                               'varcope1_10Hz_r1', 
                                               'varcope1_10Hz_r2', 
                                               'varcope1_10Hz_r3', 
                                               'func_2_anat_trans_10Hz_r1', 
                                               'func_2_anat_trans_10Hz_r2', 
                                               'func_2_anat_trans_10Hz_r3'],
                           output_names = ['varcopes1_2_anat'],
                           function = varcopes1_2_anat_func))

#==========================================================================================================================================================

#==========================================================================================================================================================
#Create desing
create_l2_design = Node(fsl.model.L2Model(), name='create_l2_design')
create_l2_design.inputs.num_copes = no_runs


#==========================================================================================================================================================
#perform higher level model fits
design = '/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/design_2nd_level_3_sessions.mat'
t_contrast = '/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/design_2nd_level_3_sessions.con'
f_contrast = '/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/design_2nd_level_3_sessions.fts'
grp_contrast = '/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/design_2nd_level_3_sessions.grp'


flameo_fit_copes1 = Node(fsl.model.FLAMEO(), name='flameo_fit_copes1')
flameo_fit_copes1.inputs.run_mode = 'fe'
flameo_fit_copes1.inputs.design_file = design
flameo_fit_copes1.inputs.t_con_file = t_contrast
flameo_fit_copes1.inputs.f_con_file = f_contrast
flameo_fit_copes1.inputs.cov_split_file = grp_contrast

#==========================================================================================================================================================
smooth_est_copes1 = Node(fsl.SmoothEstimate(), name = 'smooth_estimation_copes1')
smooth_est_copes1.inputs.dof = 2 #3 sessions - 2 

#==========================================================================================================================================================
#mask zstat1

mask_zstat1 = Node(fsl.ApplyMask(), name='mask_zstat1')
mask_zstat1.inputs.out_file = 'thresh_zstat1.nii.gz'


#==========================================================================================================================================================
#cluster copes1
cluster_copes1 = Node(fsl.model.Cluster(), name='cluster_copes1')

cluster_copes1.inputs.threshold = 2.3
cluster_copes1.inputs.pthreshold = 0.05
cluster_copes1.inputs.connectivity = 26

cluster_copes1.inputs.out_threshold_file = 'thresh_zstat1.nii.gz'
cluster_copes1.inputs.out_index_file = 'cluster_mask_zstat1'
cluster_copes1.inputs.out_localmax_txt_file = 'lmax_zstat1_std.txt'
cluster_copes1.inputs.use_mm = True

#==========================================================================================================================================================
#overlay thresh_zstat1

overlay_cope1 = Node(fsl.Overlay(), name='overlay_cope1')
overlay_cope1.inputs.auto_thresh_bg = True
overlay_cope1.inputs.stat_thresh = (2.300302,5)
overlay_cope1.inputs.transparency = True
overlay_cope1.inputs.out_file = 'rendered_thresh_zstat1.nii.gz'
overlay_cope1.inputs.show_negative_stats = True

#==========================================================================================================================================================
#generate pics thresh_zstat1

slicer_cope1 = Node(fsl.Slicer(), name='slicer_cope1')
slicer_cope1.inputs.sample_axial = 2
slicer_cope1.inputs.image_width = 750
slicer_cope1.inputs.out_file = 'rendered_thresh_zstat1.png'

#===========================================================================================================================================================
#trasnform copes from 2nd level to template space to be ready fro 3rd level

cope1_2ndlevel_2_template = Node(ants.ApplyTransforms(), name='cope1_2ndlevel_2_template')
cope1_2ndlevel_2_template.inputs.dimension = 3
cope1_2ndlevel_2_template.inputs.reference_image = template_brain
cope1_2ndlevel_2_template.inputs.output_image = 'cope1_2ndlevel_2_template_brain.nii.gz'



varcope1_2ndlevel_2_template = Node(ants.ApplyTransforms(), name='varcope1_2ndlevel_2_template')
varcope1_2ndlevel_2_template.inputs.dimension = 3
varcope1_2ndlevel_2_template.inputs.reference_image = template_brain
varcope1_2ndlevel_2_template.inputs.output_image = 'varcope1_2ndlevel_2_template_brain.nii.gz'


#==========================================================================================================================================================


stimulation_2nd_level.connect([


              (infosource, selectfiles, [('subject_id','subject_id')]),


              (selectfiles, copes1_2_anat_func,[('anat_brain','fixed'),
                                                ('cope1_10Hz_r1','cope1_10Hz_r1'),
                                                ('cope1_10Hz_r2','cope1_10Hz_r2'),
                                                ('cope1_10Hz_r3','cope1_10Hz_r3'),
                                                ('func_2_anat_trans_10Hz_r1','func_2_anat_trans_10Hz_r1'),
                                                ('func_2_anat_trans_10Hz_r2','func_2_anat_trans_10Hz_r2'),
                                                ('func_2_anat_trans_10Hz_r3','func_2_anat_trans_10Hz_r3'),
                                                ('mask_brain','mask_brain')]),

              (selectfiles, varcopes1_2_anat_func,[('anat_brain','fixed'),
                                                ('varcope1_10Hz_r1','varcope1_10Hz_r1'),
                                                ('varcope1_10Hz_r2','varcope1_10Hz_r2'),
                                                ('varcope1_10Hz_r3','varcope1_10Hz_r3'),
                                                ('func_2_anat_trans_10Hz_r1','func_2_anat_trans_10Hz_r1'),
                                                ('func_2_anat_trans_10Hz_r2','func_2_anat_trans_10Hz_r2'),
                                                ('func_2_anat_trans_10Hz_r3','func_2_anat_trans_10Hz_r3')]),




              # (create_l2_design,flameo_fit_copes1, [('design_mat','design_file'),
              #                                       ('design_con','t_con_file'),
              #                                       ('design_grp','cov_split_file')]),

              (copes1_2_anat_func, flameo_fit_copes1, [('copes1_2_anat','cope_file'),
                                                       ('dofs_t1_2_anat','dof_var_cope_file')]),

              (varcopes1_2_anat_func, flameo_fit_copes1, [('varcopes1_2_anat','var_cope_file')]),

              (selectfiles, flameo_fit_copes1, [('mask_brain','mask_file')]),

              (selectfiles, smooth_est_copes1, [('mask_brain','mask_file')]),
              (flameo_fit_copes1, smooth_est_copes1, [('res4d','residual_fit_file')]),

              (selectfiles, mask_zstat1, [('mask_brain','mask_file')]),
              (flameo_fit_copes1, mask_zstat1, [('zstats','in_file')]),


              (mask_zstat1, cluster_copes1, [('out_file','in_file')]),
              (smooth_est_copes1, cluster_copes1, [('volume','volume'),
                                                   ('dlh','dlh')]),

              (flameo_fit_copes1, cluster_copes1, [('copes','cope_file')]),

              (selectfiles, overlay_cope1, [('anat_brain','background_image')]),

              (cluster_copes1, overlay_cope1, [('threshold_file','stat_image')]),

              (overlay_cope1, slicer_cope1, [('out_file','in_file')]),

              (flameo_fit_copes1, cope1_2ndlevel_2_template, [('copes','input_image')]),
              (selectfiles, cope1_2ndlevel_2_template, [('anat_2_temp_trans','transforms')]),

              (flameo_fit_copes1, varcope1_2ndlevel_2_template, [('var_copes','input_image')]),
              (selectfiles, varcope1_2ndlevel_2_template, [('anat_2_temp_trans','transforms')]),




              # (flameo_fit_copes1, datasink, [('copes','copes1'),
              #                                ('var_copes', 'varcopes1')]),

              # (slicer_cope1, datasink, [('out_file','cope1_activation_pic')]),

              # (cope1_2ndlevel_2_template, datasink, [('output_image','cope1_2ndlevel_2_template')]),
              # (varcope1_2ndlevel_2_template, datasink, [('output_image','varcope1_2ndlevel_2_template')]),



              ])

stimulation_2nd_level.write_graph(graph2use='colored', format='png', simple_form=True)

stimulation_2nd_level.run('MultiProc', plugin_args={'n_procs': 8})

#need number for l2model

