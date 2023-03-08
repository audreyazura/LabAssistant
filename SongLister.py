from mutagen.flac import FLAC
from mutagen.mp3 import EasyMP3
from os import listdir
from os.path import isdir, isfile, splitext

def get_directories_and_files(directory):
    directory_list = []
    file_list = []
    for file_name in listdir(directory):
        extension = splitext(file_name)[1]
        file = directory + "/" +  file_name

        if isdir(file):
            directory_list.append(file)
        else:
            if isfile(file) and (extension == ".mp3" or extension == ".flac"):
                file_list.append(file)

    return directory_list, file_list

directory_list = ["/home/audreyazura/Music"]
file_list = []

print("Getting all the audio files.")
old_directory_list_size = 0
while not(len(directory_list) == old_directory_list_size):
    old_directory_list_size = len(directory_list)
    for directory in directory_list:
        if isdir(directory):
            (new_directories, new_files) = get_directories_and_files(directory)
            for new_dir in new_directories:
                if not(new_dir in directory_list):
                    directory_list.append(new_dir)
            for new_file in new_files:
                new_file = new_file.split("/Music/")[1]
                if not(new_file in file_list):
                    file_list.append(new_file)

print("Creating the white-list and the song database")
artist_album_song_dict = {}
song_command_dict = {}
with open("AddressWhiteList.dat", "w") as white_list_file:
    for file in file_list:
        print(file, file=white_list_file)

        artist = ""
        album = ""
        title = ""
        track = ""
        if splitext(file)[1] == ".flac":
            flac_file = FLAC("/home/audreyazura/Music/" + file)
            if flac_file.tags is not None:
                artist = flac_file.tags["artist"][0] if "artist" in flac_file.tags else "Unknown artist"
                album = flac_file.tags["album"][0] if "album" in flac_file.tags else "Unknown album"
                title = flac_file.tags["title"][0] if "title" in flac_file.tags else "Unknown track"
                track = flac_file.tags["tracknumber"][0] if "tracknumber" in flac_file.tags else ""
        else:
            if splitext(file)[1] == ".mp3":
                mp3_file = EasyMP3("/home/audreyazura/Music/" + file)
                if mp3_file.tags is not None:
                    artist = mp3_file.tags["artist"][0] if "artist" in mp3_file.tags else "Unknown artist"
                    album = mp3_file.tags["album"][0] + " (mp3)" if "album" in mp3_file.tags else "Unknown album"
                    title = mp3_file.tags["title"][0] + " (mp3)" if "title" in mp3_file.tags else "Unknown track"
                    track = mp3_file.tags["tracknumber"][0] if "tracknumber" in mp3_file.tags else ""

        track = track.split("/")[0]
        if len(track) == 1:
            track = "0" + track
        title = track + " - " +  title
        if artist in artist_album_song_dict:
            if album in artist_album_song_dict[artist]:
                artist_album_song_dict[artist][album].append(title)
            else:
                artist_album_song_dict[artist][album] = [title]
        else:
            artist_album_song_dict[artist] = {album:[title]}

        song_command_dict[title] = "!sr " + file

print("Writing the html file")
artist_list = list(artist_album_song_dict)
artist_list.sort()
with open("SongList.html", "w") as list_file:
    print("<html>", file=list_file)
    print("<head>", file=list_file)
    print("\t<link rel=\"stylesheet\" type=\"text/css\" href=\"stylesheet.css\">", file=list_file)
    print("\t<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">", file=list_file)
    print("\t<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>", file=list_file)
    print("\t<link href=\"https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&family=Jost:ital,wght@0,400;0,600;1,400;1,600&display=swap\" rel=\"stylesheet\">", file=list_file)
    print("\t<script>", file=list_file)
    print("\t\tfunction copy(text)", file=list_file)
    print("\t\t{", file=list_file)
    print("\t\t\tnavigator.clipboard.writeText(text);", file=list_file)
    print("\t\t}", file=list_file)
    print("\t</script>", file=list_file)
    print("</head>", file=list_file)
    print("<body>", file=list_file)
    print("<h1>Song list</h1>", file=list_file)
    for artist in artist_list:
        if artist != "":
#            print("<details class=\"artist\">", file=list_file)
#            print("<summary>" +  + "</summary>", file=list_file)
            album_list = list(artist_album_song_dict[artist])
            album_list.sort()
            for album in album_list:
                print("\t<details class=\"album\">", file=list_file)
                print("\t<summary>" + album + " [" + artist.replace("\n", " ; ") + "]</summary>", file=list_file)
                print("\t<table>", file=list_file)
                song_list = artist_album_song_dict[artist][album]
                song_list.sort()
                for song in song_list:
                    print("\t\t<tr>", file=list_file)
                    print("\t\t<td>" + song + "</td><td><input type=\"button\" onClick=\"copy(\'" + song_command_dict[song] + "\')\" value=\"" + song_command_dict[song] + "\" class=\"command\"></td>", file=list_file)
                    print("\t\t</tr>", file=list_file)
                print("\t</table>", file=list_file)
                print("\t</details>", file=list_file)
                print("<br>", file=list_file)
#            print("</details><br>", file=list_file)
    print("</body></html>", file=list_file)
