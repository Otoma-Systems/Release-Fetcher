from json import load, dumps
from os.path import exists, dirname

class Settings():
    releaseFetcherTemplate = {
        "repository": {
            "owner": "Otoma-Systems",
            "name": "Release_Fetcher"
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
                    "download_path": "./Downloaded_Assets/",
                    "overwrite_downloaded_files": False,
                    "unzip_file": False
                },
            "unzipper_settings": {
                    "delete_zip_after_unzip": False,
                    "separated_folder_to_unzip": False,
                    "clear_target_before_unzip": False,
                    "overwrite_unziped_files": False,
                    "unzip_targer_path": "./Unziped_Assets/"
                }
        }
    }
    filesTemplate ={
        "files":[
            {
                "file_settings": {
                    "name": None,
                    "extension": "exe",
                    "overwrite_downloaded_files": True
                }
            }
        ]
    }

    def __init__(self, **kwargs) -> None:
        self.configJsonPath = kwargs.get("configJsonPath", "./config.json")
        self.settings = {}

    def InicialConfig(self) -> bool:
        print("╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍")
        if exists(self.configJsonPath):
            #Get settings from config.json
            print("Config file detected. Reading existing configuration.")
            with open(self.configJsonPath, "r") as configFile:
                exstingConfig = load(configFile)

            #Normalize settings from config.json adding any missing configuration
            self.settings = Settings.configTemplate | exstingConfig
            for dictKey in set(Settings.configTemplate):
                self.settings[dictKey] = Settings.configTemplate.get(dictKey) | exstingConfig.get(dictKey, {})

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