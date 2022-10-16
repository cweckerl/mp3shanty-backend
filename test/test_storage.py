from src.storage import upload, get_url, delete


def test_upload(mocker):
  path = "/tmp/test.mp3"
  service = mocker.patch("src.storage.get_client")
  mocker.patch("src.storage.MediaFileUpload")

  upload(path)

  assert service.called_once()


def test_get_url(mocker):
  id = "test"
  service = mocker.patch("src.storage.get_client")

  get_url(id)

  assert service.called_once()


def test_delete(mocker):
  id = "test"
  service = mocker.patch("src.storage.get_client")

  delete(id)

  assert service.called_once()
