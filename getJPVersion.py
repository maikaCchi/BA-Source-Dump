import os, platform

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
    data = decrypt_game_config(find_game_config(os.path.join(extract_dir, "UnityDataAssetPack", "assets", "bin", "Data")))
    output_file_path = os.path.join(os.getcwd(), 'game_url.txt')
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(data)
    
    print(f"Game url has been written to {output_file_path}")
