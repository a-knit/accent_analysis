inputDir$ = "/Users/Alex/accent_sound_files/sino_tibetan/gan/"
outputDir$ = "/Users/Alex/Documents/gitrepos/accent_analysis/data/sino_tibetan/"

Create Strings as file list... list 'inputDir$'*.mp3
numberOfFiles = Get number of strings

for ifile to numberOfFiles
    
    select Strings list
    file$ = Get string... ifile
    Read from file... 'inputDir$''file$'
    fileName$ = file$ - ".mp3"
    
	Edit
	editor: "Sound " + fileName$
		Select: 0, 20
		Zoom to selection
		gender$ = left$ (fileName$, 1)
		if gender$ = "m"
			Formant settings: 5000, 5, 0.025, 30, 1
		else
			Formant settings: 5500, 5, 0.025, 30, 1
		endif

		formants$ = Formant listing
		pulses$ = Pulse listing
		path_f$ = outputDir$ + fileName$ + "_formant.txt"
		path_p$ = outputDir$ + fileName$ + "_pulse.txt"
		writeFileLine: path_f$, formants$
		writeFileLine: path_p$, pulses$

	endeditor

endfor

select all
Remove