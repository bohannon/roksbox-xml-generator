roksbox-xml-generator
=====================

Generates the XML required for Roksbox on a roku machine.  Roksbox allows you to stream local network files to your roku.  

Roksbox can be found at http://roksbox.com/home/

Currently this app only parses video files.

Currently, there are two versions of IMDbPY floating around, one on sourceforge and another here on github. Use the version on github if you want this to work. If you install the default using pip or easy_install it will not work. Also, the versions that get installed on most linux distros seem to be the SF version as well. Just use this one:

https://github.com/alberanid/imdbpy

How to use roksbox-xml-generator.

    Using a command prompt, navigate to the root of the directory containing the videos you want to be processed. (i.e. if you have a directory called Videos with subdirectories in it, navigate to Videos).
    Run python roksbox-xml-generator.py. This script will navigate through your subdirectories and create a separate .xml file for each video file. If an xml file already exists it will skip that movie. You can run this in a cron job and it will only process new movie files.

Limitations:

    The script uses the movie filename (minus the extension) as the search term when looking for matches. This means your movie filenames should be the movie title to get the best results.
    Even when you do this sometimes it still gets the wrong movie, since it uses the first match in the returned list. So if the movie is a remake, you may see the original version or vice-versa.
    It seems to have a hard time with TV episodes
    I have only tried this on linux, it should work on windows and mac, but I don't know for sure that it does.
    For some reason the 'plot' keyword always comes back blank from imdbpy.
