import subprocess

# Path to Blender executable
blender_executable = "/path/to/blender"

# Path to the Python script to run within Blender
blender_script = "/path/to/blender_script.py"

# Additional arguments to pass to the Blender script
additional_args = ["--", "arg1", "arg2"]

# Construct the command
command = [blender_executable, "-b", "-P", blender_script] + additional_args

# Run the command
subprocess.run(command)
