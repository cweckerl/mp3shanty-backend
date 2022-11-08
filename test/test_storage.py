from src.storage import upload, get_url

def test_upload(mocker):
  path = "/tmp/test.mp3"
  service = mocker.Mock()
  mocker.patch("src.storage.MediaFileUpload")

  upload(service, path)
    
  assert 1 == service.files().create().execute.call_count


def test_get_url(mocker):
  id = "test"
  service = mocker.Mock()

  get_url(service, id)

  assert 1 == service.files().get().execute.call_count
