# Map Mod Repo Scanner
Scans Crab Game's Map Mod repo for errors. Makes fixing issues with large repo's easier.

**Instructions:** <br />
1. Open the program <br />
2. Give it your local repository's path (must be on drive, url not supported)<br /><br />

**Supports:**<br />
- Checking if the indexfile exists <br />
- Checking if the maps folder exists <br />
- Checking if the indexfile is valid and matches the contents of the maps folder <br />
- Checking if the map configs exist in the zip files ("size" and "modes" options exist and are valid) <br />
- Checking the map zip files for .obj and .mtl files <br /><br />

**Note:** If no path is provided, it will scan the path the script is currently inside of.

**Build instructions:** <br />
1. Make sure you have python3 installed with pip.
2. Run `pip install pyinstaller` (replace "pip" with "pip3" if not found)
3. Execute `build.bat` on Windows or `build.sh` on Linux
4. Built binary will be located in scriptPath/dist
