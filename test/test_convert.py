from src.convert import convert


def test_convert_valid_path(mocker):
  id = "test-id"
  title = "test-file"
  artist = "tester"
  mocker.patch("src.convert.YouTube")
  mocker.patch("src.convert.subprocess")

  path = convert(id, title, artist)

  assert "/tmp/test-file.mp3" == path
