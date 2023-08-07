#!/usr/bin/env python

import os

class Song:
  def __init__(self, name, path, artist, album, destination):
    self.name, self.type = os.path.splitext(name)
    self.path = path
    self.artist = artist
    self.album = album
    self.dest_path = os.path.join(destination, self.artist, self.album, self.name + (".ogg" if self.type == ".flac" else self.type))
    self.dest_song_exists = os.path.isfile(self.dest_path)
    
    # normalize the naming conventions to gather track number and album number as 1-12
    track_info = self.name.split(" ")
    if (track_info[1] != "-" and not "-" in track_info[0])or(not "-" in track_info[0]): # test for 1-12 style
      # means [0] is `12.` or `12`
      if track_info[0].endswith("."):
        track_info[0] = "1-" + track_info[0][:-1]
      else:
        track_info[0] = "1-" + track_info[0]

    self.disk_num, self.track_num = track_info[0].split("-")

class Album:
  def __init__(self, name, path, artist, destination):
    self.name = name
    self.path = path
    self.artist = artist
    self.dest_album_dir = os.path.join(destination, self.artist, self.name)
    with os.scandir(path) as it:
      songs = []
      for entry in it:
        if entry.is_file() and (entry.name.endswith(".mp3") or entry.name.endswith(".flac") or entry.name.endswith(".ogg")):
          songs.append(Song(entry.name, entry.path, artist, name, destination))

    # sort and enumerate the songs with their new track numbers
    self.need_convert = any(s.type == ".flac" for s in songs)
    self.songs = sorted(songs, key=lambda x: int(x.disk_num)*1000 + int(x.track_num))
    song_index = 1
    for song in self.songs:
      song.new_track_number = song_index
      song.new_disk_number = 1
      song_index += 1

    self.dest_album_exists = any(s.dest_song_exists for s in self.songs)
    self.dest_album_full = all(s.dest_song_exists for s in self.songs)
    self.add_album = False
    self.remove_album = False

class Artist:
  def __init__(self, name, path, destination):
    self.name = name
    self.path = path
    self.dest_artist_dir = os.path.join(destination, self.name)
    with os.scandir(path) as it:
      albums = []
      for entry in it:
        if entry.is_dir():
          albums.append(Album(entry.name, entry.path, name, destination))
    
    # sort and enumerate the albums
    self.albums = sorted(albums, key=lambda x: x.name)
    album_index = 1
    for album in self.albums:
      album.number = album_index
      album_index += 1
    self.dest_artist_exists = any(a.dest_album_exists for a in self.albums)
    self.dest_artist_full = all(a.dest_album_full for a in self.albums)
    self.add_artist = False
    self.remove_artist = False
