import os, platform
import json
import requests

from lib.CatalogFetcher import decrypt_game_config, find_game_config
from lib.Il2CppInspectorDumper import Il2CppInspectorDumperCLI
from lib.FBSDumper import FbsDumperCLI

if __name__ == "__main__":
    # Setup paths
    os_system = platform.system()
    lib_dir = os.path.join(os.getcwd(), f'dump_lib')
    extract_dir = os.path.join(os.getcwd(), 'jp_extracted')
    data_dir = os.path.join(os.getcwd(), 'jp_data')
    libil2cpp_path = os.path.join(extract_dir, "config_arm64_v8a", "lib", "arm64-v8a", "libil2cpp.so")
    metadata_path = os.path.join(extract_dir, "BlueArchive_apk", "assets", "bin", "Data", "Managed", "Metadata", "global-metadata.dat")
    dummydll_dir = os.path.join(data_dir, "DummyDll")
    il2cpp_exec_path = os.path.join(lib_dir, "Il2CppInspector", "Il2CppInspector")
    fbsdumper_exec_path = os.path.join(lib_dir, "FbsDumper", "FbsDumper")
    if os_system == "Windows":
        il2cpp_exec_path = os.path.join(lib_dir, "Il2CppInspector", "Il2CppInspector.exe")
        fbsdumper_exec_path = os.path.join(lib_dir, "FbsDumper", "FbsDumper.exe")
    os.makedirs(data_dir, exist_ok=True)

    # Dump il2cpp data from the apk file & Generate fbs data
    Il2CppInspectorDumperCLI(il2cpp_exec_path).dump(libil2cpp_path, metadata_path, data_dir)
    FbsDumperCLI(fbsdumper_exec_path).dump(dummydll_dir, libil2cpp_path, data_dir)

    # Old fbs generator
    # dump_cs_path = os.path.join(dumped_dir, "dump.cs")
    # fbs_path = os.path.join(dumped_dir, "BlueArchive.fbs")
    # FBSGenerator(dump_cs_path, fbs_path).generate_fbs()

    # Get the game url
    config_url = decrypt_game_config(find_game_config(os.path.join(extract_dir, "UnityDataAssetPack", "assets", "bin", "Data")))
    output_file_path = os.path.join(data_dir, "config.json")

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

    print(f"Data has been moved to {data_dir}")