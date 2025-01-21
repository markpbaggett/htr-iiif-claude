from csv import DictReader
import subprocess

total_images_to_get = 10

with open('htr_describe.csv', 'r') as csvfile:
    reader = DictReader(csvfile)
    i = 0
    for row in reader:
        if i <= total_images_to_get:
            fields_that_matter = ("Item title", "Creator", "Publisher", "Category", "Location", "Collection", "Title", "Creator (Photographer)", "Year (Coverage)", "Description", "Note", "Descriptive Notes", "Caption", "Subject", "Event", "Keywords", "Drawing Name")
            metadata_elements = []
            for field in fields_that_matter:
                if row[field] != "":
                    metadata_elements.append(f"{field}: {row[field]}")
            command = [
                "htr",
                "describe",
                "-i", row["Item link"],
                "-d", ",".join(metadata_elements),
                "-o", f"flickr/{row['Item link'].split('/')[-1].split('.')[0]}",
            ]
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            i += 1
