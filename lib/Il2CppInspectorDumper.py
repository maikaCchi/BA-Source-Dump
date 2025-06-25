import subprocess
import os

class Il2CppInspectorDumperCLI:
    def __init__(self, executable_path):
        if not os.path.exists(executable_path):
            raise FileNotFoundError(f"Il2CppInspectorPro executable not found at: {executable_path}")
        self.executable_path = executable_path

    def dump(self, 
            library_file: str, 
            global_metadata: str, 
            output_base_directory: str
        ):
        # Create output directories
        os.makedirs(output_base_directory, exist_ok=True)
        
        command = [
            self.executable_path,
            "-i", library_file,
            "-m", global_metadata,
            "--select-outputs",
            "-c", os.path.join(output_base_directory, "dump.cs"),
            "-d", os.path.join(output_base_directory, "DummyDll"),
            "-k",
        ]

        print("Executing command:", " ".join(command))
        
        try:
            result = subprocess.run(command, 
                                    check=True, 
                                    capture_output=True, 
                                    text=True, 
                                    encoding='utf-8', 
                                    errors='replace',
                                    cwd=output_base_directory)

            print("\nIl2CppInspectorPro output (stdout):")
            print(result.stdout)
            
            if result.stderr:
                print("\nIl2CppInspectorPro errors (stderr):")
                print(result.stderr)
            
            print("\nIl2CppInspectorPro dumping process completed successfully.")

        except FileNotFoundError:
            print(f"Error: Il2CppInspectorPro executable or one of the specified input files was not found.")
            print(f"Please double-check paths: {self.executable_path}, {library_file}, {global_metadata}")

        except subprocess.CalledProcessError as e:
            print(f"\nError executing Il2CppInspectorPro (returned non-zero exit code {e.returncode}):")
            print(f"Command attempted: {' '.join(e.cmd)}")
            print(f"STDOUT:\n{e.stdout}")
            print(f"STDERR:\n{e.stderr}")
            print("\nIl2CppInspectorPro likely encountered an issue. Check the output above for details.")
            print("Common issues: Incorrect Unity version, corrupted binary/metadata, invalid paths.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")