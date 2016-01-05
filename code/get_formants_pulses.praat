inputDir$ = "/Users/Alex/accent_sound_files/mongolian/"
outputDir$ = "/Users/Alex/accent_sound_files/mongolian/output/"

Create Strings as file list... list 'inputDir$'*.mp3
numberOfFiles = Get number of strings

for ifile to numberOfFiles
    
    select Strings list
    file$ = Get string... ifile
    Read from file... 'inputDir$''file$'
    fileName$ = file$ - ".mp3"
    
	Edit
	editor: "Sound " + fileName$
		Select: 0, 15
		Zoom to selection
		gender$ = "f"
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