from requests import get
from os import makedirs
from OtoPy import UsefulTools

class Downloader():
    def DownloadAsset(self, assetDetails):
        fileName = assetDetails.get("file_name")
        url = assetDetails.get("download_details").get("url")
        header = assetDetails.get("download_details").get("header")
        downloadPath = assetDetails.get("download_path")
        unzipRelease = assetDetails.get("unzipperSettings").get("unzip_release")

        print(f"Downloading: {fileName}")
        streamFile = get(url, stream=True, headers=header)
        contentLength = streamFile.headers.get('content-length')
        donwloadProgress = UsefulTools.OTimedProgressBar(completeState = int(contentLength))

        makedirs(downloadPath, exist_ok=True)
        with open(f"{downloadPath}{fileName}", "wb") as file:
            if contentLength is None:
                file.write(streamFile.content)
            else:
                dataLenght = 0
                contentLength = int(contentLength)
                for data in streamFile.iter_content(chunk_size=4096):
                    dataLenght += len(data)
                    file.write(data)
                    donwloadProgress.PrintProgress(int(dataLenght))
        
        if unzipRelease:
            pass
