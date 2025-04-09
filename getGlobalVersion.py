import os, platform
import json
import requests

from lib.GlobalCatalogFetcher import catalog_url
from lib.Il2cppDumper import Il2CppDumperCLI
from lib.FBSGenerator import FBSGenerator

if __name__ == "__main__":
    extract_dir = os.path.join(os.getcwd(), 'global_extracted')
    dumped_dir = os.path.join(os.getcwd(), 'global_dumped')
    data_dir = os.path.join(os.getcwd(), 'global_data')
    os.makedirs(data_dir, exist_ok=True)
    os_system = platform.system()

    # Dump il2cpp data from the apk file
    exec_path = os.path.join(extract_dir, "Il2CppDumper", "Il2CppDumper")
    lib_path = os.path.join(extract_dir, "config_arm64_v8a", "lib", "arm64-v8a", "libil2cpp.so")
    metadata_path = os.path.join(extract_dir, "BlueArchive_apk", "assets", "bin", "Data", "Managed", "Metadata", "global-metadata.dat")
    if os_system == "Windows":
        exec_path = os.path.join(extract_dir, "Il2CppDumper", "Il2CppDumper.exe")
    Il2CppDumperCLI(exec_path).dump(lib_path, metadata_path, dumped_dir)

    # Dump fbs data from dump.cs from il2cpp dumped apk
    dump_cs_path = os.path.join(dumped_dir, "dump.cs")
    fbs_path = os.path.join(dumped_dir, "BlueArchive.fbs")
    FBSGenerator(dump_cs_path, fbs_path).generate_fbs()

    # Get the game url
    config_data = catalog_url()
    config_file_path = os.path.join(data_dir, 'config.json')
    resources_file_path = os.path.join(data_dir, 'resources.json')
    

    # Request the data from config and save to the disk
    try:
        response = requests.get(config_data['patch']['resource_path'])
        response.raise_for_status()
        resources_data = response.json()

        with open(config_file_path, 'w', encoding='utf-8') as file:
            json.dump(config_data, file, indent=4, ensure_ascii=False)
        with open(resources_file_path, 'w', encoding='utf-8') as file:
            json.dump(resources_data, file, indent=4, ensure_ascii=False)

        print(f"Config data has been written to {config_file_path}")
        print(f"Resources data has been written to {resources_file_path}")
    except requests.RequestException as e:
        print(f"Error fetching config data: {e}")

    # Move dump.cs and BlueArchive.fbs to the data folder
    os.replace(dump_cs_path, os.path.join(data_dir, "dump.cs"))
    os.replace(fbs_path, os.path.join(data_dir, "BlueArchive.fbs"))

    print(f"Data has been moved to {data_dir}")