import os
import zipfile
import cloudscraper

class FileDownloader:
    def __init__(self, url, download_dir, filename):
        self.url = url
        self.download_dir = download_dir
        self.filename = filename
        self.local_filepath = os.path.join(self.download_dir, self.filename)
        os.makedirs(self.download_dir, exist_ok=True)
        self.scraper = cloudscraper.create_scraper()

    def download(self):
        """Downloads the file from the URL to the local filepath."""
        try:
            response = self.scraper.get(self.url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 8192

            with open(self.local_filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        # self.print_progress(downloaded, total_size)
            print(f"\nDownloaded {self.local_filepath}")
        except Exception as e:
            print(f"Error during download: {e}")

    def print_progress(self, downloaded, total_size):
        """Prints the download progress as a percentage along with downloaded and total sizes (in KB)."""
        if total_size > 0:
            percent = downloaded / total_size * 100
            print(
                f"\rDownloading: {percent:.2f}% complete ({downloaded/1024:.2f} KB / {total_size/1024:.2f} KB)",
                end=''
            )

class FileExtractor:
    def __init__(self, file_path, extract_dir):
        self.file_path = file_path
        self.extract_dir = extract_dir
        os.makedirs(self.extract_dir, exist_ok=True)

    def extract_xapk(self):
        """Extracts the XAPK (zip file) to the designated directory and then extracts specific APKs."""
        try:
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_dir)
            print(f"Extracted {self.file_path} to {self.extract_dir}")
        except Exception as e:
            print(f"Error extracting {self.file_path}: {e}")
            return
        
        apk_files = {
            'config.arm64_v8a.apk': os.path.join(self.extract_dir, 'config_arm64_v8a'),
            'com.YostarJP.BlueArchive.apk': os.path.join(self.extract_dir, 'BlueArchive_apk'),
            'UnityDataAssetPack.apk': os.path.join(self.extract_dir, 'UnityDataAssetPack')
        }
        for apk_name, dest_dir in apk_files.items():
            self.extract_apk(apk_name, dest_dir)
    
    def extract_il2cpp(self):
        """Extracts the il2cpp zip archive from the extraction directory to its own folder."""
        destination_dir = os.path.join(self.extract_dir, 'Il2CppDumper')
        os.makedirs(destination_dir, exist_ok=True)
        
        try:
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(destination_dir)
            print(f"Extracted {self.file_path} to {destination_dir}")
        except Exception as e:
            print(f"Error extracting {self.file_path}: {e}") 

    def extract_apk(self, apk_filename, destination_dir):
        """Extracts an APK file (which is a zip archive) to the specified destination directory."""
        apk_path = os.path.join(self.extract_dir, apk_filename)
        if os.path.exists(apk_path):
            os.makedirs(destination_dir, exist_ok=True)
            try:
                with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                    apk_zip.extractall(destination_dir)
                print(f"Extracted {apk_filename} to {destination_dir}")
            except Exception as e:
                print(f"Error extracting {apk_filename}: {e}")
        else:
            print(f"{apk_filename} not found in {self.extract_dir}")
