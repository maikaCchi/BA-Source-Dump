import os, platform

from lib.ApkDownloader import FileDownloader, FileExtractor

if __name__ == "__main__":
    download_dir = os.path.join(os.getcwd(), 'download')
    extract_dir = os.path.join(os.getcwd(), 'extracted')
    os_system = platform.system()

    # Download the XAPK file
    url = 'https://d.apkpure.com/b/XAPK/com.YostarJP.BlueArchive?version=latest'
    downloader = FileDownloader(url, download_dir, "BlueArchive.xapk")
    downloader.download()

    # # Extract XAPK file
    extractor = FileExtractor(downloader.local_filepath, extract_dir)
    extractor.extract_xapk()

    # Download the il2cppdumper
    dumperUrl = "https://github.com/AndnixSH/Il2CppDumper/releases/download/v6.7.46/Il2CppDumper-net8-linux-x64-v6.7.46.zip"
    if os_system == "Windows":
        dumperUrl = "https://github.com/Perfare/Il2CppDumper/releases/download/v6.7.46/Il2CppDumper-net6-v6.7.46.zip"
    dumperDownload = FileDownloader(dumperUrl, download_dir, "il2cppDumper.zip")
    dumperDownload.download()

    # # Extract il2cppdumper
    dumperExtract = FileExtractor(dumperDownload.local_filepath, extract_dir)
    dumperExtract.extract_il2cpp()