import httpx
import base64
import os


class Image:
    def __init__(self, image_uri_or_path):
        self.is_uri = self.__is_uri(image_uri_or_path)
        if self.is_uri:
            self.uri = image_uri_or_path
            self.gray = self.__get_full_gray(self.uri)
        else:
            self.path = image_uri_or_path
            self.gray = self.path  # No grayscale transformation needed
        self.converted = self.__convert(self.gray)
        self.hash = [self.__get_hash()]

    @staticmethod
    def __is_uri(string):
        return string.startswith('http://') or string.startswith('https://')

    @staticmethod
    def __get_full_gray(url):
        x = f"{url.replace('/info.json', '')}/full/full/0/gray.jpg"
        size = len(httpx.get(x).content)
        if size < 4000000:
            return x
        else:
            return f"{url.replace('/info.json', '')}/full/pct:50/0/gray.jpg"

    def __convert(self, image_uri_or_path):
        if self.is_uri:
            return base64.b64encode(httpx.get(image_uri_or_path).content).decode("utf-8")
        else:
            with open(image_uri_or_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

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
        return self.__switch_image_to_hash(self.converted)


if __name__ == '__main__':
    # For URI
    # image_uri = 'https://api.library.tamu.edu/iiif/2/50ae1c1c-b272-3d64-b132-c17d9704d49a/info.json'
    # x = Image(image_uri)
    # print(x.hash)

    # For local file
    image_path = '/Users/mark.baggett/Desktop/july_9_output_all_failures.png'
    y = Image(image_path)
    print(y.hash)
