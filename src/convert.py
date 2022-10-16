import os

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
  output_path = os.path.join("/tmp", f"{filename}.mp3")
  audio.download(filename=output_path)
  return output_path
