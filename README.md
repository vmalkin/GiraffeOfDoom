# GiraffeOfDoom
Vaughn's public repository

Mostly python, and mostly about my home magnetometer/sky-camera project (http://RuruObservatory.org.nz). This is a spinoff and testbed for our work at http://DunedinAurora.NZ.

This repo is a bit of a mess - the significant folders are:

### pyDataReader
The datalogger that is used at Ruru Observatory and Dunedin Aurora. This software gets serial coms data from the magnetometer, stores it to a 24hr logfile and creates a number of CSV files for display purposes. 

### Coronal Hole Suite
This project correlates coronal hole coverage to solar wind speed. It corrects for transit time and uses a linear regression to provide a forecast of solar wind speeds. This can be used to forecast conditions likely to cause an auroral display. This is implemented from a paper published by the University of Gratz. 

### DataFusionProject
Simple project to combine logfile data from different magnetometers according to a common timestamp. Was going to form the basis for "actual" sensor/data fusion to try and increase accuracy of readings across a network of magnetometers

### TrendGetter
This project is designed to aggregate 24hr magnetogram logfiles and incorporate auroral sightings. It processes the magnetograms to calculate dH/dt and derive a storm threshold value. If it works, there should be a corelation between the storm threshold and aurora sightings. Over the long term, we should see carrington rotations and maybe equinoctual clumping of sightings. The current code is horrid and relies on brute-forcing *ICK* better version in the pipeline.

### Camera
Python scripts to work with SharpCap image capture software. Used to control an ZWO imaging camera running as DunedinAurora.NZ all-sky camera. Incl code that uses sine/cosine functions to aproximate an algorthm that calculates sunrise/sunset/twilight

### What is my IP
Python script to use an external site to determine my IP from the outside world. Logs as a text file. 