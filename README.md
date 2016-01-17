# Accent Inspector

Accent Inspector is your solution to automated accent detection. Accent Inspector can determine whether an individual is a native English speaker based on their speech. This is useful for identifying customer types and providing targeted customer service and marketing.  Accent Inspector classifies speakers using formant analysis and a Support Vector Machine.

## Using the Model

This repo contains the code for recreating the inspector. The data folder contains .txt files precompiled for training the model. To use the data files and run the model, follow the Quickstart Setup instructions. To scrape and format the data yourself, follow the Full Setup instructions.

### Files Included

code  
*    scrape_data.py  
*    get_formants_pulses.praat  
*    mongo_setup.py  
*    basic_models.py  
*    pulse_analysis.py  
*    undersample.py  
*    uniformity.py  
*    cross_validate.py

data  
*    afroasiatic - formant and pulse files for accents in the Afroasiatic language family  
*    european - formant and pulse files for the European language family  
*    indo_iranian - formant and pulse files for the Indo-Iranian language family  
*    sino_tibetan - formant and pulse files for the Sino-Tibetan language family  

### Quickstart Setup

This setup utilizes the data files available in the data folder. If you prefer to run through the entire experiment, including scraping and extracting the data, please refer to the Full Setup. This will require you to install the free software, Praat.

Step 1: Run mongo_setup.py

This will prepare the mongoDB database using the formant and pulse files in the data folder. The mongo_setup script is in the code folder.

Step 2: Run basic_models.py

This will build and test the model.

### Full Setup