from datetime import datetime
from src.storage import upload, get_url, delete, sweep

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


def test_delete(mocker):
  id = "test"
  service = mocker.Mock()

  delete(service, id)

  assert 1 == service.files().delete().execute.call_count


def test_sweep(mocker):
  files = [
    {"id": "0", "createdTime": "2022-10-18T23:12:13.783Z"},
    {"id": "1", "createdTime": "2021-10-10T23:12:13.783Z"},
    {"id": "2", "createdTime": "1990-10-10T23:12:13.783Z"}
  ]
  service = mocker.Mock()
  service.files().list().execute.return_value = {"files": files}
  mocker.patch(
    "src.storage.utc_now",
    return_value=datetime.strptime("2022-10-18 04:22:52", "%Y-%m-%d %H:%M:%S")
  )

  deleted = sweep(service)

  assert 1 == service.files().list().execute.call_count
  assert 2 == service.files().delete().execute.call_count
  assert 2 == deleted
