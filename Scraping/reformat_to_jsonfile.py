import json
from datetime import datetime

def transform_data(input_data):
    # Ensure input_data is a list
    if isinstance(input_data, list):
        transformed_data = []
        for item in input_data:
            # Check if item is a dictionary and process it
            if isinstance(item, dict):
                url = item.get("url", "").strip()

                # Skip if "Category:" is in the URL
                if "Category" in url:
                    continue

                content = item.get("content", "").strip()

                # Extract the name from the URL (last segment of the URL path)
                name = url.split("/")[-1].replace("_", " ").title()  # Extract and clean URL

                # Generate the summary using the first sentence
                summary = content.split(".")[0].strip() + "." if "." in content else content.strip()

                output_data = {
                    "content": content,
                    "summary": summary,
                    "name": name,
                    "url": url,
                }
                transformed_data.append(output_data)
        return transformed_data
    else:
        raise ValueError("Input data is not a list.")

def read_input_json(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        return json.load(file)

def save_as_json(output_data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

# Example usage:
input_file_path = "output_lotr_all.json"  # Input JSON file with "title", "content", and "url"
output_file_path = "transformed1_output.json"  # Output JSON file path

# Read the input data from the JSON file
input_data = read_input_json(input_file_path)

# Transform the data
transformed_data = transform_data(input_data)

# Save the transformed data to a new JSON file
save_as_json(transformed_data, output_file_path)

# Print a success message
print(f"Transformed JSON saved to {output_file_path}")
