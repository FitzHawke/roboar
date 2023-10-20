#!/usr/bin/env python

import os
from modules.inputs import user_input_list, user_input_yn
from modules.operations import delete_artist, delete_tmp_files, retag_copy
from modules.classes import Artist

# configs
srcRoot = "/mnt/hylia/"
default_destination = "/mnt/usb"
paths = ["Music", "Music_FLAC"]
tmp = "/tmp/reboar"
page_size = 10

if __name__ == "__main__":
  queue = {
    "delete_artists": [],
    "copy_albums": [],
  }

  destination = input(f'Path to mounted usb (default: {default_destination}): ') or destination
  if not os.path.isdir(destination):
    print(f'Path {destination} does not exist :(')
    exit()

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

  print(len(artist_list), "artists")

  if user_input_yn("Remove existing? (Y/n) "):
    existing = filter(lambda x: x.dest_artist_exists, artist_list)
    user_input_list(list(existing), "Enter the numbers of the artists you want to remove: (comma separated, no spaces. ie 1,2,3 q to quit) ", queue["delete_artists"], page_size)

  if user_input_yn("Add new? (Y/n) "):
    candidates = filter(lambda x: (x.remove_artist or not x.dest_artist_full), artist_list)
    selected = user_input_list(list(candidates), "Enter the numbers of the artists you'd like to add: (comma separated, no spaces. ie 1,2,3 q to quit) ",[],page_size)
    if user_input_yn("Skip individual album selection? (Y/n) "):
      for artist in selected:
        for album in artist.albums:
          queue["copy_albums"].append(album)
    else:
      for artist in selected:
        user_input_list(list(artist.albums), "Enter the numbers of the albums you'd like to add: (comma separated, no spaces. ie 1,2,3 q to quit) ", queue["copy_albums"], page_size)

  print("Artists marked for deletion: ", len(queue["delete_artists"]))
  print("Albums marked for copying/converting: ", len(queue["copy_albums"]))

  if user_input_yn("Continue? (Y/n) "):
    for artist in queue["delete_artists"]:
      delete_artist(artist)
    for album in queue["copy_albums"]:
      retag_copy(album, tmp)