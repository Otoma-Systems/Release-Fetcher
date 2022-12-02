from handlers.settings_handler import Settings
from handlers.requests_handler import ReleaseFetcher
from handlers.downloads_handler import Downloader
from handlers.unzipper_handler import Unzipper
from handlers.tools_handler import WaitKeyToClose


configSettings = Settings()
if not configSettings.IniciateConfig():
    WaitKeyToClose("No configuration detected so a template config.json was created in the main folder")

releaseFetcher = ReleaseFetcher(configSettings.CONFIG)
fileDownloader = Downloader()

allAssets = releaseFetcher.GetReleaseAssets()

if type(allAssets) != list:
    WaitKeyToClose(type(allAssets))
else:
    for asset in allAssets:
        fileDownloader.DownloadAsset(asset)

    WaitKeyToClose("Finished running")