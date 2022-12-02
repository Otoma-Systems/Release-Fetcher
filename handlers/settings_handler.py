from json import load, dumps
from os.path import exists, dirname

class Settings():
    configTemplate = {
        "repository": {
            "owner": "Otoma-Systems",
            "name": "Release_Fetcher",
            "token": ""
        },
        "release": {
            "version": "latest",
            "sufix": None
        },
        "files":[
            {
                "file_detais": { 
                    "extension": "zip",
                    "name": None,
                    "download_path": f"{dirname(__file__)}/../Downloads/".replace("\\\\", "/").replace("\\", "/"),
                    "targer_path": f"{dirname(__file__)}/../Unziped_Release/".replace("\\\\", "/").replace("\\", "/")
                },
                "unzipper_settings": {
                    "unzip_release": False,
                    "clean_target_before_unzip": False
                }
            }
        ]
    }

    def __init__(self, **kwargs) -> None:
        self.configTemplate = kwargs.get("configTemplate", Settings.configTemplate)
        self.configPath = kwargs.get("configPath", f"{dirname(__file__)}/../config.json")
        self.CONFIG = {}

    def IniciateConfig(self) -> bool:
        if exists(self.configPath):
            with open(self.configPath) as configFile:
                self.CONFIG = load(configFile)
                return True
        else:
            templateJsonConfig = dumps(Settings.configTemplate, indent=4)
            with open(self.configPath, "w") as templateConfigFile:
                templateConfigFile.write(templateJsonConfig)
            return False
