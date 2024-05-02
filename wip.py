
import os
import argparse
import subprocess
from blessed import Terminal
from PIL import Image
import xml.etree.ElementTree as ET

def parse_xmp_metadata(xmp_data):
    namespaces = {
        'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'dc': "http://purl.org/dc/elements/1.1/",
        'xmp': "http://ns.adobe.com/xap/1.0/",
        'exif': "http://ns.adobe.com/exif/1.0/"
    }
    root = ET.fromstring(xmp_data)
    description_path = "./rdf:RDF/rdf:Description/dc:description/rdf:Alt/rdf:li"
    description = root.find(description_path, namespaces)
    cleaned_data = {}
    if description is not None:
        details = description.text.strip()
        steps_index = details.find("Steps")
        if steps_index != -1:
            cleaned_data['Prompt'] = details[:steps_index].strip()
            remaining_details = details[steps_index:]
            entries = remaining_details.split(', ')
            for entry in entries:
                if ': ' in entry:
                    key, value = entry.split(': ', 1)
                    cleaned_data[key.strip()] = value.strip()
    return cleaned_data

def draw_status_bar(term):
    status_text = "Enter :help for help, y to yank, q to quit."
    with term.location(0, term.height - 1):
        print(term.on_dodgerblue4(term.yellow(status_text + term.clear_eol)))


def wrap_text(text, width):
    """Wrap text to the specified width."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        if sum(len(w) for w in current_line) + len(word) + len(current_line) > width:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def display_image_and_metadata(image_path, term, file_tree_height, messages):
    y_offset = term.height // 2 - 2  # Adjust the position to avoid status bar overlap
    cmd = f"kitty +kitten icat --place {term.width//2}x{file_tree_height}@0x{y_offset} '{image_path}'"
    subprocess.run(cmd, shell=True)

    with Image.open(image_path) as img:
        xmp_data = img.info.get('XML:com.adobe.xmp')
        if xmp_data:
            metadata = parse_xmp_metadata(xmp_data)
            start_y = 1  # Start displaying metadata at the top right of the screen
            for key, value in metadata.items():
                wrapped_text = wrap_text(f"{key}: {value}", term.width // 2 - 2)  # Assuming right half is for metadata
                for line in wrapped_text:
                    print(term.move_xy(term.width // 2 + 1, start_y) + line)
                    start_y += 1
        else:
            print(term.move_xy(term.width // 2 + 1, 1) + "No XMP metadata found.")


def choose_file(startpath, term):
    current_path = os.path.abspath(startpath)
    selection = 0
    messages = {
        "00001.png": "this is the image of a cat.",
        "image2.png": "Message for Image 2",
        # Add more messages for each image as needed
    }

    while True:
        try:
            entries = [e for e in os.listdir(current_path) if e.lower().endswith('.png') or os.path.isdir(os.path.join(current_path, e))]
            entries.sort(key=lambda e: (not os.path.isdir(os.path.join(current_path, e)), e.lower()))

            if current_path != os.path.abspath(startpath):
                entries.insert(0, '../')

            with term.cbreak(), term.hidden_cursor():
                print(term.home + term.clear)
                for i, entry in enumerate(entries):
                    if i == selection:
                        print(term.reverse(entry))
                    else:
                        print(entry)

                # Display image and metadata if a .png file is selected
                selected_path = os.path.join(current_path, entries[selection])
                if selected_path.lower().endswith('.png'):
                    display_image_and_metadata(selected_path, term, term.height // 2, messages)
                    filename = os.path.basename(selected_path)
                    message = messages.get(filename, "No message found for this image.")
                    print(term.move_xy(term.width // 2 + 1, term.height // 2) + message)
                else:
                    print(term.move_xy(term.width // 2 + 1, term.height // 2) + "Select a file to view details.")

                draw_status_bar(term)
                
                key = term.inkey()
                if key.lower() == 'q':
                    print(term.clear)
                    return
                elif key.code == term.KEY_UP and selection > 0:
                    selection -= 1
                elif key.code == term.KEY_DOWN and selection < len(entries) - 1:
                    selection += 1
                elif key.code == term.KEY_ENTER:
                    if entries[selection] == '../':
                        current_path = os.path.dirname(current_path)
                        selection = 0
                    elif os.path.isdir(selected_path):
                        current_path = selected_path
                        entries = [e for e in os.listdir(current_path) if e.lower().endswith('.png') or os.path.isdir(os.path.join(current_path, e))]
                        entries.sort(key=lambda e: (not os.path.isdir(os.path.join(current_path, e)), e.lower()))
                        selection = 0

        except Exception as e:
            print(f"An error occurred: {e}")
            return  # Exit on error

def main():
    term = Terminal()
    parser = argparse.ArgumentParser(description='Display image metadata with Blessed and navigate with keys.')
    args = parser.parse_args()

    start_directory = '.'  # Start directory for the file browser
    choose_file(start_directory, term)

if __name__ == '__main__':
    main()
