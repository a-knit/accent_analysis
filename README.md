# Accent Inspector

Accent Inspector is your solution to automated accent detection. Accent Inspector can determine whether an individual is a native English speaker based on their speech. All  you need is a recording of the person in question reading the following phrase:

"Please call Stella, ask her to bring these things with her from the store."

Accent Inspector classifies the person as either a native or a non-native English speaker using formant analysis and a Support Vector Machine. Applications for this include identifying customer types and providing targeted customer service and marketing.

## Understanding the Model

The objective of this project was to answer the following question:

Can an algorithm detect the accent of a speaker?

The human ear easily notices when an unfamiliar accent is present. Accent Detector attempts to use the same differences in sound that the human ear focuses on and deliver an accurate label for whether a given speaker has an accent.

### The Data

A database of over 1500 audio files from [The Speech Accent Archive](http://accent.gmu.edu/) was used to train the model. These files contain recordings of speakers with 39 different native languages, and all of them are reading the same transcript. This gives the dataset the consistency needed to conservatively test the hypothesis.

The model relies on analysis of formant data to make predictions. Formants are frequencies in soundwaves from speech that are amplified due to the size and shapes of certain cavaties in the speakers vocal tract. The first formant comes from the back of the throat, the second from the front of the mouth, and so on. A free linguistics software named [Praat](http://www.fon.hum.uva.nl/praat/) was used to extract the formant data.

![](images/waveform_spectrogram.png)
Above is a waveform and spectrogram from Praat

### The Model

Accent detector uses a Support Vector Machine to make predictions based on formant data. The analysis uses first 4 formants of the first 12 words from each audio file. These allow the model to classify the speaker as either a native English speaker, or a non-native English, non-Indo-European speaker. Several tests sets have been run through the model and the accuracy is consitently above 85%, while the F1 score for the native English speaking class is almost 90%.

### Insights

These are reasonably auspicious results, considering the subtleties in the formant differences across accents and the amount of data used. The model did not perform well on more difficult problems, but these are likely solvable with further data and research.

The model did not perform well when other Indo-European languages were included in the training and test sets. This is because these languages are too similar to English and much harder to distinguish. This would be solved with much more data, especially from the other languages.

The model did not classify between more specific accent groups with high accuracy. Again, the amount of data is the prevailing issue. Four language families were used and the model was only able to select with about 50% accuracy. Most of the observations were in the European family, the maximum observations in any one of the other groups was below 200. This just was not enough to accurately make decisions with the SVM. The model performed much better when the non-European families were grouped together.

The model also required that each subject read the same transcript as the speakers in the database. This would be resolved with more accurate labeling of the words from each speaker as well as more data. Each audio file was divided into words (or more specifically, the vowel sounds for each word), using pulse analysis from Praat. This worked fairly well, but would sometimes pick up sounds that were not words as well as lump two words together. This is evidenced by the fact that the model performed best using only the first 12 words when there were actually 69 words in the transcript. The 13th word in each recording was too varied to be useful. This could be solved with a labeling algorithm that more accurately identifies each word.

Despite the above setbacks, the results from classifying native English against all non-European speakers proves the feasibility of solving more difficult problems.

## Using the Model

This repo contains the code for recreating the inspector. The data folder contains .txt files precompiled for training the model. To use the data files and run the model, follow the Quickstart Setup instructions. To scrape and format the data yourself, follow the Full Setup instructions (this will require downloading a third-party software). All scripts are located in the code folder.

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

This setup utilizes the data files available in the data folder. If you prefer to run through the entire experiment, including scraping and extracting the data, please refer to the Full Setup. This will require you to install Praat, a free software.

**Step 1:** Run mongo_setup.py

This will prepare the mongoDB database using the formant and pulse files in the data folder. The database saves all available information on the speakers and saves a list of all words with additional information on each word. Many of this information is not used in the final model but could be useful for additional research.

**Step 2:** Run basic_models.py

This will build and test the model. The model outputs accuracy and F1 scores.

### Full Setup

**Step 1:** Run scrape_data.py

This will scrape the mp3 files for analysis. We will save native language, birth country, and gender as well for use in further analysis. The data source is [The Speech Accent Archive](http://accent.gmu.edu/), a free accent database.

**Step 2:** Download Praat

Praat is a free linguistic software and is necessary for Accent Inspector to extract the data required to make predictions. We will be using the formant and pulse data that Praat derives from our audio files. Go to the [Praat homepage](http://www.fon.hum.uva.nl/praat/) to download.

**Step 3:** Run get_formants_pulses.praat

The file will need to be in the same folder as the audio files you have downloaded. It may be best to place a copy of the file in each directory where files are stored. You will also need to edit the input and output directories in the file, so that they match the desired input and output locations on your computer. Be sure that Praat is set as the default application for files of this type and open the file. You may need to click 'Run' in Praat, and Praat will begin scraping the formant and pulse data for the first 20 seconds of each audio file in .txt files.

**Step 4:** Run mongo_setup.py

This will prepare the mongoDB database using the formant and pulse files in the data folder. The database saves all available information on the speakers and saves a list of all words with additional information on each word. Many of this information is not used in the final model but could be useful for additional research.

**Step 5:** Run basic_models.py

This will build and test the model. The model outputs accuracy and F1 scores.