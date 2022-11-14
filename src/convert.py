import os
import subprocess

from pytube import YouTube


def convert(id: str, title: str, artist: str, album: str = "") -> str:
  """Converts video ID to mp3.

  Parameters
  ----------
  id : str
    Video ID.
  title : str
    Title of the track.
  artist : str
    Artist of the track.
  album : str, default=""
    Album of the track.

  Returns
  -------
  str
    Output path of saved mp3.
  """
  uri = f"https://www.youtube.com/watch?v={id}"
  yt = YouTube(uri)
  audio = yt.streams.get_audio_only()
  mp4_path = os.path.join("/tmp", f"{title}.mp4")
  cover_path = os.path.join("/tmp", f"{id}.jpg")
  tmp_file_path = os.path.join("/tmp", f"{id}.mp3")
  mp3_path = os.path.join("/tmp", f"{title}.mp3")
  audio.download(filename=mp4_path)

  # /opt/bin/ffmpeg
  p = subprocess.run(
    [
      "ffmpeg",
      "-y",
      "-i", f"https://img.youtube.com/vi/{id}/maxresdefault.jpg",
      "-vf",
      "crop=720:720:280:720",
      cover_path,
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT,
  )
  subprocess.run(
    ["ffmpeg", "-y", "-i", mp4_path, "-vn", tmp_file_path],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT,
  )
  if p.returncode != 0:
    subprocess.run(
      [
        "ffmpeg",
        "-y",
        "-i", tmp_file_path,
        "-c", "copy",
        "-id3v2_version", "3",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        mp3_path,
      ],
      stdout=subprocess.DEVNULL,
      stderr=subprocess.STDOUT,
    )
  else:
    subprocess.run(
      [
        "ffmpeg",
        "-y",
        "-i", tmp_file_path,
        "-i", cover_path,
        "-map", "0:0",
        "-map", "1:0",
        "-c", "copy",
        "-id3v2_version", "3",
        "-metadata:s:v", 'title="Album cover"',
        "-metadata:s:v", 'comment="Cover (front)"',
        "-metadata", f"title={title}",
        "-metadata", f"album={album}",
        "-metadata", f"artist={artist}",
        mp3_path,
      ],
      stdout=subprocess.DEVNULL,
      stderr=subprocess.STDOUT,
    )
  return mp3_path
