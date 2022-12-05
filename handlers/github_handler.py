from requests import get
from os import makedirs, path, remove
from handlers.unzipper_handler import Unzipper
from OtoPy.UsefulTools import OTimedProgressBar
from handlers.tools_handler import WaitKeyToClose, CompareTwoDicts

class GithubHandler():
    def __init__(self, settings):
        self.defaultFileSettings = settings.get("default_file_settings", {})
        self.repository = settings.get("repository", {})
        self.release = settings.get("release", {})
        self.files = settings.get("files", [])

    def GetReleaseAssets(self):
        if not self.repository['owner'] or not self.repository['name']:
            return {"code": 1, "error_message": "Repository settings missing"}

        URL = f"https://api.github.com/repos/{self.repository['owner']}/{self.repository['name']}/releases"
        HEADER = {"Accept": "application/vnd.github+json"}
        DOWNLOAD_HEADER = {"Accept": "application/octet-stream"}
        if self.repository['token']:
            HEADER["Authorization"] = f"token {self.repository['token']}"
            DOWNLOAD_HEADER["Authorization"] = f"token {self.repository['token']}"

        releasesData = get(URL, headers=HEADER).json()
        if type(releasesData) != list:
            return {"code": 2, "error_message": releasesData}
        for release in releasesData:
            if self.release.get("pre-release_identifier"):
                if self.release.get("pre-release_identifier") in release["tag_name"]:
                    releaseData = release
                    break
            elif release["tag_name"][-1].isdigit() and not "alpha" in release["tag_name"] and not "beta" in release["tag_name"] and not "pre-release" in release["tag_name"]:
                    releaseData = release
                    break
            else: releaseData = {}

        releaseTagName = releaseData.get('tag_name')
        if not releaseTagName:
            return {"code": 3, "error_message": f"No Release Found"}

        releaseAssetsUrls = releaseData.get("assets_url")
        if not releaseAssetsUrls:
            return {"code": 4, "error_message": f"No Assets Found for {releaseData.get('tag_name')}"}

        assetsToDownload = list()
        allReleaseAssets = get(releaseAssetsUrls, headers=HEADER).json()

        if self.files:
            for file in self.files:
                #Normalize settings from file adding any missing details
                file = CompareTwoDicts(self.defaultFileSettings, file)

                fileSettings = file.get("file_settings", {})
                fileNameWithExtension = f"{fileSettings['name'] if fileSettings.get('name') else releaseTagName}.{fileSettings['extension']}"
                    
                for asset in allReleaseAssets:
                    if fileSettings['contains_in_name']:
                        assetContainsDinamicName = (
                                (fileSettings['contains_in_name'] in asset["name"] if fileSettings['contains_in_name'] != True else releaseTagName in asset["name"])
                                and fileSettings['extension'] == asset["name"][-len(fileSettings['extension']):]
                            )
                        fileNameWithExtension = asset["name"]
                    else: assetContainsDinamicName = False

                    if (asset["name"] == fileNameWithExtension or assetContainsDinamicName):
                        downloadDetails = {
                            "download_details":{
                                "release_name": releaseData.get('tag_name'),
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
                            "release_name": releaseData.get('tag_name'),
                            "file_name": asset["name"],
                            "url": asset["url"],
                            "header": DOWNLOAD_HEADER
                        }
                    }
                    assetsToDownload.append(self.defaultFileSettings | downloadDetails)
                    
        if not assetsToDownload:
            return {"code": 5, "error_message": f"No Assets Found for {releaseData.get('tag_name')} with the configured settings"}
        return assetsToDownload

    def DownloadAsset(self, assetToDownload):
        downloadDetails = assetToDownload.get("download_details",{})
        fileSettings = assetToDownload.get("file_settings",{})
        unzipperSettings = assetToDownload.get("unzipper_settings",{})
        assetExistsPriorDownload = path.exists(f"{fileSettings['download_path']}{downloadDetails['file_name']}")
        assetIsZip = downloadDetails['file_name'].__contains__(".zip")
        chunkSize = 524288

        print("╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍")
        if fileSettings['overwrite_downloaded_files'] or not assetExistsPriorDownload:
            print(f"Downloading: {downloadDetails['file_name']} to: \"{fileSettings['download_path']}\".")
            streamFile = get(downloadDetails['url'], stream=True, headers=downloadDetails['header'])
            contentLength = streamFile.headers.get('content-length')
            donwloadProgress = OTimedProgressBar(completeState = int(contentLength), fill='❚', suffix="Downloaded")
            makedirs(fileSettings['download_path'], exist_ok=True)

            try:
                with open(f"{fileSettings['download_path']}{downloadDetails['file_name']}", "wb") as file:
                    if not contentLength:
                        file.write(streamFile.content)
                    else:
                        dataLenght = 0
                        for data in streamFile.iter_content(chunk_size=chunkSize):
                            dataLenght += len(data)
                            file.write(data)
                            donwloadProgress.PrintProgress(int(dataLenght))
            except :
                print(f"\nClearing {downloadDetails['file_name']} because some error has occurred.")
                remove(f"{fileSettings['download_path']}{downloadDetails['file_name']}")
                WaitKeyToClose("!!! Execution interruped by exception !!!")

        else: print(f"File {downloadDetails['file_name']} already exists, as directed in config will not be downloaded again.")

        if assetIsZip and fileSettings['unzip_file']:
            unzipper = Unzipper()
            unzipper.UnzipFile(assetToDownload)
        elif fileSettings['unzip_file']: print(f"File {downloadDetails['file_name']} is not a zip to be unzipped.")