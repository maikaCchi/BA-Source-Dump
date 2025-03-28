import os, platform

from lib.ApkDownloader import FileDownloader, FileExtractor
from lib.Il2cppDumper import Il2CppDumperCLI
from lib.FBSGenerator import FBSGenerator

if __name__ == "__main__":
    download_dir = os.path.join(os.getcwd(), 'download')
    extract_dir = os.path.join(os.getcwd(), 'extracted')
    dumped_dir = os.path.join(os.getcwd(), "dumped")
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
