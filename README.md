# Cyt

automatic image analysis for immunofluorescence quantification

Scientists often analyses microscopic images in ImageJ. Some of them use ImageJ macros to save time. 
however, there are few who can write scripts in java to fully automate the process. In contrast, python is a  common language  in scientific community. My main goal was to automate immunofluorescence-inmunohistochemistry protein expression quantification in python. The program calculates three expression measurements: 
integrated intensity, area percent and mean gray value. 
To speed up, it uses parallel computation (300 images in ~2 minutes, using 4 cores). 
I have tested the program, analyzing my own images from calcium-binding adapter molecule 1 (IBA-1) inmunostaining (microglia marker) 
and tyrosine hydroxylase (TH) inmunostaining (dopaminergic neuron marker). 

I used this code in my honors thesis. If you have any doubt or improvement, just send me an email (mapenag@emory.edu). 

Note: It runs in Python 3. 


