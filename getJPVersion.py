import os, platform
import json
import requests

from lib.CatalogFetcher import decrypt_game_config, find_game_config
from lib.Il2cppDumper import Il2CppDumperCLI
from lib.FBSGenerator import FBSGenerator

if __name__ == "__main__":
    extract_dir = os.path.join(os.getcwd(), 'extracted')
    dumped_dir = os.path.join(os.getcwd(), 'dumped')
    data_dir = os.path.join(os.getcwd(), 'jp_data')
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
        config_data_res = response.json()

        config_data = {"ServerInfoDataUrl": config_url}
        config_data.update(config_data_res)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(config_data, file, indent=4, ensure_ascii=False)

        print(f"Config data has been written to {output_file_path}")
    except requests.RequestException as e:
        print(f"Error fetching config data: {e}")

    # Move config.json, dump.cs, BlueArchive.fbs to the data folder
    os.makedirs(data_dir, exist_ok=True)
    os.replace(dump_cs_path, os.path.join(data_dir, "dump.cs"))
    os.replace(fbs_path, os.path.join(data_dir, "BlueArchive.fbs"))
    os.replace(output_file_path, os.path.join(data_dir, "config.json"))

    print(f"Data has been moved to {data_dir}")