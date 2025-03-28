import subprocess
import os

class Il2CppDumperCLI:
    def __init__(self, executable_path):
        if not os.path.exists(executable_path):
            raise FileNotFoundError(f"{executable_path} does not exist")
        self.executable_path = executable_path

    def dump(self, library_file, global_metadata, output_directory):
        os.makedirs(output_directory, exist_ok=True)
        
        command = [
            self.executable_path,
            library_file,
            global_metadata,
            output_directory
        ]
        
        print("Executing command:", " ".join(command))
        
        try:
            result = subprocess.run(command, input="a", check=True, capture_output=True, text=True)
            print("il2cppdumper output:")
            print(result.stdout)
            if result.stderr:
                print("il2cppdumper errors:")
                print(result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error executing il2cppdumper: {e.stderr}")
            print(f"This may not exit properly, but hopefully the program dumped correctly")
