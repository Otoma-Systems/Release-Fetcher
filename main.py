from handlers.settings_handler import Settings
from handlers.github_handler import GithubHandler
from handlers.unzipper_handler import Unzipper
from handlers.tools_handler import WaitKeyToClose


configSettings = Settings()
if not configSettings.InicialConfig():
    WaitKeyToClose("Please edit the new 'config.json' file created in the root folder and execute again")
githubHandler = GithubHandler(configSettings.settings)

allAssets = githubHandler.GetReleaseAssets()

if type(allAssets) != list:
    WaitKeyToClose(allAssets)
else:
    for asset in allAssets:
        githubHandler.DownloadAsset(asset)

WaitKeyToClose("Finished running")