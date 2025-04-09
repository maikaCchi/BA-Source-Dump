import os
import platform
import argparse

from lib.ApkDownloader import FileDownloader, FileExtractor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download & extract Blue Archive XAPK and Il2CppDumper"
    )
    parser.add_argument(
        "--region",
        choices=["global", "jp"],
        default="jp",
        help="Which region APK to download (default: jp)",
    )
    args = parser.parse_args()
    region = args.region

    download_dir = os.path.join(os.getcwd(), f'{region}_download')
    extract_dir = os.path.join(os.getcwd(), f'{region}_extracted')
    os_system = platform.system()

    if region == "global":
        pkg = "com.nexon.bluearchive"
    else:
        pkg = "com.YostarJP.BlueArchive"
    print(f"Downloading {region} APK...")

    xapk_url = f"https://d.apkpure.com/b/XAPK/{pkg}?version=latest"
    downloader = FileDownloader(xapk_url, download_dir, "BlueArchive.xapk")
    downloader.download()

    # Extract XAPK file
    extractor = FileExtractor(downloader.local_filepath, extract_dir, region)
    extractor.extract_xapk()

    # Download the il2cppdumper
    dumperUrl = "https://github.com/AndnixSH/Il2CppDumper/releases/download/v6.7.46/Il2CppDumper-net8-linux-x64-v6.7.46.zip"
    if os_system == "Windows":
        dumperUrl = "https://github.com/Perfare/Il2CppDumper/releases/download/v6.7.46/Il2CppDumper-net6-v6.7.46.zip"
    dumperDownload = FileDownloader(dumperUrl, download_dir, "il2cppDumper.zip")
    dumperDownload.download()

    # Extract il2cppdumper
    dumperExtract = FileExtractor(dumperDownload.local_filepath, extract_dir, "")
    dumperExtract.extract_il2cpp()

    print("Successfully downloaded and extracted files")