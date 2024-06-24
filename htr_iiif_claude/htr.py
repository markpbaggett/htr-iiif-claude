from htr_iiif_claude.image import Image
from htr_iiif_claude.claude import ClaudeRequest
from htr_iiif_claude.manifest import Manifest
import os
import click


@click.group()
def cli() -> None:
    pass


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
    default='This image contains handwritten text. Please find all handwritten text.',
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
        for item in images:
            image = Image(image_uri=item)
            y = ClaudeRequest(
                model=model,
                key=os.getenv("CLAUDE_API"),
                prompt=f'{prompt} Respond with the message as output in JSON format with keys: "htr" (string)',
                image=image.hash
            )
            with open(item.split('/')[-2], "w") as f:
                f.write(y.text)
    else:
        image = Image(image_uri=image_uri)
        y = ClaudeRequest(
            model=model,
            key=os.getenv("CLAUDE_API"),
            prompt=f'{prompt} Respond with the message as output in JSON format with keys: "htr" (string)',
            image=image.hash
        )
        with open(output, "w") as f:
            f.write(y.text)
        print(f"Done. Total cost was: {y.cost.get('total')}")
