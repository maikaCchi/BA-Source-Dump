import os

import lib.GlobalCatalogFetcher
import lib.CatalogFetcher

#lib.CatalogFetcher.decrypt_game_config(lib.CatalogFetcher.find_game_config(os.path.join("jp_extracted", "UnityDataAssetPack", "assets", "bin", "Data")))
lib.GlobalCatalogFetcher.decrypt_game_config(lib.GlobalCatalogFetcher.find_game_config(os.path.join("global_extracted", "BlueArchive_apk", "assets", "bin", "Data")))