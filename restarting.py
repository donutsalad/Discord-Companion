import os
import sys
import conlog

def restart_program():
    try:
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        conlog.log_restart(f"Error restarting program: {e.__class__.__name__}, {e}")