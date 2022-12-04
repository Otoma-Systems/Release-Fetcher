from zipfile import ZipFile
from os import makedirs, remove
from os.path import exists
from shutil import rmtree
from OtoPy.UsefulTools import OTimedProgressBar

class Unzipper():
    def UnzipFile(self, fileToUnzip):
        downloadDetails = fileToUnzip.get("download_details",{})
        fileSettings = fileToUnzip.get("file_settings",{})
        unzipperSettings = fileToUnzip.get("unzipper_settings",{})

        filePath = f"{fileSettings['download_path']}{downloadDetails['file_name']}"
        targetPath = unzipperSettings['unzip_targer_path']

        if unzipperSettings['separated_folder_to_unzip']: 
            if unzipperSettings['separated_folder_to_unzip'] == True:
                targetPath += f"{downloadDetails['file_name'][:-4]}/"
            else: 
                targetPath += f"{unzipperSettings['separated_folder_to_unzip']}/"

        if exists(f"{targetPath}RELEASE_VERSION"):
            with open(f"{targetPath}RELEASE_VERSION", "r") as versionFile:
                releaseAlreadyExists = bool(versionFile.read() == downloadDetails["release_name"])
        else: releaseAlreadyExists = False

        if unzipperSettings['overwrite_unzipped_files'] or not releaseAlreadyExists:         
            if unzipperSettings["clear_target_before_unzip"] and exists(targetPath):
                print(f"Clearing \"{targetPath}\" before unziping, as requested in config.")
                rmtree(f"{targetPath}")
            makedirs(targetPath, exist_ok=True)

            print(f"Unzipping: {downloadDetails['file_name']} on: \"{targetPath}\".")

            with ZipFile(filePath, "r") as zipFile:
                zipSize = sum([size.file_size for size in zipFile.filelist])
                filesList = zipFile.filelist
                filesCount = len(filesList)
                unzipProgress = OTimedProgressBar(completeState = filesCount, fill='❚', suffix="Unzipped  ")

                for fileCount, file in enumerate(filesList):
                    zipFile.extract(file.filename, path=targetPath)
                    unzipProgress.PrintProgress(fileCount+1)

            if not releaseAlreadyExists:
                with open(f"{targetPath}RELEASE_VERSION", "w") as versionFile:
                    versionFile.write(downloadDetails["release_name"])

            print(f"Folders and Files unzipped: {filesCount}, Total size of unzipped files: {round((zipSize / 1048576), 2)} Mb.")

        else: print(f"File {downloadDetails['file_name']} already unzipped, as directed in configs will not be unzipped again.")

        if unzipperSettings["delete_zip_after_unzip"]:
                remove(filePath)
                print(f"Clearing \"{filePath}\" as requested in config.")