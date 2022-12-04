from handlers.settings_handler import Settings
from handlers.github_handler import GithubHandler
from handlers.unzipper_handler import Unzipper
from handlers.tools_handler import WaitKeyToClose
from os import system, get_terminal_size

windowSize = f"mode 121,45"
system(windowSize)

Logo = [
    "  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
    "  ┃          #########       ################         #########         #######        #######        ########        ┃",
    "  ┃       ###############    ################      ###############      ########      ########       #########        ┃",
    "  ┃     ###################  ################    ###################    #########    #########       ##########       ┃",
    "  ┃    ##################### ################   #####################   ######################      ###########       ┃",
    "  ┃   ########       ########     ######       ########       ########  ######################      ############      ┃",
    "  ┃  #######           ######     ######      ########          ####### ######################     #############      ┃",
    "  ┃  #######           #######    ######      #######           ####### ######################     ######  ######     ┃",
    "  ┃  #######           #######    ######      #######           ####### ######  ######  ######    ######   ######     ┃",
    "  ┃  ########         #######     ######       #######         ######## ######   ####   ######   ######## ########    ┃",
    "  ┃   ########       ########     ######       #########      ########  ######          ######   ##################   ┃",
    "  ┃    #####################      ########   ########################   ######          ######  ###################   ┃",
    "  ┃     ###################        #################################    ######          ######  ####################  ┃",
    "  ┃       ###############           ##############################      ######          ###### ######         ######  ┃",
    "  ┃          ########                 ############     ########         ######          ###### ######         ######  ┃",
    "  ┃                                                                                     ######                        ┃",
    "  ┃                                                                                     ######                        ┃",
    "  ┃                                                                                     ######                        ┃",
    "  ┃                                                                                     ######                        ┃",
    "  ┣╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍┫",
    "  ┃     ┃                   ____       __                        ______     __       __                         ┃     ┃",
    "  ┃  O  ┃                  / __ \___  / /__  ____ _________     / ____/__  / /______/ /_  ___  _____            ┃  O  ┃",
    "  ┃  T  ┃                 / /_/ / _ \/ / _ \/ __ `/ ___/ _ \   / /_  / _ \/ __/ ___/ __ \/ _ \/ ___/            ┃  T  ┃",
    "  ┃  O  ┃                / _, _/  __/ /  __/ /_/ (__  )  __/  / __/ /  __/ /_/ /__/ / / /  __/ /                ┃  O  ┃",
    "  ┃  M  ┃               /_/ |_|\___/_/\___/\__,_/____/\___/  /_/    \___/\__/\___/_/ /_/\___/_/                 ┃  M  ┃",
    "  ┃  A  ┃                                                                                                       ┃  A  ┃", 
    "  ┃     ┃                          Developed and Distributed By: Otoma Systems!                                 ┃     ┃", 
    "  ┗━━━━━┛━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┗━━━━━┛"
]

for line in Logo:
    print(line)


configSettings = Settings()
if not configSettings.InicialConfig():
    WaitKeyToClose("Please edit the new 'config.json' file created in the root folder and execute again.")
githubHandler = GithubHandler(configSettings.settings)

allAssets = githubHandler.GetReleaseAssets()

if type(allAssets) != list:
    WaitKeyToClose(allAssets)
else:
    for asset in allAssets:
        githubHandler.DownloadAsset(asset)

WaitKeyToClose("!!! Finished running !!!")