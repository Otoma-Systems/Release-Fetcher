from json import load, dumps
from os.path import exists
from handlers.tools_handler import CompareTwoDicts

class Settings():
    releaseFetcherTemplate = {
        "repository": {
            "owner": "Otoma-Systems",
            "name": "Release-Fetcher"
        }
    }
    configTemplate = {
        "repository": {
            "owner": "",
            "name": "",
            "token": ""
        },
        "release": {
            "pre-release_identifier": None
        },
        "default_file_settings" : {
            "file_settings": { 
                    "name": None, 
                    "extension": "zip",
                    "contains_in_name": None,
                    "download_path": "./Downloaded_Assets/",
                    "overwrite_downloaded_files": False,
                    "unzip_file": False
                },
            "unzipper_settings": {
                    "delete_zip_after_unzip": False,
                    "separated_folder_to_unzip": False,
                    "clear_target_before_unzip": False,
                    "overwrite_unzipped_files": False,
                    "unzip_targer_path": "./unzipped_Assets/"
                }
        }
    }
    filesTemplate ={
        "files":[
            {
                "file_settings": {
                    "name": None,
                    "extension": "exe",
                    "download_path": "./"
                }
            }
        ]
    }

    def __init__(self, **kwargs) -> None:
        self.configJsonPath = kwargs.get("configJsonPath", "./config.json")
        self.settings = {}

    def InicialConfig(self) -> bool:
        print("╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍")
        if exists(self.configJsonPath):
            #Get settings from config.json
            print("Config file detected. Reading existing configuration.")
            with open(self.configJsonPath, "r") as configFile:
                exstingConfig = load(configFile)

            #Normalize settings from config.json adding any missing configuration
            self.settings = CompareTwoDicts(Settings.configTemplate, exstingConfig)

            #Write normalized settings to config.json
            with open(self.configJsonPath, "w") as templateConfigFile:
                templateConfigFile.write(dumps(self.settings, indent=4))

            print("Config File was normalized with template in order to have all configurations if missing.")
            return True

        else:
            print("No configuration file detected. Creating one as example.")
            #Write example settings to newly created
            templateJsonConfig = dumps(Settings.configTemplate | Settings.filesTemplate | Settings.releaseFetcherTemplate, indent=4)
            with open(self.configJsonPath, "w") as templateConfigFile:
                templateConfigFile.write(templateJsonConfig)
            return False