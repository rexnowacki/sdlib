
import os
import re
import argparse
import subprocess
from blessed import Terminal


def list_directory(path):
    # List directory contents, filtering by .png files and directories
    entries = [e for e in os.listdir(path) if e.lower().endswith('.png') or os.path.isdir(os.path.join(path, e))]

    # Sort entries: directories first, then files by alphabetic and numeric order
    entries.sort(key=lambda x: (os.path.isdir(os.path.join(path, x)), alphanumeric_key(x)))
    return entries

def alphanumeric_key(input_str):
    """
    Split the input string into a list of integers and non-integer substrings,
    which provides a natural sorting key.
    """
    # Split the string into numeric and non-numeric parts
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    return [convert(c) for c in re.split('([0-9]+)', input_str)]

def display_image(image_path, term, file_tree_height):
    offset_y = term.height // 2 + 1
    offset_x = 0
    height = term.height // 2 - 2
    width = term.width // 2
    cmd = f"kitty +kitten icat --place {width}x{height}@{offset_x}x{offset_y} '{image_path}'"
    subprocess.run(cmd, shell=True)

def choose_file(startpath, term):
    current_path = startpath
    selection = 0

    messages = {
        "00001.png": "this is the image of a cat.",
        "image2.png": "Message for Image 2",
        # Add more messages for each image as needed
    }

    entries = list_directory(current_path)

    with term.cbreak(), term.hidden_cursor():
        while True:
            print(term.home + term.clear)

            # Draw file tree in the NW
            file_tree_height = term.height // 2 - 1
            for i, entry in enumerate(entries[:file_tree_height]):
                if i == selection:
                    print(term.reverse(entry))
                else:
                    print(entry)

            # Display image in the SW
            image_path = os.path.join(current_path, entries[selection])
            if image_path.lower().endswith('.png'):
                display_image(image_path, term, file_tree_height)

            # Draw message panel in the NE
            filename = os.path.basename(entries[selection])
            message = messages.get(filename, "No message found for this image.")
            message_lines = message.split('\n')
            for i, line in enumerate(message_lines):
                print(term.move_xy(term.width // 2 + 1, i + 1) + line)

            key = term.inkey()
            if key.lower() == 'q':
                print(term.clear) # Clear screen when quitting
                return
            elif key.code == term.KEY_UP and selection > 0:
                selection -= 1
            elif key.code == term.KEY_DOWN and selection < len(entries) - 1:
                selection += 1
            elif key.code == term.KEY_ENTER:
                selected_path = os.path.join(current_path, entries[selection])
                if os.path.isdir(selected_path):
                    current_path = selected_path
                    entries = list_directory(current_path)
                    selection = 0

def main():
    term = Terminal()
    parser = argparse.ArgumentParser(description='Display image metadata with Blessed and navigate with keys.')
    args = parser.parse_args()

    start_directory = '.'  # start directory for the file browser
    choose_file(start_directory, term)

if __name__ == '__main__':
    main()
