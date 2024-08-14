import os
import sys

def restart_program():
    try:
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"Error restarting program: {e.__class__.__name__}, {e}")