import requests
from http_server_client.abstract_camera_http import AbstractCameraModule


class CameraHTTPClient(AbstractCameraModule):
    def __init__(self, url: str = "http://127.0.0.1:8002/"):
        self.url = url

    def single_image(self):
        url = self.url + "single_image"
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            # with open('single_image_old.png', 'wb') as f:
            # f.write(r.content)
            return r.content
        return False
