import sys
import subprocess
import os

operating_system = 'windows'

# Get the operating system argument
if len(sys.argv) < 3 or sys.argv[1] != '-o':
    print("Usage: python script.py -o <operating system>")
    sys.exit(1)
   
# Get the current directory
current_directory = os.getcwd()

operating_system = sys.argv[2]

# Execute the appropriate batch file based on the operating system
if operating_system.lower() == 'windows':
    # Construct the path to the batch file
    batch_file_path = os.path.join(current_directory, 'build', 'vc15-x86_64', 'make-solutions.bat')  
    subprocess.run([batch_file_path], shell=True)
    subprocess.run(['cmake', '--build', '.'], shell=True)
elif operating_system.lower() == 'linux':
    # Construct the path to the batch file
    batch_file_path = os.path.join(current_directory, 'build', 'linux', 'make-Makefiles.bash')
    subprocess.run([batch_file_path], shell=True)
else:
    print("Invalid operating system argument.")
    sys.exit(1)
