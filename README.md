# GSRProcessingPipeline
Pipeline that processes raw iMotions Galvanic Skin Response data into statistics that indicate change in emotional arousal. 

What the pipeline does: 

Note - for all the following metrics, all GSR peak values are reported in the microsiemens unit. All timestamp values are reported in milli-seconds.

1) takes in input of a folder containing raw iMotions Galvanic Skin Response data files
2) processes each file, reporting the following statistics in a processed file: 
- number of GSR peaks in file 
- number of GSR peaks in every 5 second range for entire time series (excluding first and last four seconds; common practice to exclude data at beginning and end of file for biometric data analysis pipeline aimed towards aiding scientific studies) 
- Peak onset value and timestamp, peak offset value and timestamp, maximum peak value and timestamp, length of peak,  and amplitude of GSR peak. Reports these metrics for every GSR peak in file. Also detects whether all GSR peaks are 'stimulus' peaks or not (a 'stimulus' peak is a GSR peak that occurs 1-5 seconds after a stimulus in a study trial, indicating  emotional arousal as a result of the stimulus). If a GSR peak is a 'stimulus' peak, reports the following: 
- timestamp of stimulus
- type of stimulus
- physical response marker to stimulus
If a GSR peak is a 'stimulus' peak for multiple stimuli in a trial, then it reports this. Also reports the timestamp and type of the additional stimuli, as well as the participants physical response marker to these stimuli. 

------------------------------------------------------------------------------------------------------------------------

This pipeline further separates 'stimulus' peaks into two categories. The pipeline was designed around a study trial that had stimuli participants were suppose to respond to, and stimuli participants were not suppose to respond to. Out of all the 'stimuli' peaks, peaks that resulted from stimuli participants were trained to respond to are categorized as 'trained stimuli peaks', while peaks that resulted from stimuli participants were trained not to respond to are categorized as 'nontrained stimuli peaks'. For both of these categories, pipeline reports the following metrics: 

- number of total stimuli peaks 
- number of trained stimuli peaks
- number of nontrained stimuli peaks 
- average peak amplitude for trained stimuli peaks
- average peak amplitude for nontrained stimuli peaks 
- average peak length, in milliseconds, for trained stimuli peaks 
- average peak length, in milliseconds, for nontrained stimuli peaks 
- percentage of stimulus markers that participants were suppose to respond to, and responded 
- percentage of stimulus markers participants were not suppose to respond to, and did not respond to 

Finally, this pipeline has the capability of directly comparing the above metrics for trained and nontrained stimulus peaks between pre and post trials for a participant to see differences between GSR peaks that would indicate whether the hypothesis of the study is supported by GSR data. The metrics above are always reported in pairs; these metrics for a participant's pre and post file are always reported together. 

All the above metrics are reported in another processed file separate from the processed file for the metrics above the divider (------------). This processed file reads the processed file for the metrics above the divider, and calculates its metrics from the metrics in this file.

How to use the pipeline: 

Note - ensure you have python 3.7 or greater installed in your text editor/IDE with the following packages: os, math, and csv.

1) Download the .py file and open in appropriate text editor/IDE. Program was created in pyCharm and Jupyter Notebooks; running the script in either of these IDE's would allow for the least errors while setting up.
2) in the preprocessing function, edit the 'Folder' and 'NewFilePath' variables to the directory of the folder with the GSR files on your computer. 
3) ensure the GSR files are of type .txt; if they are of any other type, convert them to type .txt before using this script
4) in the compareoddball function, change 'Folder1' variable to the directory where processed GSR data is stored (should be same as the 'NewFilePath' variable in the preprocessing function), and change the 'Foldersave' variable to the Folder which will save the data produced with this function. 
5) Run the preprocessing function to process all the raw GSR data to the statistics denoted above the divider (-------); processed data for every file will be stored in a new file at the directory you specified through the 'NewFilePath' variable
6) Run the compareoddball function to generate statistics comparing the stimuli peaks between pre and post files for the same participant (statistics denoted below the divider); processed data for to compare pre and post files will be stored in a new file at the directory you specified through the 'Foldersave' variable
