from htr_iiif_claude.image import Image
from htr_iiif_claude.claude import ClaudeRequest
import os
import click
import httpx
import base64

@click.group()
def cli() -> None:
    pass

@cli.command("transcribe", help="Transcribe an image with Claude")
@click.option(
    "--image_uri",
    "-i",
    required=True,
    help="The URI of a IIIF Image",
)
@click.option(
    "--prompt",
    "-p",
    default='This image contains handwritten text. Please find all handwritten text and respond with the message as output in JSON format with keys: "htr" (string)',
    help="The prompt to submit with the image",
)
@click.option(
    "--model",
    "-m",
    default="claude-3-haiku-20240307",
    help="The model to use",
)
def transcribe(
        image_uri: str,
        prompt: str,
        model: str,
) -> None:
    image = Image(image_uri=image_uri)
    y = ClaudeRequest(
        model=model,
        key=os.getenv("CLAUDE_API"),
        prompt=prompt,
        image=image.hash
    )
    print(y.output)
    print(y.text)

