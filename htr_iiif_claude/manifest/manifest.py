import httpx


class Manifest:
    def __init__(self, uri):
        self.uri = uri
        self.contents = httpx.get(uri).json()
        self.version = self.__get_version()

    def __get_version(self):
        schemas = self.contents['@context']
        if isinstance(schemas, list):
            presentation_context = schemas[-1]
        else:
            presentation_context = schemas
        return presentation_context.split('/')[-2]

    def get_images(self):
        if self.version == '2':
            return self.__get_v2_images()
        elif self.version == '3':
            return self.__get_v3_images()

    def __get_v2_images(self):
        image_info = []
        for image in self.contents['sequences'][0]['canvases']:
            image_info.append(f"{image['images'][0]['resource']['service']['@id'].replace('/info.json', '')}/info.json")
        return image_info

    def __get_v3_images(self):
        image_info = []
        for image in self.contents['items']:
            image_info.append(
                f"{image['items'][0]['items'][0]['body']['service'][0]['@id'].replace('/info.json', '')}/info.json"
            )
        return image_info


if __name__ == '__main__':
    manifest = Manifest('https://library.tamu.edu/iiif_manifests/houstonoilmanifest.json')
    print(manifest.get_images())

