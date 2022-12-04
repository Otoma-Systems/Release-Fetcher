from zipfile import ZipFile, ZipInfo
from os import makedirs
from OtoPy.UsefulTools import OTimedProgressBar

class Unzipper():
    def UnzipFile(self, fileToUnzip):
        downloadDetails = fileToUnzip.get("download_details",{})
        fileSettings = fileToUnzip.get("file_settings",{})
        unzipperSettings = fileToUnzip.get("unzipper_settings",{})

        filePath = f"{fileSettings['download_path']}{downloadDetails['file_name']}"
        targetPath = unzipperSettings['unzip_targer_path']
        chunkSize = 1048576

        if unzipperSettings['separated_folder_to_unzip']: 
            if unzipperSettings['separated_folder_to_unzip'] == True:
                targetPath += f"{downloadDetails['file_name'][:-4]}/"
            else: 
                targetPath += f"{unzipperSettings['separated_folder_to_unzip']}/"
        print("-----------------------------------------------------------------------------------------------------------------------")
        print(f"Unzipping: {downloadDetails['file_name']} on: \"{targetPath}\"")

        makedirs(targetPath, exist_ok=True)
        with ZipFile(filePath, "r") as zipFile:
            zipSize = sum([size.file_size for size in zipFile.filelist])
            filesList = zipFile.filelist
            currentFilesSize = 0
            foldersCount = 0
            filesCount = 0
            unzipProgress = OTimedProgressBar(completeState = int(zipSize))

            for file in filesList:
                if file.filename[-1] == "/":
                    makedirs(targetPath + file.filename, exist_ok=True)
                    foldersCount += 1
                else:
                    with zipFile.open(file.filename, "r") as fileToRead:
                        with open(targetPath + file.filename, "wb") as fileToWrite:
                            filesCount += 1
                            while True:
                                fileChunk = fileToRead.read(chunkSize)
                                if not fileChunk: break
                                fileToWrite.write(fileChunk)
                                currentFilesSize += len(fileChunk)
                                unzipProgress.PrintProgress(currentFilesSize)

            print(f"Number of Folders Unziped: {foldersCount}, Number of Files Unziped: {filesCount}")
            print(f"Total size of unziped files: {round((zipSize / 1048576), 2)} Mb")