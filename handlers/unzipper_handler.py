from zipfile import ZipFile, ZipInfo
from os import makedirs
from OtoPy.UsefulTools import OTimedProgressBar

class Unzipper():
    def UnzipFile(self, assetDetails):
        filePath = f"{assetDetails.get('download_path')}{assetDetails.get('file_name')}"
        fileName = assetDetails.get('file_name')
        unzipPath = assetDetails.get("targer_path")
        cleanTargetBeforeUnzip = assetDetails.get("unzipperSettings").get("clean_target_before_unzip")

        print(f"Unzipping: {fileName}")

        makedirs(unzipPath, exist_ok=True)
        with ZipFile(filePath, "r") as zipFile:
            zipSize = sum([size.file_size for size in zipFile.filelist])
            mbSize = 1048576
            filesList = zipFile.filelist
            progressSize = 0
            foldersCount = 0
            filesCount = 0
            unzipProgress = OTimedProgressBar(completeState = int(zipSize))

            for file in filesList:
                if file.filename[-1] == "/":
                    makedirs(unzipPath + file.filename, exist_ok=True)
                    foldersCount += 1
                else:
                    filesCount += 1
                    with zipFile.open(file.filename, "r") as fileToRead:
                        with open(unzipPath + file.filename, "wb") as fileToWrite:
                            while True:
                                fileChunk = fileToRead.read(mbSize)
                                if not fileChunk: break
                                fileToWrite.write(fileChunk)
                                progressSize += len(fileChunk)
                                unzipProgress.PrintProgress(progressSize)

            print(f"Number of Folders Unziped: {foldersCount}, Number of Files Unziped: {filesCount}")
            print(f"Total size of unziped files: {round((zipSize / mbSize), 2)} Mb")