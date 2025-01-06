import re
import json

def reformat_json_string(input_string):
    # Remove excessive whitespace, tabs, and newline characters
    cleaned_string = re.sub(r"[\n\t]+", " ", input_string)
    # Replace multiple spaces with a single space
    cleaned_string = re.sub(r" +", " ", cleaned_string)
    # Strip leading and trailing spaces
    cleaned_string = cleaned_string.strip()
    # Add a line break after every period followed by a space or end of the string
    formatted_string = re.sub(r"\. ", ".\n", cleaned_string)
    formatted_string = re.sub(r"\.$", ".\n", formatted_string)  # Ensure a final line break after the last period
    return formatted_string

def save_as_json(formatted_string, output_file):
    # Prepare the JSON structure
    formatted_data = {"content": formatted_string}
    # Write to JSON file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(formatted_data, file, indent=4, ensure_ascii=False)

# Example input
input_string = """
\n\n\t\n\n\t\t\n\n\t\t\n\t\n\n\t\nCover of the 2001 revised edition, with art by the Brothers Hildebrandt\n\nThe Complete Guide to Middle-earth\n\n\t\n\t\t\nAuthor\n\n\t\n\t\nRobert Foster\n\n\t\n\t\t\nPages\n\n\t\n\t\n573\n\n\t\n\t\t\nMedia type(s)\n\n\t\n\t\nPaperback\n\n\t\n\t\t\nReleased\n\n\t\n\t\n1978, 2001,\n2022\n\n\t\n\t\t\nPublisher\n\n\t\n\t\nBallantine Books\n,\nRandom House Publishing\n\n\t\n\t\nISBN 0-345-44976-2\n\nThe Complete Guide to Middle-earth: The Definitive Guide to the World of J.R.R. Tolkien\n is a reference book for the canon of \nMiddle-earth\n, compiled and written by \nRobert Foster\n, and now published by \nRandom House Publishing Group\n.\n\nOriginally released soon after the publication of \nThe Silmarillion\n, this book is generally recognised as an excellent reference book on the subject. However, as it excludes information on post-Silmarillion material (e.g., \nUnfinished Tales\n and the \nThe History of Middle-earth\n series\n), there a few errors.\n\nEditions\n[\n]\nThe book was first published as \nA Guide to Middle-earth\n in 1971, with paperback being released in 1973. In 1978, the title was emended to \nThe Complete Guide to Middle-earth: from The Hobbit to The Silmarillion. \nA revised edition was published by Del Rey in 2001, as well as an illustrated edition in 2003, in time for \nThe Lord of the Rings\n film trilogy\n.\n\nA 2022 edition was later released, with art by \nTed Nasmith\n.\n\nSee also\n[\n]\nA Companion to J.R.R. Tolkien\n\nTolkien's World: Paintings of Middle-earth\n\nA Middle-earth Traveler: Sketches from Bag End to Mordor\n"""

# Reformat the string
reformatted_string = reformat_json_string(input_string)

# Save the reformatted string as a JSON file
output_file_path = "formatted_output.json"
save_as_json(reformatted_string, output_file_path)

# Print a success message
print(f"Formatted JSON saved to {output_file_path}")
