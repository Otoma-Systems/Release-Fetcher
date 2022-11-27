from requests import get, session

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

print(f"Downloading: {latestTagName}.zip with link: {latestReleaseZipUrl}")

HEADER["Accept"] = 'application/octet-stream'
streamFile = get(latestReleaseZipUrl, headers=HEADER)
with open(CONFIG['download_path'] + fileName, "wb") as file:
    file.write(streamFile.content)

print("Download completed!")