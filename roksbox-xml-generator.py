import os, unicodedata
#Bruce 
try:

   from imdb import IMDb, IMDbError

except ImportError:
   print "Imdpy package not found, please install (http://imdpy.sourceforge.net)!"
   sys.exit(1)
   
#The file extensions that this script will consider movies.  It will ignore anything else
movie_file_extensions = {'.m4v', '.mp4', '.mkv'}

def SearchMovies(Name, MovDB):
   movies = MovDB.search_movie(Name)
   mov = None
   for movie in movies:
      #summary = movie.summary()
      title = unicodedata.normalize('NFKD', movie.get('title')).encode('ascii','ignore')
      print title
      #print summary
      if (str.lower(Name) in str.lower(title)):
         mov = movie
         #mov.update()
         print title + " match!"
         break
      else:
         print title

   return mov



def SearchTV(Name, MovDB):
   movies = MovDB.search_episode(Name)
   mov = None
   for movie in movies:
      title = unicodedata.normalize('NFKD', movie.get('title')).encode('ascii','ignore')
      #print title
      if (str.lower(Name) in str.lower(title)):
         mov = movie
         #mov.update()
	 break
      else:
         print title
	 
   if mov:
      return mov
   else:        
      print "Did not find a TV match either"
      return None 


def FindVideo(Name):
   MovDB = IMDb()
   
   mov = SearchMovies(Name, MovDB)
	
   if mov:
      MovDB.update(mov)
      #print mov.summary()
      return mov
    
   print "Did not find a movie match, searching TV"
   
   mov = SearchTV(Name, MovDB)
   if mov:
      MovDB.update(mov)
      return mov

   return None



def WriteDefaultMovieInfo(OutFile, filename, dirname, moviexmlfile):

   notwatched = ""
   if ("Not Watched Yet" in dirname):
      notwatched = "Not Watched Yet,"

   homemovie = ""
   if ("HomeMovies" in dirname):
      homemovie = "Home Movies,"
   

   moviexmlfile.write("      <movie>\n")
   moviexmlfile.write("         <origtitle>"+ filename + "</origtitle>\n")
   moviexmlfile.write("         <year> Unknown </year>\n")
   moviexmlfile.write("         <genre> " + notwatched + homemovie + "All, Unknown</genre>\n")
   moviexmlfile.write("         <mpaa>UR</mpaa>\n")
   moviexmlfile.write("         <director>Unknown</director>\n")
   moviexmlfile.write("         <actors>Unknown</actors>\n") 
   moviexmlfile.write("         <description>None</description>\n")
   moviexmlfile.write("         <path>" + os.getcwd() + dirname[1:] + "/" + filename + "</path>\n")
   moviexmlfile.write("         <length>Unknown</length>\n")
   moviexmlfile.write("         <videocodec>mp4</videocodec>\n")
   moviexmlfile.write("         <poster>images/videoicon.jpg</poster>\n")
   moviexmlfile.write("      </movie>\n")

   OutFile.write("      <movie>\n")
   OutFile.write("         <origtitle>"+ filename + "</origtitle>\n")
   OutFile.write("         <year> Unknown </year>\n")
   OutFile.write("         <genre> " + notwatched + homemovie +"All, Unknown</genre>\n")
   OutFile.write("         <mpaa>UR</mpaa>\n")
   OutFile.write("         <director>Unknown</director>\n")
   OutFile.write("         <actors>Unknown</actors>\n") 
   OutFile.write("         <description>None</description>\n")
   OutFile.write("         <path>" + os.getcwd() + dirname[1:] + "/" + filename + "</path>\n")
   OutFile.write("         <length>Unknown</length>\n")
   OutFile.write("         <videocodec>mp4</videocodec>\n")
   OutFile.write("         <poster>images/videoicon.jpg</poster>\n")
   OutFile.write("      </movie>\n")

