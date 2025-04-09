import re
import requests

from requests_cache import CachedSession

PLAYSTORE_URL = "https://play.google.com/store/apps/details?id=com.nexon.bluearchive&hl=in&gl=US"
API_URL = "https://api-patch.nexon.com/patch/v1.1/version-check"


def get_game_version() -> str:
    version_pattern = re.compile(r"\d{1}\.\d{2}\.\d{6}")
    response = requests.get(PLAYSTORE_URL)
    version_match = version_pattern.search(response.text)
    if not version_match:
        raise ValueError("Could not find game version in Play Store page")
    return version_match.group()

def catalog_url() -> str:
    version = get_game_version()
    build_number = version.split('.')[-1]

    with CachedSession('nexonapi', use_temp=True) as session:
        response = session.post(
            API_URL,
            json={
                "market_game_id": "com.nexon.bluearchive",
                "market_code": "playstore",
                "curr_build_version": version,
                "curr_build_number": build_number
            }
        )
        data = response.json()
        return data
        # return data['patch']['resource_path']

# def find_game_config(game_path) -> None | bytes:

#     pattern = bytes([
# 	    0x47,
#         0x61,
#         0x6D,
#         0x65,
#         0x4D,
#         0x61,
#         0x69,
#         0x6E,
#         0x43,
#         0x6F,
#         0x6E,
#         0x66,
# 	    0x69,
#         0x67,
#         0x00,
#         0x00
#     ])

#     for config_file in Path(game_path).rglob('*'):
#         if config_file.is_file():
#             content = config_file.read_bytes()

#             if pattern in content:
#                 # print(config_file)
#                 start_index = content.index(pattern)
#                 data = content[start_index + len(pattern) :]
#                 return data[:-2]
#     return None


# def decrypt_game_config(data: bytes) -> str:
#     encryption_service = TableEncryptionService()
#     encoded_data = b64encode(data)
    
#     print(encoded_data) # this is the data you asked
#     game_config = encryption_service.create_key('GameMainConfig')
#     server_data = encryption_service.create_key('ServerInfoDataUrl')
    
#     decrypted_data = encryption_service.convert_string(encoded_data, game_config)
#     # print(decrypted_data)
#     loaded_data = json.loads(decrypted_data)

#     decrypted_key = encryption_service.new_encrypt_string('ServerInfoDataUrl', server_data)
#     decrypted_value = loaded_data[decrypted_key]
#     return encryption_service.convert_string(decrypted_value, server_data)