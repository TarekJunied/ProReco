import io
import re
import sys
import threading
import time
import queue
import globals
import pm4py
from contextlib import contextmanager
from utils import read_log
# Custom stream to capture stderr line by line


class QueueStream(io.IOBase):
    def __init__(self):
        self.queue = queue.Queue()

    def write(self, message):
        self.queue.put(message)
        return len(message)

# Context manager to redirect stderr to the QueueStream


@contextmanager
def capture_stderr_live(q_stream):
    old_stderr = sys.stderr
    sys.stderr = q_stream
    try:
        yield
    finally:
        sys.stderr = old_stderr


def noisy_function():
    for i in range(1, 101):
        print(f"\rLoading... {i}%", file=sys.stderr, end='')
        time.sleep(0.1)  # Simulate work


def progressed_read_log(log_path):
    # Run noisy_function in a separate thread
    def run_noisy_function():
        with capture_stderr_live(q_stream):
            read_log(log_path)

    # Initialize QueueStream

    global captured_stderr_output
    captured_std_err_output = ""

    # Initialize QueueStream
    q_stream = QueueStream()

    # Start the noisy function in a separate thread
    thread = threading.Thread(target=run_noisy_function)
    thread.start()

    # Process stderr output live from the queue
    try:
        while thread.is_alive():
            while not q_stream.queue.empty():
                stderr_line = q_stream.queue.get()
                # Append the captured line to the global variable
                captured_std_err_output += stderr_line
                progress_percentage = capture_progress_percent_from_progress_bar(
                    stderr_line)
                if progress_percentage != None:
                    globals.set_parse_percentage(log_path, progress_percentage)
    finally:
        thread.join()


def capture_progress_percent_from_progress_bar(s):
    # Regular expression to find a percentage
    match = re.search(r'(\d+)%', s)
    if match:
        # Extract and return the percentage number as an integer
        return int(match.group(1))
    else:
        # Return None or a default value if no percentage is found
        return None


if __name__ == "__main__":
    print("hi")
