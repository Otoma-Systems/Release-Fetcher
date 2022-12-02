from requests import get
from os.path import dirname

class ReleaseFetcher():
    def __init__(self, CONFIG):
        repository = CONFIG.get("repository", {})
        release = CONFIG.get("release", {})
        self.files = CONFIG.get("files", {})
        self.repositoryOwner = repository.get("owner", None)
        self.repositoryName = repository.get("name", None)
        self.repositoryToken = repository.get("token", None)
        self.releaseVersion = release.get("version", "latest")
        self.releaseSufix = release.get("sufix", None)

    def GetReleaseAssets(self):
        if self.repositoryOwner == None or self.repositoryName == None:
            return {"code": 1, "error_message": "Repository settings missing"}

        URL = f"https://api.github.com/repos/{self.repositoryOwner}/{self.repositoryName}/releases/{self.releaseVersion}"
        HEADER = {"Accept": "application/vnd.github+json"}
        DOWNLOAD_HEADER = {"Accept": "application/octet-stream"}
        if self.repositoryToken != None:
            HEADER["Authorization"] = f"token {self.repositoryToken}"
            DOWNLOAD_HEADER["Authorization"] = f"token {self.repositoryToken}"

        releaseData = get(URL, headers=HEADER).json()
        if releaseData.get("message", None) != None:
            return {"code": 2, "error_message": releaseData}

        releaseTagName = releaseData.get('tag_name', None)
        if releaseTagName == None:
            return {"code": 3, "error_message": "Release missing"}

        releaseAssetsUrls = releaseData.get("assets_url", None)
        if releaseAssetsUrls == None:
            return {"code": 4, "error_message": "Assets missing"}

        assetsDetails = list()

        for file in self.files:
            fileDetais = file.get("file_detais", {})
            unzipperSettings = file.get("unzipper_settings", {})

            fileName = fileDetais.get("name") if fileDetais.get("name", None) != None else releaseTagName
            fileNameWithExtension = f"{fileName}.{fileDetais.get('extension', 'zip')}"
            downloadPath = fileDetais.get("download_path", f"{dirname(__file__)}/..//Downloads/")
            TargetPath = fileDetais.get("targer_path", f"{dirname(__file__)}/..//Unziped_Release/")

            for asset in get(releaseAssetsUrls, headers=HEADER).json():
                if asset["name"] == fileNameWithExtension:
                    assetUrl = asset["url"]
                    break
            assetsDetails.append(
                                    {
                                        "file_name": fileNameWithExtension,
                                        "download_details":{
                                            "url": assetUrl,
                                            "header": DOWNLOAD_HEADER
                                        },
                                        "download_path": downloadPath,
                                        "targer_path": TargetPath,
                                        "unzipperSettings": unzipperSettings
                                    }
                                )
        
        return assetsDetails