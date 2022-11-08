import os
import subprocess

from pytube import YouTube


def convert(id: str, filename: str) -> str:
  """Converts video ID to mp3.

  Parameters
  ----------
  id : str
    Video ID.

  Returns
  -------
  str
    Output path of saved mp3.
  """
  uri = f"https://www.youtube.com/watch?v={id}"
  yt = YouTube(uri)
  audio = yt.streams.get_audio_only()
  mp4_path = os.path.join("/tmp", f"{filename}.mp4")
  tmp_file_path = os.path.join("/tmp", "tmp.mp3")
  mp3_path = os.path.join("/tmp", f"{filename}.mp3")
  audio.download(filename=mp4_path)
  subprocess.run(["ffmpeg", "-i", mp4_path, "-vn", tmp_file_path])
  subprocess.run([
    "ffmpeg", "-i", tmp_file_path, "-i", f"https://img.youtube.com/vi/{id}/maxresdefault.jpg", 
    "-map", "0:0", "-map", "1:0", "-c", "copy", "-id3v2_version", "3",
    "-metadata:s:v", 'title="Album cover"',
    "-metadata:s:v", 'comment="Cover (front)"', "-metadata", f"title={filename}", mp3_path
  ])
  return mp3_path
