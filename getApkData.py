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

    lib_dir = os.path.join(os.getcwd(), f'dump_lib')
    download_dir = os.path.join(os.getcwd(), f'apk_downloads')
    extract_dir = os.path.join(os.getcwd(), f'{region}_extracted')
    os_system = platform.system()

    if region == "global":
        pkg = "com.nexon.bluearchive"
    elif region == "chinese":
        pkg = "com.RoamingStar.bluearchive"
    else:
        pkg = "com.YostarJP.BlueArchive"

    # Download the required dumper
    il2cppInspectorProUrl = "https://github.com/ArkanDash/Il2CppInspectorRedux/releases/download/v1.0/Il2CppInspectorRedux.CLI-linux-x64.zip"
    if os_system == "Windows":
        il2cppInspectorProUrl = "https://github.com/ArkanDash/Il2CppInspectorRedux/releases/download/v1.0/Il2CppInspectorRedux.CLI-win-x64.zip"
    il2cppDownloader = FileDownloader(il2cppInspectorProUrl, lib_dir, "il2cppinspector.zip")
    il2cppDownloader.download()
    FileExtractor(il2cppDownloader.local_filepath, lib_dir, "").extract_il2cppData()

    il2cppInspectorPluginUrl = "https://github.com/djkaty/Il2CppInspectorPlugins/releases/latest/download/plugins.zip"
    il2cppPluginDownloader = FileDownloader(il2cppInspectorPluginUrl, lib_dir, "il2cppinspectorplugin.zip")
    il2cppPluginDownloader.download()
    FileExtractor(il2cppPluginDownloader.local_filepath, lib_dir, "").extract_il2cppPlugin()

    fbsDumperUrl = "https://github.com/ArkanDash/FbsDumperV2/releases/download/1.0.0/FbsDumper-net8-linux-x64.zip"
    if os_system == "Windows":
        fbsDumperUrl = "https://github.com/ArkanDash/FbsDumperV2/releases/download/1.0.0/FbsDumper-net8-win-x64.zip"
    fbsDumperDownload = FileDownloader(fbsDumperUrl, lib_dir, "fbsDumper.zip")
    fbsDumperDownload.download()
    FileExtractor(fbsDumperDownload.local_filepath, lib_dir, "").extract_fbsdumper()
    print("Successfully downloaded and extracted the required dumper")

    # Download and Extract the Game XAPK
    print(f"Downloading {region} APK...")
    xapk_url = f"https://d.apkpure.com/b/XAPK/{pkg}?version=latest"
    downloader = FileDownloader(xapk_url, download_dir, f"{pkg}.xapk")
    downloader.download()
    FileExtractor(downloader.local_filepath, extract_dir, region).extract_xapk()

    print("Successfully downloaded and extracted files")