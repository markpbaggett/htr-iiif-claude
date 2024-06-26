# transcribe_htr_from_iiif 

## About

Transcribe Handwritten Text from IIIF with Claude

* Point at an Image response
* Point at a Manifest (in progress)

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

Set API key as `CLAUDE_API`

## Running

To transcribe a single IIIF image doc, just:

```shell
htr transcribe -i https://api.library.tamu.edu/iiif/2/50ae1c1c-b272-3d64-b132-c17d9704d49a/info.json   
```