def WriteMovieInfo(OutFile, filename, dirname, moviexmlfile):
   

   mov = None   
   if filename[-4:] in movie_file_extensions:
      mov = FindVideo(filename[:-4])
   else:
      print "not a movie"
      return

   if mov == None:
      WriteDefaultMovieInfo(OutFile, filename, dirname, moviexmlfile)
      return  
   

   #rating
   mpaa = ""
   rating = mov.get('mpaa')
   if rating:
      i = rating.find("Rated ")
      if i != -1:
        x = rating.find(" ", i+6)
        if x != -1:
           mpaa = rating[i+6:x]
           print mpaa
   else:
      mpaa = "UR"
   print "Rating: " + mpaa;


   #title
   title = mov.get('title')
   if title == None:
      title = filename
   print title
      

   #director
   director = mov.get('director')
   if director:
      directorname = unicodedata.normalize('NFKD', director[0]['name']).encode('ascii', 'ignore')
      print directorname
   else:
      directorname = "Unknown"

   genrestring = ""
   genres = mov.get('genre')
   if genres:
      for genre in genres:
         if genrestring == "":
            genrestring = str(genre)
         else:
            genrestring = genrestring + ", " + str(genre)

   print genrestring

   caststring = ""
   cast = mov.get('cast')
   if cast:
      for person in cast[0:6]:
         if caststring == "":
            caststring = unicodedata.normalize('NFKD',unicode(person)).encode('ascii', 'ignore')
         else:
            caststring = caststring + ", " + unicodedata.normalize('NFKD',unicode(person)).encode('ascii', 'ignore')

  # print caststring


   plot = mov.get('plot', u'')
  # print plot
   plotstring = "None"
   if plot:
      plot = plot[0]
      i = plot.find('::')
      if i != -1:
         plot = plot[:i]
      plotstring = unicodedata.normalize('NFKD',plot).encode('ascii', 'ignore')

  # print plotstring

   yearstring = "Unknown"
   year = mov.get('year')
   if year:
      yearstring = str(year)
   #print year
   
   runtimestring = ""
   runtime = mov.get('runtimes')
   if runtime:
      rt = runtime[0]
      i = rt.find(':')
      if i == -1:
         runtimestring = str(rt)
      else:
         runtimestring = str(rt[i+1:])
      i = runtimestring.find('::')
      if i != -1:
         runtimestring = runtimestring[:i]

   #print runtimestring


   notwatched = ""
   if ("Not Watched Yet" in dirname):
      notwatched = "Not Watched Yet,"

   homemovie = ""
   if ("HomeMovies" in dirname):
      homemovie = "Home Movies,"
   
   moviexmlfile.write("      <movie>\n")
   moviexmlfile.write("         <origtitle>"+ title.encode('ascii', 'ignore') + "</origtitle>\n")
   moviexmlfile.write("         <year>" + yearstring + "</year>\n")
   moviexmlfile.write("         <genre> All, " + notwatched + homemovie + genrestring.encode('ascii', 'ignore') + "</genre>\n")
   moviexmlfile.write("         <mpaa>" + mpaa + "</mpaa>\n")
   moviexmlfile.write("         <director>" + directorname + "</director>\n")
   moviexmlfile.write("         <actors>" + caststring + "</actors>\n") 
   moviexmlfile.write("         <description>" + plotstring + "</description>\n")
   moviexmlfile.write("         <path>" + os.getcwd() +  dirname[1:] +"/"+ filename + "</path>\n")
   moviexmlfile.write("         <length>" + runtimestring + "</length>\n")
   moviexmlfile.write("         <videocodec>mp4</videocodec>\n")
   moviexmlfile.write("         <poster>images/videoicon.jpg</poster>\n")
   moviexmlfile.write("      </movie>\n")
   

   OutFile.write("      <movie>\n")
   OutFile.write("         <origtitle>"+ title.encode('ascii', 'ignore') + "</origtitle>\n")
   OutFile.write("         <year>" + yearstring + "</year>\n")
   OutFile.write("         <genre> All, " + notwatched + homemovie + genrestring.encode('ascii', 'ignore') + "</genre>\n")
   OutFile.write("         <mpaa>" + mpaa + "</mpaa>\n")
   OutFile.write("         <director>" + directorname + "</director>\n")
   OutFile.write("         <actors>" + caststring + "</actors>\n") 
   OutFile.write("         <description>" + plotstring + "</description>\n")
   OutFile.write("         <path>" + os.getcwd() +  dirname[1:] +"/"+ filename + "</path>\n")
   OutFile.write("         <length>" + runtimestring + "</length>\n")
   OutFile.write("         <videocodec>mp4</videocodec>\n")
   OutFile.write("         <poster>images/videoicon.jpg</poster>\n")
   OutFile.write("      </movie>\n")


def CopyMovieInfo(XMLFile, xmlfilename):
   tempfile = open(xmlfilename, "r")
   lines = tempfile.readlines()
   for line in lines:
      XMLFile.write(line)
   tempfile.close()

def MoviesinDirWrite(XMLFile, dirname, names, filename):

   print "MID: " + filename
   if os.path.isdir(filename):
      print "ERROR: MID got a directory!"

   #filelist = os.listdir(dirname)
   #for filename in filelist:
   if filename[-4:] not in movie_file_extensions:
      return
   xmlfilename = dirname + "/" + filename[:-3] + "xml"
   print xmlfilename
   if os.path.exists(xmlfilename):
      print "XML file exists"
      CopyMovieInfo(XMLFile, xmlfilename)
   else:
      tempmoviefile = open(xmlfilename, "w")
      WriteMovieInfo(XMLFile, filename, dirname, tempmoviefile)
      tempmoviefile.close()


def ProcessDirectory(XMLFile, dirname, names):
   #filelist = os.listdir(dirname)

   #print names
#   print "PD: " + str(filelist)
   #print "PD: " + dirname
   for entry in names:
      #print "PD: entry: " + entry
      #if os.path.isdir(entry):
         #os.path.walk(dirname + "/" + entry, ProcessDirectory, XMLFile)
      #   ProcessDirectory(XMLFile, dirname + "/" + entry, names)
      #else:
      MoviesinDirWrite(XMLFile, dirname, names, entry)



XMLFile = open("Videos.xml", "w")
XMLFile.write("<xml>\n")
XMLFile.write("   <viddb>\n")


#ProcessDirectory(XMLFile, ".", names)
os.path.walk(".", ProcessDirectory, XMLFile)

XMLFile.write("   </viddb>\n")
XMLFile.write("</xml>\n")
XMLFile.close()

