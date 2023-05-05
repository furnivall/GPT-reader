# Simple ChatGPT Terminal Client

This repository contains a simple terminal-based client for having conversations with OpenAI's ChatGPT, written in Python. It provides an easy-to-use interface to interact with different models like GPT-4, GPT-4-32K, and GPT-3.5-turbo.

## Features

- Terminal-based user interface
- Easily switch between different models
- Clear and concise conversation history display
- Supports arrow key and delete key input handling
- Provides a spinner animation during API request processing

## Installation

1. Clone the repository:
`git clone https://github.com/furnivall/GPT-reader.git`

2. Install the required dependencies:
`pip install -r requirements.txt`

3. Set up your OpenAI API key:
`export OPENAPI_KEY="your_openai_api_key"` in bash - use your own shell's guide to setting up an environment variable.


## Usage

Run the terminal client:
`python pyRequest.py`


- Enter your message and press Enter to send it to ChatGPT.
- To change the model, prepend your message with `(g4)`, `(g4-32)`, or `(g3)`.
- Type `exit` to quit the application.
- Type `new` to start a new conversation.

## Dependencies

- Python 3.x
- openai
- textwrap
- readchar
- threading
- time
- colorama
- shutil

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

