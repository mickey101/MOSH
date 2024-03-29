import sys
import shlex
import os
from mosh.constants import *
from mosh.builtins import *

# Hash map to store built-in function name and reference as key and value
built_in_cmds = {}

def tokenize(string):
	return shlex.split(string)

def execute(cmd_tokens):
	# Extract command name and arguments from tokens
    cmd_name = cmd_tokens[0]
    cmd_args = cmd_tokens[1: ]

    # If the command is a built-in command, invoke its function with arguments
    if cmd_name in built_in_cmds:
        return built_in_cmds[cmd_name](cmd_args)

    pid = os.fork()

    if pid == 0:
    # Child process
        # Replace the child shell process with the program called with exec
        os.execvp(cmd_tokens[0], cmd_tokens)
    elif pid > 0:
    # Parent process
        while True:
            # Wait response status from its child process (identified with pid)
            wpid, status = os.waitpid(pid, 0)

            # Finish waiting if its child process exits normally
            # or is terminated by a signal
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break

    # Return status indicating to wait for next command in shell_loop
    return SHELL_STATUS_RUN

def shell_loop():
	#start loop here
	status = SHELL_STATUS_RUN

	while status == SHELL_STATUS_RUN:
		#display a command prompt 
		sys.stdout.write('Mickey_needs_some_data!->')
		sys.stdout.flush()

		#Read command input
		cmd = sys.stdin.readline()

		#Tokenize the command input 
		cmd_tokens = tokenize(cmd)

		#Execute the command and retrieve new status
		status = execute(cmd_tokens)

# Register a built-in function to built-in command hash map
def register_command(name, func):
    built_in_cmds[name] = func

# Register all built-in commands here
def init():
    register_command("cd", cd)
    register_command("exit", exit)

def main():
    # Init shell before starting the main loop
    init()
    shell_loop()

if __name__ == "__main__":
	main()
