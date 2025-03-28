import os
from lib.CatalogFetcher import decrypt_game_config, find_game_config

if __name__ == "__main__":
    extract_dir = os.path.join(os.getcwd(), 'extracted')
    data = decrypt_game_config(find_game_config(os.path.join(extract_dir, "UnityDataAssetPack", "assets", "bin", "Data")))
    output_file_path = os.path.join(os.getcwd(), 'game_url.txt')
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(data)
    
    print(f"Game url has been written to {output_file_path}")
