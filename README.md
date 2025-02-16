# transcribe_htr_from_iiif 

## About

This is a sample utility originally created to test the handwritten text recognition from Claude for the purposes of
transcription. You can transcribe a document by:

* Pointing at a IIIF Image response
* Image file
* or a IIIF Manifest (in progress)

## Installing

Installation is easiest with pipx:

```shell
pipx install htr_iiif_claude
```

You can also install with pip but do some mindfully:

```shell
pip install htr_iiif_claude
```

## Configuring API Key

Set API key as an environmental variable called `CLAUDE_API` using your preferred method.

## Transcribing

To transcribe a single IIIF image doc, just:

```shell
htr transcribe -i https://api.library.tamu.edu/iiif/2/50ae1c1c-b272-3d64-b132-c17d9704d49a/info.json   
```

## Describing 

To describe an image, you can:

```shell
htr describe -i josh.jpg -p "Give this image a title, description, and 3 subjects. Respond with the message as JSON with title, description and subject keys with values as strings."
```

## Describing a Full CSV

Describing a full CSV can be done many ways, but the simplest approach is something like:

```shell
htr describe_simple -c htr_describe2.csv -o flickr2 -s 6413 -e 6415 -f "Item title|Publisher" -i "Medium Image"
```

Use `-i` to tell it where to find the field with the image (either online or on disk), optionally use `-f` to pass
certain metadata fields to claude (separate with `|`), and use `-s` and `-e` to start and end at specific points.
