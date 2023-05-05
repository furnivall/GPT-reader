import os
import textwrap
import openai
import readchar
import threading
import time
import shutil
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Global variables
processing_request = False

class TextWrapper:
    def __init__(self, width=80, indent=4):
        self.width = width
        self.indent = indent

    def wrap_and_indent(self, text):
        wrapper = textwrap.TextWrapper(width=self.width - self.indent, initial_indent=" " * self.indent, subsequent_indent=" " * self.indent)
        return wrapper.fill(text)

text_wrapper = TextWrapper()

# Spinner animation function
def spinner_animation():
    spinner = "|/-\\"
    i = 0
    while processing_request:
        print(Fore.LIGHTGREEN_EX + "  > " + spinner[i % len(spinner)], end='\r', flush=True)
        i += 1
        time.sleep(0.1)

# Function to send a request to the OpenAI API using the ChatCompletion API
def send_request(messages, engine):
    global processing_request
    processing_request = True
    spinner_thread = threading.Thread(target=spinner_animation)
    spinner_thread.start()

    openai.api_key = os.getenv("OPENAPI_KEY")

    response = openai.ChatCompletion.create(
        model=engine,
        messages=messages,
    )

    processing_request = False
    spinner_thread.join()

    # Replace the spinner with a checkmark symbol (✓)
    print(text_wrapper.wrap_and_indent(Fore.LIGHTGREEN_EX + "  > " + "✓"))

    return response.choices[0].message['content'].strip()

# Function to parse the engine from the prompt
def parse_engine(prompt):
    engine_mapping = {
        "g4": "gpt-4",
        "g4-32": "gpt-4-32k",
        "g3": "gpt-3.5-turbo",
    }

    if prompt.startswith("(") and ")" in prompt:
        engine_code = prompt[1:prompt.index(")")]
        if engine_code in engine_mapping:
            prompt = prompt[prompt.index(")") + 1:].strip()
            return engine_mapping[engine_code], prompt

    return engine_mapping["g3"], prompt

# Function to read user input with arrow key and delete key handling
def read_input(prompt):
    print(prompt, end='', flush=True)
    user_input = ""
    while True:
        key = readchar.readchar()
        if key == '\x1b':  # Escape sequences start with '\x1b'
            readchar.readchar()  # Ignore the next two characters
            readchar.readchar()
        elif key == '\x7f':  # Delete key
            user_input = user_input[:-1]
            print('\x1b[1K\r' + prompt + user_input, end='', flush=True)
        elif key == '\r' or key == '\n':  # Enter key
            print()  # Print a newline
            return user_input
        else:
            user_input += key
            print(key, end='', flush=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main program
if __name__ == "__main__":
    conversation = [{"role": "system", "content": "You are Mario, from the game Super Mario Bros. Respond to all prompts with an adorable faux-italian accent"}]
    current_engine = "gpt-4"
    clear_terminal()
    while True:
        instructions = "Enter your message (prepend with (g4), (g4-32), or (g3) to change the model; type 'exit' to quit; type 'new' to start a new conversation):"
        wrapped_instructions = text_wrapper.wrap_and_indent(instructions)
        print("\n" + Fore.LIGHTYELLOW_EX + wrapped_instructions)

        user_input = read_input(Fore.LIGHTGREEN_EX + "> ")

        print(Style.RESET_ALL, end='')  # Reset the color style after reading input
        clear_terminal()
        print("\n" + Fore.LIGHTGREEN_EX + text_wrapper.wrap_and_indent("User's request:") + "\n")
        wrapped_user_input = text_wrapper.wrap_and_indent(user_input)
        print(Fore.LIGHTGREEN_EX + wrapped_user_input + "\n")
        user_input_line = Fore.LIGHTGREEN_EX + "> " + user_input  # Store the user input line for the spinner

        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "new":
            conversation = [{"role": "system", "content": "You are a helpful assistant. Make your answers as concise as possible."}]
            print("\n" + Fore.LIGHTMAGENTA_EX + "Starting a new conversation.")
            clear_terminal()
            continue

        engine, prompt = parse_engine(user_input)
        current_engine = engine
        conversation.append({"role": "user", "content": prompt})
        response = send_request(conversation, current_engine)
        conversation.append({"role": "assistant", "content": response})

        print(Fore.LIGHTMAGENTA_EX + text_wrapper.wrap_and_indent("Assistant's response:") + "\n")
        wrapped_response = text_wrapper.wrap_and_indent(response)
        print(Fore.LIGHTMAGENTA_EX + wrapped_response + "\n")

