
# MetaVista

MetaVista is a terminal-based application designed to read and display metadata from AI-generated images, specifically those created using Stable Diffusion. It integrates vim-like keybindings for intuitive navigation and interaction within a terminal environment, making it ideal for developers, data scientists, and AI art enthusiasts who are accustomed to keyboard-driven interfaces.

## Features

- **Vim-like Keybindings**: Navigate through the application using familiar vim commands.
- **Dual-Pane Left Panel**: Includes a file tree and an image preview pane for easy navigation and verification of image files.
- **Metadata Display**: Displays metadata relevant to Stable Diffusion outputs in a clean and organized format on the right panel.
- **Clipboard Support**: Allows users to easily yank (copy) metadata to the clipboard with a simple keystroke.
- **Responsive Design**: Adapts the layout dynamically to terminal size for optimal usability on various devices.
- **Enhanced Search Functionality**: Features integrated search with pattern matching for efficient file and metadata discovery.

## System Requirements

- **Operating Systems**: Compatible with Linux, MacOS, and Windows Subsystem for Linux (WSL).
- **Dependencies**: Requires Python 3.8 or newer and PIL (Python Imaging Library).

## Installation

To install MetaVista, run the following command in your terminal:

```bash
pip install metavista
```
This command will download and install MetaVista along with its dependencies. Ensure that Python and pip are correctly installed on your system before running the installation.

## Usage

After installation, you can run MetaVista from your terminal. Here are some basic commands to get you started:

- h, j, k, l - Navigation keys to move through the application.
- y - Yank (copy) metadata to the clipboard.
- / - Activate search functionality.
- For a detailed guide on all commands and keybindings, access the help section within the app by typing :help.

## Contributing

We welcome contributions from the community, whether it's in the form of bug reports, feature requests, or pull requests. Here's how you can contribute:

- Bug Reports and Feature Requests: Please use the GitHub Issues tab to report bugs or suggest features.
- Pull Requests: If you would like to contribute to the codebase, please fork the repository, make your changes, and submit a pull request.

## License

MetaVista is released under MIT License.

For more information on contributing to MetaVista, please read our CONTRIBUTING.md.
