import sys
import os

# Add the current directory to sys.path so we can import casio_gpt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from casio_gpt.app import main

if __name__ == "__main__":
    main()
