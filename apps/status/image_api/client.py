import requests

from config import Config

from requests.packages.urllib3.util.retry import Retry


class TaggingException(Exception):
    pass


class ImageAPIClient:
    def __init__(self):
        self.base_url = "https://api.imagga.com/v2"
        self.timeout = Config.IMAGGA_CLIENT_TIMEOUT_SECONDS
        self.retry_strategy = Retry(
            backoff_factor=0.5,
            total=Config.IMAGGA_CLIENT_RETRIES,
        )
        self.session = requests.Session()
        self.session.auth = (Config.IMAGGA_API_KEY, Config.IMAGGA_API_SECRET)

    def face_detection(self, photo, threshold):
        url = f"{self.base_url}/faces/detections"

        resp = self.session.post(
            url,
            timeout=self.timeout,
            files={"image": photo},
            params={"return_face_id": 1},
        )

        resp.raise_for_status()

        data = resp.json()
        faces = data["result"]["faces"]
        if len(faces) != 1:
            raise TaggingException("multiple or insufficient faces detected.")

        face = faces[0]
        if face["confidence"] >= threshold:
            return face

        raise TaggingException("confidence threshold not met.")

    def face_similarity(self, photo1_face_id, photo2_face_id, threshold):
        url = f"{self.base_url}/faces/similarity"

        resp = self.session.get(
            url,
            timeout=self.timeout,
            params={"face_id": photo1_face_id, "second_face_id": photo2_face_id},
        )

        resp.raise_for_status()

        data = resp.json()
        similarity = data["result"]["score"]

        return (similarity >= threshold)
