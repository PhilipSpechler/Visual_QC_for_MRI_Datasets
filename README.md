# Visual QC for MRI Datasets
This python script partially automates the visual QC process for MRI datasets.
Essentially, this script is a wrapper around the 'afni -dset ' command, and python's "raw_input" command.
All MRI visualizations are automated through the script, and all quality assessments are recorded through the terminal window.
A csv file is automatically populated and backed up after each subject.

Built in user friendly options like basic afni controls, subject counting, input error checking, and quit functions, all come standard!

## Dependencies
The following must be installed prior to using this script--

  1.) [AFNI]('https://afni.nimh.nih.gov') ---> installed in the default '~/abin' directory
  2.) python 2.x, and numpy

The user's working directory ('workdir') is must have the following files.

  1.) the python script itself
  2.) hotsub.txt --> a one-line textfile of the subject ID being inspected
  3.) allsubs.txt --> a newline delimited textfile containing all subject IDs to QC
  4.) logfile.csv --> the logfile where QC metrics are saved
  
### Background

This script will loop through a user supplied list of subjects to be visually inspected.
Visual QC is an important step to ensure MRI datasets are acceptable for further analysis.

This script assumes some preprocessing of the whole-brain T1 weighted anatomical image (i.e., VBM)
And some preprocessing of the whole-brain T2* fMRI images (i.e., functional preprocessing). 

#### More background
Developing this code was my first project on day 1 of my graduate student career and has gone through major overhaul since August 2014.
It was initially developed to be used for the larger [IMAGEN project]('www.imagen-europe.com').

Please [email me]('pspechle@uvm.edu') with any questions!


