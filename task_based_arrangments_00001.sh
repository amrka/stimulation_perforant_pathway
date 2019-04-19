#!/bin/bash
#The data was acquired using Bruker 7T MRI machine
#The default output of the machine is 2dseq
  
cd '/media/amr/Amr_4TB/Work/stimulation/+ve_stimulation'
mkdir '/media/amr/Amr_4TB/Work/stimulation/Data' 
for folder in *;do
	#convert 2dseq to analyze format using an old script written in perl
	pvconv.pl $folder -outdir $folder
	
	cd $folder

	mkdir /media/amr/Amr_4TB/Work/stimulation/Data/${folder}
	pwd
	

	for image in *.img;do
		fslchfiletype NIFTI_GZ $image
	done

	for image in *.nii.gz;do
		#You cannot swapdim without sform or qform


		dim1=`fslval ${image} dim1`
		dim4=`fslval ${image} dim4`
		echo $pixdim $dim4
		without_ext=`remove_ext $image`
		number=`echo ${without_ext} | cut  -d"_" -f2` 

		
		if    [[ "$dim1" -eq "200"  &&  "$dim4" -eq "1" ]]; then
			
			fslswapdim $image RL AP IS $image
			Augment.sh $image 10 2
			fslorient -deleteorient    $image
			fslorient -setsformcode 1  $image
			fslorient -setqformcode 1  $image



			imcp $image /media/amr/Amr_4TB/Work/stimulation/Data/${folder}/Anat_${folder}
		elif  [[ "$dim1" -eq "100"   &&  "$dim4" -eq "150" ]]; then
			
			fslswapdim $image RL AP IS $image
			Augment.sh $image 10 2
			fslorient -deleteorient    $image
			fslorient -setsformcode 1  $image
			fslorient -setqformcode 1  $image

			#Extract a ROI from each file and take the average to use for manual skull-stripping
			#The electrode makes everything difficult with the coregistration
			fslroi $image Example_${number} 75 1
			imcp $image /media/amr/Amr_4TB/Work/stimulation/Data/${folder}/Stim_${folder}_${number}
		fi
	done
	fslmerge -t EPI_Average_${folder} Example_*
	fslmaths EPI_Average_${folder} -Tmean EPI_Average_${folder} 
	imrm Example_* 
	imcp EPI_Average_${folder} /media/amr/Amr_4TB/Work/stimulation/Data/${folder}/ 

	cd ..
done


#Now, you have to draw a mask for anat and epi_average manually

















