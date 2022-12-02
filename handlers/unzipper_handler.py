from zipfile import ZipFile
from os import makedirs

class Unzipper():
    def UnzipFile(self, assetDetails):
        filePath = f"{assetDetails.get('download_path')}{assetDetails.get('file_name')}"
        unzipPath = assetDetails.get("targer_path")
        cleanTargetBeforeUnzip = assetDetails.get("unzipperSettings").get("clean_target_before_unzip")

        makedirs(unzipPath, exist_ok=True)
        with ZipFile(filePath, "r") as zipFile:
            zipFile.extractall(unzipPath)