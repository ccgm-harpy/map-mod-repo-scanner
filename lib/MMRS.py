from os import listdir, name as osName
from os.path import isfile, isdir
from .MMZ import MapModZip

class MapModRepoScanner():
    def __init__(self, path):
        self.slash = "\\" if osName == "nt" else "/"
        self.repoPath = path
        self.mapsPath = f"{self.repoPath}{self.slash}maps"
        self.indexFilePath = f"{self.repoPath}{self.slash}indexfile"
        self.zipScanExclusions = [".gitkeep"]

    def valid_map_list(self):
        files = [m for m in listdir(self.mapsPath) if not m in self.zipScanExclusions]

        for file in files:
            if isdir(file):
                print(f"Found extra directory in your maps folder '{self.mapsPath}{self.slash}{file}'")
                return False

            if not file.endswith(".zip"):
                print(f"File in maps folder that's not a zip '{self.mapsPath}{self.slash}{file}'")
                return False

        return True

    def map_list(self):
        mapList = listdir(self.mapsPath)
        return [
            m.replace(".zip", "") for m in mapList if not m in self.zipScanExclusions
        ]

    def read_index_file(self):
        with open(self.indexFilePath, "r") as f:
            data = f.read()

            if data.endswith("\n"):
                data = data[:-1]

            return data

    def valid_index_file(self, indexStr: str):
        indexMapNames = []

        for i, line in enumerate(indexStr.split("\n")):
            i += 1

            if not "|" in line:
                print(f"Missing '|' in indexfile line #{i}")
                return False

            lineInfo = line.split("|")

            if len(lineInfo) != 2:
                print()
                return False

            try:
                versionNumber = int(lineInfo[0])
                mapName = lineInfo[1]
            except ValueError:
                print(f"Invalid version number in indexfile line #{i}")
                return False

            indexMapNames.append(mapName)

        fileMapNames = self.map_list()

        for i, indexMapName in enumerate(indexMapNames):
            if not indexMapName in fileMapNames:
                print(f"Indexfile contains map '{indexMapName}' which is not in your maps folder. Line #{i+1}")
                return False

        return True
        
    def valid_maps(self):
        mapList = [m for m in listdir(self.mapsPath) if not m in self.zipScanExclusions]

        for _mapZip in mapList:
            mapZip = MapModZip(f"{self.mapsPath}{self.slash}{_mapZip}")

            if not mapZip.has_config():
                print(f"The map {self.mapsPath}{self.slash}{_mapZip} is missing a map.config file")
                return False
            
            if not mapZip.has_map_files():
                return False

            configStr = mapZip.read_config()

            if not mapZip.valid_config_modes(configStr):
                if mapZip.valid_config_lobby_map(configStr):
                    pass
                else:
                    print(f"The map {self.mapsPath}{self.slash}{_mapZip} has invalid map.config modes setting")
                    return False

            if not mapZip.valid_config_size(configStr):
                if mapZip.valid_config_lobby_map(configStr):
                    pass
                else:
                    print(f"The map {self.mapsPath}{self.slash}{_mapZip} has invalid map.config size setting")
                    return False

        return True

    def valid_repo(self):
        if not isfile(self.indexFilePath):
            print("Index file not found in repo folder")
            return False

        if not isdir(self.mapsPath):
            print("The maps folder not found in repo folder")
            return False

        indexStr = self.read_index_file()

        if not self.valid_map_list():
            return False

        if not self.valid_index_file(indexStr):
            return False

        if not self.valid_maps():
            return False

        return True


