#!/usr/bin/env python

import os

from modules.operations import convert_flac_to_ogg, delete_artist, delete_tmp_files, retag_copy_mp3_album
from modules.classes import Artist

srcRoot = "/mnt/hylia/"
destination = "/mnt/usb/"
paths = ["Music", "Music_FLAC"]
tmp = "/tmp/reboar"
no_per_page = 20

if __name__ == "__main__":
  queue = {
    "delete_artists": [],
    "convert_albums": [],
    "copy_albums": [],
  }

  if os.path.isdir(tmp):
    delete_tmp_files(tmp)

  # buildup artist tree
  artist_list = []
  for path in paths:
    cur_path = os.path.join(srcRoot, path)
    with os.scandir(cur_path) as it:
      for entry in it:
        if entry.is_dir():
          artist_list.append(Artist(entry.name, entry.path, destination))

  # sort and enumerate the artists
  artist_list.sort(key=lambda x: x.name)
  artist_index = 1
  for artist in artist_list:
    artist.number = artist_index
    artist_index += 1
  
  if input("Remove existing? (Y/n) ").lower() not in ["n","no"]:
    existing = filter(lambda x: x.dest_artist_exists, artist_list)
    dict = {} # store pointers using artist number
    for artist in existing:
      dict[artist.number] = artist
      print(artist.number, " -- ", artist.name, " - ", "Full" if artist.dest_artist_full else "Partial")
    
    for artist in input("Enter the numbers of the artists you want to remove: (comma separated, no spaces. ie 1,2,3)").split(","):
      if int(artist) in dict:
        current_artist = dict[int(artist)]
        current_artist.remove_artist = True
        queue["delete_artists"].append(current_artist)

  if input("Add new? (Y/n) ").lower() not in ["n","no"]:
    candidates = filter(lambda x: (x.remove_artist or not x.dest_artist_exists), artist_list)
    dict = {} # store pointers using artist number
    for artist in candidates:
      dict[artist.number] = artist
      print(artist.number, " -- ", artist.name, " - ", "Full" if artist.dest_artist_full else "Partial")
    
    for artist in input("Enter the numbers of the artists you'd like to add: (comma separated, no spaces. ie 1,2,3) ").split(","):
      if int(artist) in dict.keys():
        current_artist = dict[int(artist)]
        mini_dict = {}
        for album in current_artist.albums:
          mini_dict[album.number] = album
          print(album.number, " -- ", album.name)

        for album in input("Enter the numbers of the albums you'd like to copy: (comma separated, no spaces. ie 1,2,3) ").split(","):
          if int(album) in mini_dict.keys():
            current_album = mini_dict[int(album)]
            queue["convert_albums"].append(current_album) if current_album.need_convert else queue["copy_albums"].append(current_album)

  print("Artists marked for deletion: ", len(queue["delete_artists"]))
  print("Albums marked for conversion: ", len(queue["convert_albums"]))
  print("Albums marked for copying: ", len(queue["copy_albums"]))

  if input("Continue? (Y/n) ").lower() not in ["n","no"]:
    for artist in queue["delete_artists"]:
      delete_artist(artist)
    for album in queue["convert_albums"]:
      convert_flac_to_ogg(album, tmp)
    for album in queue["copy_albums"]:
      retag_copy_mp3_album(album)
