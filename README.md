# Cyt

automatic image analysis for immunofluorescence quantification

Scientists use to analyses microscopic images in ImageJ. Some of them use ImageJ macros to save time. 
however, there are few who can write scripts in java to fully automate the process. In contrast, python is a  widespread language  in scientific community. My main goal was to automate immunofluorescence-inmunohistochemistry protein expression quantification in python. The program calculates three expression measurements: 
integrated intensity, area percent and mean gray value. 
To speed up, it uses parallel computation (300 images in ~2 minutes, using 4 cores). 
I have tested the program, analyzing my own images from calcium-binding adapter molecule 1 (IBA-1) inmunostaining (microglia marker) 
and tyrosine hydroxylase (TH) inmunostaining (dopaminergic neuron marker). 

I used this code in my honors thesis. As soon as I defend and publish it, I will put the way to cite the program. Meanwile, you should cite ImageJ because the program use it in the analysis. If you have any doubt or improvement, just send me an email (marco.pena@unmsm.edu.pe). 



