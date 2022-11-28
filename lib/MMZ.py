from zipfile import ZipFile
import regex

class MapModZip(ZipFile):
    def __init__(self, zipPath: str):
        super().__init__(zipPath)
        self.zipPath = zipPath
        self.sizeOptions = ["small", "medium", "large", "any"]
        self.modeOptions = [
            "bomb", "tag", "hat king", "king of the hill",
            "race", "hide and seek", "snow brawl"
        ]

    def file_list(self):
        return [file.filename for file in self.filelist]

    def has_config(self):
        return "map.config" in self.file_list()

    def has_map_files(self):
        fileList = self.file_list()

        for fileName in ["map.obj", "map.mtl"]:
            if not fileName in fileList:
                print(f"Missing {fileName} in {self.zipPath}")
                return False

        return True

    def read_config(self):
        with self.open("map.config", "r") as f:
            return f.read().decode('utf-8')

    def valid_config_size(self, configStr: str):
        searchString = f"size\[(?:" + '|'.join(self.sizeOptions) + ")\]"
        results = regex.findall(searchString, configStr)
        return len(results) == 1

    def valid_config_modes(self, configStr: str):
        results = regex.findall("modes\[.*\]", configStr)

        if not results:
            return False

        results = results[0]

        for mode in self.modeOptions:
            results = results.replace(mode, "")

        results = results.replace(" ", "").replace("modes[]", "")
        return len(results) == 0