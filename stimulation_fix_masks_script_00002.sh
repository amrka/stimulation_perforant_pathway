#!/bin/bash
#This script to adjust the sform and qform matrix of the manually drawn masks for the stimulation data


cd /media/amr/Amr_4TB/Work/stimulation/Data


for folder in *;do
	cd $folder

	pwd

	fslorient -deleteorient    Anat_${folder}_Mask
	fslorient -setsformcode 1  Anat_${folder}_Mask
	

	#Remove the skull from anatomicla images ty multiplying with mask
	fslmaths Anat_${folder} -mas Anat_${folder}_Mask Anat_${folder}_bet

	fslorient -deleteorient    EPI_${folder}_Mask
	fslorient -setsformcode 1  EPI_${folder}_Mask

	cd ..
done

#After this you have to name the runs to 10, 20, 40 Hz manually	
#sample to the name of the files after this step and before adding the frequency
# Anat_003_bet.nii.gz
# Anat_003_Mask.nii.gz
# Anat_003.nii.gz
# EPI_003_Mask.nii.gz
# EPI_Average_003.nii.gz
# Stim_003_10.nii.gz
# Stim_003_11.nii.gz
# Stim_003_12.nii.gz
# Stim_003_13.nii.gz
# Stim_003_14.nii.gz
# Stim_003_15.nii.gz
# Stim_003_16.nii.gz
# Stim_003_17.nii.gz


#After renaming and adding the run number and frequency
# Anat_003_bet.nii.gz
# Anat_003_Mask.nii.gz
# Anat_003.nii.gz
# EPI_003_Mask.nii.gz
# EPI_Average_003.nii.gz
# Stim_003_10_10Hz_run001.nii.gz
# Stim_003_11_10Hz_run002.nii.gz
# Stim_003_12_10Hz_run003.nii.gz
# Stim_003_13_20Hz_run001.nii.gz
# Stim_003_14_20Hz_run002.nii.gz
# Stim_003_15_20Hz_run003.nii.gz
# Stim_003_16_40Hz_run001.nii.gz
# Stim_003_17_40Hz_run002.nii.gz
