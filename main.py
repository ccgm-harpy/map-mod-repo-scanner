import os
from os import system
from os.path import isdir, dirname, realpath
from lib.MMRS import MapModRepoScanner

scriptPath = dirname(realpath(__file__))

def clear_console():
    if os.name == "nt":
        system("cls")
    else:
        system("clear")

if __name__ == "__main__":
    while True:
        clear_console()
        print("Enter your repo path. Must be on your drive! URL is not supported.")
        print("Leave empty to use folder I'm inside of.\n")
        repoPath = str(input("Repo Path-> "))

        if not repoPath:
            repoPath = scriptPath

        if not isdir(repoPath):
            print("Invalid repo path! Press enter to retry.")
            input()
            continue
        
        if MapModRepoScanner(repoPath).valid_repo():
            print("Your repo appears to be valid.")
            print("Still have issues? Ask for help!")

        input("Press enter to continue.")