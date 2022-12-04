from requests import get
from os import makedirs, path
from handlers.unzipper_handler import Unzipper
from OtoPy.UsefulTools import OTimedProgressBar, OLogger

class GithubHandler():
    def __init__(self, settings):
        self.defaultFileSettings = settings.get("default_file_settings", {})
        self.repository = settings.get("repository", {})
        self.release = settings.get("release", {})
        self.files = settings.get("files", [])

        releaseSufix = self.release['sufix']

    def GetReleaseAssets(self):
        if not self.repository['owner'] or not self.repository['name']:
            return {"code": 1, "error_message": "Repository settings missing"}

        URL = f"https://api.github.com/repos/{self.repository['owner']}/{self.repository['name']}/releases/{self.release['version']}"
        HEADER = {"Accept": "application/vnd.github+json"}
        DOWNLOAD_HEADER = {"Accept": "application/octet-stream"}
        if self.repository['token']:
            HEADER["Authorization"] = f"token {self.repository['token']}"
            DOWNLOAD_HEADER["Authorization"] = f"token {self.repository['token']}"

        releaseData = get(URL, headers=HEADER).json()
        if releaseData.get("message"):
            return {"code": 2, "error_message": releaseData}

        releaseTagName = releaseData.get('tag_name')
        if not releaseTagName:
            return {"code": 3, "error_message": f"No {self.release['version']} Release Found"}

        releaseAssetsUrls = releaseData.get("assets_url")
        if not releaseAssetsUrls:
            return {"code": 4, "error_message": f"No Assets Found for {releaseData.get('tag_name')}"}

        assetsToDownload = list()
        allReleaseAssets = get(releaseAssetsUrls, headers=HEADER).json()

        if self.files:
            for file in self.files:
                for dictKey in set(self.defaultFileSettings):
                    file[dictKey] = self.defaultFileSettings.get(dictKey) | file.get(dictKey, {})

                fileSettings = file.get("file_settings", {})

                fileName = fileSettings['name'] if fileSettings.get("name") else releaseTagName
                fileNameWithExtension = f"{fileName}.{fileSettings['extension']}"

                for asset in allReleaseAssets:
                    if asset["name"] == fileNameWithExtension:
                        downloadDetails = {
                            "download_details":{
                                "file_name": fileNameWithExtension,
                                "url": asset["url"],
                                "header": DOWNLOAD_HEADER
                            }
                        }
                        assetsToDownload.append(file | downloadDetails)
                        break
        else: 
            for asset in allReleaseAssets:
                    downloadDetails = {
                        "download_details":{
                            "file_name": asset["name"],
                            "url": asset["url"],
                            "header": DOWNLOAD_HEADER
                        }
                    }
                    assetsToDownload.append(self.defaultFileSettings | downloadDetails)
                    
        return assetsToDownload

    def DownloadAsset(self, assetToDownload):
        downloadDetails = assetToDownload.get("download_details",{})
        fileSettings = assetToDownload.get("file_settings",{})
        unzipperSettings = assetToDownload.get("unzipper_settings",{})
        assetExistsPriorDownload = path.exists(f"{fileSettings['download_path']}{downloadDetails['file_name']}")
        assetIsZip = downloadDetails['file_name'].__contains__(".zip")
        chunkSize = 524288

        print("-----------------------------------------------------------------------------------------------------------------------")
        if fileSettings['overwrite_downloaded_files'] or not assetExistsPriorDownload:
            print(f"Downloading: {downloadDetails['file_name']} to: \"{fileSettings['download_path']}\"")
            streamFile = get(downloadDetails['url'], stream=True, headers=downloadDetails['header'])
            contentLength = streamFile.headers.get('content-length')
            donwloadProgress = OTimedProgressBar(completeState = int(contentLength))

            makedirs(fileSettings['download_path'], exist_ok=True)
            with open(f"{fileSettings['download_path']}{downloadDetails['file_name']}", "wb") as file:
                if not contentLength:
                    file.write(streamFile.content)
                else:
                    dataLenght = 0
                    for data in streamFile.iter_content(chunk_size=chunkSize):
                        dataLenght += len(data)
                        file.write(data)
                        donwloadProgress.PrintProgress(int(dataLenght))
        else: print(f"File {downloadDetails['file_name']} already exists, as directed in config will not be downloaded again.")

        if assetIsZip and fileSettings['unzip_file'] and (fileSettings['overwrite_downloaded_files'] or unzipperSettings['overwrite_unziped_files'] or not assetExistsPriorDownload):
            unzipper = Unzipper()
            unzipper.UnzipFile(assetToDownload)
        else: print(f"File {downloadDetails['file_name']} already exists, as directed in configs will not be unzipped again.")