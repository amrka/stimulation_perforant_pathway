#!/bin/bash

#combine the copes from the 2nd level for 10,20 and 40 Hz



mkdir -p /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/{10Hz,20Hz,40Hz}

cd /media/amr/Amr_4TB/Work/stimulation/Data/


for folder in *;do

	imcp /media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_40Hz/stimulation_2nd_level_40Hz/_subject_id_${folder}/cope1_2ndlevel_2_template/cope1_2ndlevel_2_template_brain.nii.gz \
	/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/cope1_${folder}

	imcp /media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_40Hz/stimulation_2nd_level_40Hz/_subject_id_${folder}/varcope1_2ndlevel_2_template/varcope1_2ndlevel_2_template_brain.nii.gz \
	/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/varcope1_${folder}



	imcp /media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_20Hz/stimulation_2nd_level_20Hz/_subject_id_${folder}/cope1_2ndlevel_2_template/cope1_2ndlevel_2_template_brain.nii.gz \
	/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/cope1_${folder}

	imcp /media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_20Hz/stimulation_2nd_level_20Hz/_subject_id_${folder}/varcope1_2ndlevel_2_template/varcope1_2ndlevel_2_template_brain.nii.gz \
	/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/varcope1_${folder}



	imcp /media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_10Hz/stimulation_2nd_level_10Hz/_subject_id_${folder}/cope1_2ndlevel_2_template/cope1_2ndlevel_2_template_brain.nii.gz \
	/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/cope1_${folder}

	imcp /media/amr/Amr_4TB/Work/stimulation/Stimulation_2nd_level_WorkingDir_10Hz/stimulation_2nd_level_10Hz/_subject_id_${folder}/varcope1_2ndlevel_2_template/varcope1_2ndlevel_2_template_brain.nii.gz \
	/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/varcope1_${folder}



done

#======================================================================================================================

change file names to contain gp name


python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name.py \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz -10 -7


python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name.py \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz -10 -7


python3 /Users/amr/Dropbox/SCRIPTS/change_files_to_contain_gp_name.py \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz -10 -7



#======================================================================================================================
#merge copes and varcopes for each frequency seperately


fslmerge -t /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii.gz \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/*_cope1_*.nii.gz


fslchfiletype NIFTI /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii.gz

fslmerge -t /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/varcope1_10Hz.nii.gz \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/*_varcope1_*.nii.gz 


fslchfiletype NIFTI /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/varcope1_10Hz.nii.gz



#======================================================================================================================

fslmerge -t /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii.gz \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/*_cope1_*.nii.gz



fslchfiletype NIFTI /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii.gz

fslmerge -t /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/varcope1_20Hz.nii.gz \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/*_varcope1_*.nii.gz 


fslchfiletype NIFTI /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/varcope1_20Hz.nii.gz


#======================================================================================================================


fslmerge -t /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii.gz \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/*_cope1_*.nii.gz


fslchfiletype NIFTI /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii.gz

fslmerge -t /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/varcope1_40Hz.nii.gz \
/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/*_varcope1_*.nii.gz 



fslchfiletype NIFTI /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/varcope1_40Hz.nii.gz


#======================================================================================================================


# mkdir media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/palm 

# palm \
# -i /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii \
# -o /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz//palm/10Hz_ \
# -m /media/amr/Amr_4TB/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
# -d /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.mat \
# -t /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.con \
# -f /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.fts \
# -vg /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.grp \
# -n 5000 -T -C 3.1 -ise -corrcon -save1-p 



# mkdir media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/palm 

# palm \
# -i /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii \
# -o /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/palm/20Hz_ \
# -m /media/amr/Amr_4TB/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
# -d /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.mat \
# -t /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.con \
# -f /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.fts \
# -vg /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.grp \
# -n 5000 -T -C 3.1 -ise -corrcon -save1-p 


# mkdir media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/palm 

# palm \
# -i /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii \
# -o /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/palm/40Hz_ \
# -m /media/amr/Amr_4TB/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
# -d /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.mat \
# -t /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.con \
# -f /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.fts \
# -vg /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.grp \
# -n 5000 -T -C 3.1 -ise -corrcon -save1-p 



#======================================================================================================================



flameo \
--cope=/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii \
--vc=/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/varcope1_10Hz.nii \
--mask=/media/amr/Amr_4TB/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
--ld=/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/flameo/ \
--dm=/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.mat \
--cs=/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.grp \
--tc=/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.con \
--runmode=flame12






flameo \
--cope=/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii \
--vc=/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/varcope1_20Hz.nii \
--mask=/media/amr/Amr_4TB/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
--ld=/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/flameo/ \
--dm=/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.mat \
--cs=/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.grp \
--tc=/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.con \
--runmode=flame12




 

flameo \
--cope=/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii \
--vc=/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/varcope1_40Hz.nii \
--mask=/media/amr/Amr_4TB/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
--ld=/media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/flameo/ \
--dm=/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.mat \
--cs=/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.grp \
--tc=/media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.con \
--runmode=flame12




#================================================================================================================================

mkdir /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/randomise 

randomise \
-i /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/cope1_10Hz.nii \
-o /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/10Hz/randomise/10Hz_ \
-m /media/amr/Amr_4TB/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
-d /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.mat \
-t /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_10Hz.con \
-n 5000 -x -T --uncorrp


mkdir /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/randomise



randomise \
-i /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/cope1_20Hz.nii \
-o /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/20Hz/randomise/20Hz_ \
-m /media/amr/Amr_4TB/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
-d /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.mat \
-t /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_20Hz.con \
-n 5000 -x -T --uncorrp


mkdir /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/randomise



randomise \
-i /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/cope1_40Hz.nii \
-o /media/amr/Amr_4TB/Work/stimulation/stimulation_3rd_level/40Hz/randomise/40Hz_ \
-m /media/amr/Amr_4TB/Work/stimulation/Anat_Template_Enhanced_Mask.nii \
-d /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.mat \
-t /media/amr/Amr_4TB/Work/stimulation/1st_Level_Designs/3rd_level_design_40Hz.con \
-n 5000 -x -T --uncorrp












