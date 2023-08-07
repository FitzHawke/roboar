#!/usr/bin/env python

import os, shutil
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis

def convert_flac_to_ogg(album, tmp):
  tmp_dir = os.path.join(tmp, album.artist, album.name)
  os.makedirs(tmp_dir , exist_ok=True)
  for song in album.songs:
    tmp_path = os.path.join(tmp_dir, song.name + ".ogg")
    input_song = AudioSegment.from_file(song.path, "flac")
    print("Converting ", song.artist, " - ", song.album, " - ", song.name, " to ogg")
    input_song.export(tmp_path, format="ogg")
    retag_copy_ogg(song, tmp_path, album.dest_album_dir)

  delete_tmp_files(tmp_dir)

# copy then write tags
def retag_copy_mp3_album(album):
  for song in album.songs:
    copy_song(song.path, song.dest_path, album.dest_album_dir)
    current_song = EasyID3(song.dest_path)

    print("re-tagging ", song.artist, " - ", song.album, " - ", song.name, " at " , song.dest_path)
    tags = build_tags(song)

    for tag in tags:
      current_song[tag] = tags[tag]
    current_song.save()

def retag_copy_ogg(song, tmp_path, dest_dir):
  copy_song(tmp_path, song.dest_path, dest_dir)
  current_song = OggVorbis(song.dest_path)

  print("re-tagging ", song.artist, " - ", song.album, " - ", song.name, " at " , song.dest_path)
  tags = build_tags(song)

  current_song["TITLE"] = tags["title"]
  current_song["ALBUM"] = tags["album"]
  current_song["ARTIST"] = tags["artist"]
  current_song["PERFORMER"] = tags["artist"]
  current_song["TRACKNUMBER"] = tags["tracknumber"]

  current_song.save()
  
def copy_song(src, dest, dir):
  if not os.path.isdir(dir):
    os.makedirs(dir)
  print("copying ", src, " to ", dest)
  shutil.copyfile(src, dest)

def build_tags(song):
  return {
    "artist": song.artist,
    "album": song.album,
    "title": song.name,
    "tracknumber": str(song.new_track_number),
    "discnumber": str(song.new_disk_number),
  }

def delete_artist(artist):
  shutil.rmtree(artist.dest_artist_dir)

def delete_tmp_files(tmp):
  shutil.rmtree(tmp)