import json
from datetime import datetime

def transform_data(input_data):
    # Clean and extract the content
    content = input_data.get("content", "").strip()
    # Extract the first sentence for the name
    name ="\n".join(content.splitlines()[:3]).strip()
    # Generate the summary using the first three lines
    summary = content.split(".")[0].strip() + "." if "." in content else content.strip()

    output_data = {
        "content": content,
        "summary": summary,
        "name": name,
        "url": input_data.get("url", "").strip(),
    }
    return output_data

# Example usage:

input_text = {"title": "\n\t\t\t\t\t", "content": "\n\n\t\n\n\t\t\n\n\t\t\n\t\n\n\t\nCover of the 2001 revised edition, with art by the Brothers Hildebrandt\n\nThe Complete Guide to Middle-earth\n\n\t\n\t\t\nAuthor\n\n\t\n\t\nRobert Foster\n\n\t\n\t\t\nPages\n\n\t\n\t\n573\n\n\t\n\t\t\nMedia type(s)\n\n\t\n\t\nPaperback\n\n\t\n\t\t\nReleased\n\n\t\n\t\n1978, 2001,\n2022\n\n\t\n\t\t\nPublisher\n\n\t\n\t\nBallantine Books\n,\nRandom House Publishing\n\n\t\n\t\nISBN 0-345-44976-2\n\nThe Complete Guide to Middle-earth: The Definitive Guide to the World of J.R.R. Tolkien\n is a reference book for the canon of \nMiddle-earth\n, compiled and written by \nRobert Foster\n, and now published by \nRandom House Publishing Group\n.\n\nOriginally released soon after the publication of \nThe Silmarillion\n, this book is generally recognised as an excellent reference book on the subject. However, as it excludes information on post-Silmarillion material (e.g., \nUnfinished Tales\n and the \nThe History of Middle-earth\n series\n), there a few errors.\n\nEditions\n[\n]\nThe book was first published as \nA Guide to Middle-earth\n in 1971, with paperback being released in 1973. In 1978, the title was emended to \nThe Complete Guide to Middle-earth: from The Hobbit to The Silmarillion. \nA revised edition was published by Del Rey in 2001, as well as an illustrated edition in 2003, in time for \nThe Lord of the Rings\n film trilogy\n.\n\nA 2022 edition was later released, with art by \nTed Nasmith\n.\n\nSee also\n[\n]\nA Companion to J.R.R. Tolkien\n\nTolkien's World: Paintings of Middle-earth\n\nA Middle-earth Traveler: Sketches from Bag End to Mordor\n", "url": "https://lotr.fandom.com/wiki/The_Complete_Guide_to_Middle-earth"}
# Replace `input_text` with your actual JSON input when you paste it.
transformed_data = transform_data(input_text)

# Pretty print the output
print(json.dumps(transformed_data, indent=4))
