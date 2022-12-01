from requests import get
from OtoPy import UsefulTools


HEADER["Accept"] = 'application/octet-stream'

print(f"Downloading: {releaseTagName}.zip")
streamFile = get(ReleaseZipUrl, stream=True, headers=HEADER)
contentLength = streamFile.headers.get('content-length')
donwloadProgress = UsefulTools.OTimedProgressBar(completeState = int(contentLength))

with open(CONFIG['download_path'] + fileName, "wb") as file:
    if contentLength is None:
        file.write(streamFile.content)
    else:
        dataLenght = 0
        contentLength = int(contentLength)
        for data in streamFile.iter_content(chunk_size=4096):
            dataLenght += len(data)
            file.write(data)
            donwloadProgress.PrintProgress(int(dataLenght))