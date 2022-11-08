from src.convert import convert


def test_convert_valid_path(mocker):
  id = "test-id"
  filename = "test-file"
  mocker.patch("src.convert.YouTube")
  mocker.patch("src.convert.subprocess")

  path = convert(id, filename)

  assert "/tmp/test-file.mp3" == path
