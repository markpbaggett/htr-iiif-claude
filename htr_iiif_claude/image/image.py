import httpx
import base64


class Image:
    def __init__(self, image_uri):
        self.uri = image_uri
        self.gray = self.__get_full_gray(image_uri)
        self.converted = self.__convert(self.gray)
        self.hash = [self.__get_hash()]

    @staticmethod
    def __get_full_gray(url):
        x = f"{url.replace('/info.json', '')}/full/full/0/gray.jpg"
        size = len(httpx.get(x).content)
        if size < 4000000:
            return x
        else:
            return f"{url.replace('/info.json', '')}/full/pct:50/0/gray.jpg"

    @staticmethod
    def __convert(image_url):
        return base64.b64encode(
            httpx.get(
                image_url
            ).content
        ).decode("utf-8")

    @staticmethod
    def __switch_image_to_hash(image):
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image
            }
        }

    def __get_hash(self):
        return self.__switch_image_to_hash(
            self.converted
        )


if __name__ == '__main__':
    x = Image('https://api.library.tamu.edu/iiif/2/50ae1c1c-b272-3d64-b132-c17d9704d49a/info.json')

