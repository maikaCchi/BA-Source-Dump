import subprocess
import os

class FbsDumperCLI:
    def __init__(self, executable_path):
        if not os.path.exists(executable_path):
            raise FileNotFoundError(f"{executable_path} does not exist")
        self.executable_path = executable_path

    def dump(self, dummydll_dir, library_file, output_directory, 
            output_file_name="BlueArchive.fbs",
            custom_namespace=None, 
            force_snake_case=False, 
            namespace_to_look_for=None):
        
        full_output_file_path = os.path.join(output_directory, output_file_name)
        os.makedirs(output_directory, exist_ok=True)

        command = [
            self.executable_path,
            "-d", dummydll_dir,
            "-l", library_file,
            "-o", full_output_file_path
        ]

        if custom_namespace is not None:
            command.extend(["-n", custom_namespace])
        if force_snake_case:
            command.append("-s")
        if namespace_to_look_for is not None:
            command.extend(["-nl", namespace_to_look_for])
        
        print("Executing command:", " ".join(command))
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("fbsdumper output:")
            print(result.stdout)
            if result.stderr:
                print("fbsdumper errors:")
                print(result.stderr)
            print(f"Successfully dumped to: {full_output_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing fbsdumper (exit code {e.returncode}):")
            if e.stdout:
                print("fbsdumper stdout:")
                print(e.stdout)
            if e.stderr:
                print("fbsdumper stderr:")
                print(e.stderr)
            print(f"Dump failed. Check the errors above.")
        except FileNotFoundError:
            print(f"Error: The executable '{self.executable_path}' was not found. Check the path.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

