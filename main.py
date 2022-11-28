from requests import get
from OtoPy import UsefulTools

CONFIG = {
"repo_owner" : "mogsoftware",
"repo_name" : "CommuniqueClientApp-Sandbox",
"token" : "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",
"download_path" : "./Downloads/",
"targer_path" : "",
"overwirte_files" : False,
"just_download_zip" : False,
"clean_target_before_extract" : False,
}

URL = f"https://api.github.com/repos/{CONFIG['repo_owner']}/{CONFIG['repo_name']}/releases/latest"
HEADER = {
"Accept": "application/vnd.github+json",
"Authorization": f"token {CONFIG['token']}"
}

latestReleaseJson = get(URL, headers=HEADER).json()
latestTagName = latestReleaseJson['tag_name']

for asset in get(latestReleaseJson["assets_url"], headers=HEADER).json():
    if asset["name"] == f"{latestTagName}.zip":
        fileName = asset["name"]
        latestReleaseZipUrl = asset["url"]
        break

HEADER["Accept"] = 'application/octet-stream'

print(f"Downloading: {latestTagName}.zip")
streamFile = get(latestReleaseZipUrl, stream=True, headers=HEADER)
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