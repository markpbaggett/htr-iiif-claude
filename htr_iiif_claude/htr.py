import json

import httpx

from htr_iiif_claude.image import Image
from htr_iiif_claude.claude import ClaudeRequest
from htr_iiif_claude.manifest import Manifest
import os
import click
from tqdm import tqdm
from csv import DictReader


@click.group()
def cli() -> None:
    pass


@cli.command(
    "describe", help="Describe an image and get back a title and a description from image and metadata"
)
@click.option(
    "--image_uri",
    "-i",
    help="The URI of a IIIF Image",
)
@click.option(
    "--prompt",
    "-p",
    default='Give this image a title and a description based on its contents.',
    help="The prompt to submit with the image",
)
@click.option(
    "-d",
    "--metadata",
    help="Prexisting descriptive metadata"
)
@click.option(
    "--model",
    "-m",
    default="claude-3-haiku-20240307",
    help="The model to use",
)
@click.option(
    "--output",
    "-o",
    default="output",
    help="The output file to write text to",
)
def describe(image_uri: str, prompt: str, metadata: str, model: str, output: str) -> None:
    image = Image(image_uri_or_path=image_uri)
    y = ClaudeRequest(
        model=model,
        key=os.getenv("CLAUDE_API"),
        prompt=f'{prompt} Respond with the message as output in JSON format with keys "title", "description" and values '
               f'as str. The image has the following metadata: {metadata}',
        image=image.hash
    )
    if type(y.text) == str:
        with open(f"{output}.txt", "w") as f:
            f.write(y.text)
    elif type(y.text) == dict:
        with open(f"{output}.json", "w") as f:
            json.dump(y.text, f)
    print(f"Done. Total cost was: {y.cost.get('total')}. Results written to {output}")

@cli.command("describe_csv", help="Describe images in a CSV")
@click.option(
    "--model",
    "-m",
    default="claude-3-haiku-20240307",
    help="The model to use",
)
@click.option(
    "--output",
    "-o",
    default="output",
    help="The output directory to write text to",
)
@click.option(
    "--csv",
    "-c",
    default="htr_describe.csv"
)
@click.option(
    "--start",
    "-s",
    default="1",
)
@click.option(
    "--end",
    "-e",
    default="10",
)
def describe_csv(model: str, output: str, csv: str, start: str, end: str) -> None:
    total_images_to_get = int(end)
    with open(csv, 'r') as csvfile:
        i = 0
        reader = DictReader(csvfile)
        for _ in range(int(start) - 1):
            next(reader)
        for row in reader:
            if i <= total_images_to_get:
                try:
                    fields_that_matter = (
                    "Item title", "Creator", "Publisher", "Category", "Location", "Collection", "Title",
                    "Creator (Photographer)", "Year (Coverage)", "Description", "Note", "Descriptive Notes", "Caption",
                    "Subject", "Event", "Keywords", "Drawing Name")
                    metadata_elements = []
                    for field in fields_that_matter:
                        if row[field] != "":
                            metadata_elements.append(f"{field}: {row[field]}")
                    image = Image(image_uri_or_path=row['Medium Image'])
                    y = ClaudeRequest(
                        model=model,
                        key=os.getenv("CLAUDE_API"),
                        prompt=f'Give this image a title and a description based on its contents. Respond with the message '
                               f'as output in JSON format with keys "title", "description" and values '
                               f'as str. The image has the following metadata: {",".join(metadata_elements)}',
                        image=image.hash,
                    )
                    if type(y.text) == str:
                        try:
                            json_data = json.loads(y.text)
                            with open(f"{output}/{row['Item link'].split('/')[-1].split('.')[0]}.json", "w") as f:
                                json.dump(json_data, f, indent=4)
                        except json.decoder.JSONDecodeError:
                            print(f"Couldn't convert string to json for {row['Item link']}\n")
                    elif type(y.text) == dict:
                        with open(f"{output}/{row['Item link'].split('/')[-1].split('.')[0]}.json", "w") as f:
                            json.dump(y.text, f, indent=4)
                    print(f"Done. Total cost was: {y.cost.get('total')}. Results written to {output}/{row['Item link'].split('/')[-1].split('.')[0]}")
                    i += 1
                except httpx.ReadTimeout as e:
                    print(f"Read timed out: {row['Item link']}\n")
                    i += 1


@cli.command("transcribe", help="Transcribe an image with Claude")
@click.option(
    "--image_uri",
    "-i",
    help="The URI of a IIIF Image",
)
@click.option(
    "--manifest",
    "-ma",
    help="The URI of a IIIF Manifest",
)
@click.option(
    "--prompt",
    "-p",
    default='This image contains handwritten text. Find all handwritten text.',
    help="The prompt to submit with the image",
)
@click.option(
    "--model",
    "-m",
    default="claude-3-haiku-20240307",
    help="The model to use",
)
@click.option(
    "--output",
    "-o",
    default="output.txt",
    help="The output file to write text to",
)
def transcribe(
        image_uri: str,
        prompt: str,
        model: str,
        output: str,
        manifest: str,
) -> None:
    if manifest:
        iiif_manifest = Manifest(manifest)
        images = iiif_manifest.get_images()
        total = 0.0
        for item in tqdm(images):
            image = Image(image_uri_or_path=item)
            y = ClaudeRequest(
                model=model,
                key=os.getenv("CLAUDE_API"),
                prompt=f'{prompt} Respond with the message as output in JSON format with keys: "htr" (string)',
                image=image.hash
            )
            with open(f"{output}/{item.split('/')[-2]}", "w") as f:
                f.write(y.text)
            total += y.cost.get('total')
        print(f"Done. Total cost was: {total}")
    else:
        image = Image(image_uri_or_path=image_uri)
        y = ClaudeRequest(
            model=model,
            key=os.getenv("CLAUDE_API"),
            prompt=f'{prompt} Respond with the message as output in JSON format with keys: "contents" (list(dict(content,page)))',
            image=image.hash
        )
        if type(y.text) == str:
            with open(output, "w") as f:
                f.write(y.text)
        elif type(y.text) == dict:
            with open(output, "w") as f:
                json.dump(y.text, f)
        print(f"Done. Total cost was: {y.cost.get('total')}")
