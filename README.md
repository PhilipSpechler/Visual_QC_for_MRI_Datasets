# Visual QC for MRI Datasets
This python script partially automates the visual QC process for MRI datasets by looping through a user
supplied list of subjects to be visually inspected. Quality control is a laborious yet crucial step to ensure MRI datasets are
acceptable for further analysis.

This script assumes some preprocessing of the whole-brain T1 weighted anatomical image (i.e., VBM).
And some preprocessing of whole-brain T2* fMRI images (i.e., functional preprocessing). 

All MRI visualizations are automated using AFNIs standard display. And all quality assessments are recorded through the terminal window.
A csv file is automatically appended and backed up after each subject.

After displaying an image, the user enters their quality control assessment into the terminal window. Binary 'yes' or 'no' scores denote
a passing or failing of quality control. Alternatively, the user may specify 'check' which denotes a second opinion is needed.
After each step, the user may input a comment specific to their score. At the end of a subject, the user may make overall comments
related to that subject's quality. If no image is found, a score of "MissingData" is automatically populated into the logfile.

Built in user friendly options like basic afni controls, subject counting, input error checking, and quit functions, all come 
standard!  
## Dependencies
The following must be installed prior to using this script--

<ul>
  <li><a href='https://afni.nimh.nih.gov'> AFNI</a> ---> installed in the default '~/abin' directory</li>
  <li>python2.x, and numpy</li>
</ul>

The user's working directory ('workdir') must contain the following files. Stock versions are supplied in this repo.
  
  1.) vis_QC_2.8.py --> the python QC script itself
  
  2.) hotsub.txt --> a one-line textfile of the subject ID being inspected. Start with the first subject in your allsubs.txt file. 
  This file is auto-updated (changes) during QC. 
  
  3.) allsubs.txt --> a newline delimited textfile containing all subject IDs to QC
  
  4.) logfile.csv --> the logfile where QC metrics are automatically updated and saved after each subject

## Mechanics
Essentially, this script is a wrapper around the 'afni -dset ' command, and python's "raw_input" command.

To begin, you must  
1.) Edit the allsubs.txt and hotsub.txt files to match the subject IDs of your dataset.  
2.) Edit the vis_QC_2.8.py paths to match your directory naming.  
<ul> <li>required: workdir (line 42), path2anat (line 51), path2fmri (line 54), path2backup (line58).</li></ul> 
    
**It is expected that a backup directory is provided.**
Ideally, the backup directory is a remote data server, google drive, etc. in case a lab rat eats your computer. 

The assumed directory structure is as followed:
>- path2anat -or- path2fmri  
>    - collection of subjects directories  
>        - whole-brain anatomical or functional images  

For example, studyXYZ with 3 subjects should be organized like this: 
>/StudyXYZ/Subject1/swau_preprocessed_image.nii  
>/StudyXYZ/Subject2/swau_preprocessed_image.nii  
>/StudyXYZ/Subject3/swau_preprocessed_image.nii  

To start your QC project, open up a terminal, cd to the working directory, then call up the script!  
>cd \<workingdirectory>  
>python vis_QC_2.8.py

**When running, it is recommended the user closes the AFNI window before reutrning to the terminal to input their assessment**
**Otherwise, you will have too many AFNI windows open and risk confusing which image is truly being inspected**

### Background
Developing this code was my first project on day 1 of my graduate student career and has gone through major overhaul since August 2014.
It was initially developed to be used for the larger [IMAGEN project]('www.imagen-europe.com').

Please [email me]('pspechle@uvm.edu') with any questions!
