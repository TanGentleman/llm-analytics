import re
from uuid import uuid4
import logging
import json
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('output.log', mode='a')  # Append mode
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class Configuration:
    def __init__(self, eval_batch_size, context_length, cpu_threads):
        self.eval_batch_size = eval_batch_size
        self.context_length = context_length
        self.cpu_threads = cpu_threads

def get_clipboard():
    from pyperclip import paste as py_paste # type: ignore
    clipboard_contents = py_paste()
    if not clipboard_contents:
        print("No text found in clipboard.")
        return None
    return clipboard_contents

def parse_config(input_string, cpu_threads):
    # pattern match on this string:
    # "prompt: "n_batch 1024\nn_ctx 10000"
    pattern = r"n_batch (\d+)\nn_ctx (\d+)"
    match = re.match(pattern, input_string)
    
    if match:
        eval_batch_size = int(match.group(1))
        context_length = int(match.group(2))
        return Configuration(eval_batch_size, context_length, cpu_threads)
    else:
        return None

def parse_output(config: Configuration, output_string):
    # pattern match on this string:
    # "time to first token: 0.58s gen t: 4.20s speed: 29.50 tok/s stop reason: completed gpu layers: 1 cpu threads: 8 mlock: true token count: 4699/8000"
    pattern = r"time to first token: (\d+\.\d+s) gen t: (\d+\.\d+s) speed: (\d+\.\d+) tok/s stop reason: completed gpu layers: \d+ cpu threads: (\d+) mlock: true token count: (\d+)/(\d+)"
    match = re.match(pattern, output_string)
    
    if match:
        time_to_first_token = float(match.group(1).replace('s', ''))
        gen_t = float(match.group(2).replace('s', ''))
        speed = float(match.group(3))
        cpu_threads = int(match.group(4))
        token_count = {
            "generated": int(match.group(5)),
            "total": int(match.group(6))
        }
        unique_id = str(uuid4())  # Generate a unique ID for the session
        configuration = config
        return {
            "unique_id": unique_id,
            "configuration": configuration.__dict__,
            "time_to_first_token": time_to_first_token,
            "gen_t": gen_t,
            "speed": speed,
            "cpu_threads": cpu_threads,
            "token_count": token_count
        }
    else:
        return None

def main():
    input_string = input("Enter the batch/context string: ")
    if input_string == "c":
        input_string = get_clipboard()
    cpu_string = input("Enter the cpu string: ")
    config = parse_config(input_string, cpu_string)
    if config is None:
        logger.error("Invalid input string")
        return
    output_string = input("Enter the output string: ")
    if output_string == "c":
        output_string = get_clipboard()
    output = parse_output(config, output_string)
    if output is None:
        logger.error("Invalid output string")
        return
    logger.info(json.dumps(output))

if __name__ == "__main__":
    main()