from handlers.Settings import Settings
from handlers.release_fetcher import ReleaseFetcher
from handlers.download import Downloader
#from handlers.unzipper import 
from handlers.tools import WaitKeyToClose

configSettings = Settings()
if not configSettings.IniciateConfig():
    WaitKeyToClose("No configuration detected so a template config.json was created in the main folder")

releaseFetcher = ReleaseFetcher(configSettings.CONFIG)
fileDownloader = Downloader()

for asset in releaseFetcher.GetReleaseAssets():
    fileDownloader.DownloadAsset(asset)
    
WaitKeyToClose("Finished running")