import os, platform
import json
import requests

from lib.CatalogFetcher import decrypt_game_config, find_game_config
from lib.Il2cppDumper import Il2CppDumperCLI
from lib.FBSGenerator import FBSGenerator

if __name__ == "__main__":
    extract_dir = os.path.join(os.getcwd(), 'extracted')
    dumped_dir = os.path.join(os.getcwd(), "dumped")
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
    config_url = decrypt_game_config(find_game_config(os.path.join(extract_dir, "UnityDataAssetPack", "assets", "bin", "Data")))
    output_file_path = os.path.join(os.getcwd(), 'config.json')

    # Request the data from config and save to the disk
    try:
        response = requests.get(config_url)
        response.raise_for_status()
        config_data = response.json()

        config_data["ServerInfoDataUrl"] = config_url

        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(config_data, file, indent=4, ensure_ascii=False)

        print(f"Config data has been written to {output_file_path}")

    except requests.RequestException as e:
        print(f"Error fetching config data: {e}")
