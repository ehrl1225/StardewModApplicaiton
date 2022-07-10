from zipfile import ZipFile
import os
import shutil

# constants
defalt_steam_url = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\"
unzip_folder = "unzip"
backup_folder = "backup"

# variables
steam_url = defalt_steam_url
stardew_url = os.path.join(steam_url, "Stardew Valley")
stardew_mods_url = os.path.join(stardew_url, "Mods")
stardew_portrait_url = os.path.join(stardew_url, "Content", "Portraits")
stardew_character_url = os.path.join(stardew_url, "Content", "Characters")
backup_portrait_url = os.path.join(backup_folder,"Portraits")
backup_character_url = os.path.join(backup_folder,"Characters")

# for unzip
if not os.path.isdir(unzip_folder):
    os.mkdir(unzip_folder)

# for backup
if not os.path.isdir(backup_folder):
    os.mkdir(backup_folder)
if not os.path.isdir(backup_portrait_url):
    os.mkdir(backup_portrait_url)
if not os.path.isdir(backup_character_url):
    os.mkdir(backup_character_url)


def loadMods():
    folders = []
    for i in os.listdir(stardew_mods_url):
        if os.path.isdir(os.path.join(stardew_mods_url, i)):
            folders.append(i)
    return folders


def unzip_mod(file):
    basename = os.path.basename(file)
    basepath = os.path.join(unzip_folder, basename)
    with ZipFile(file, "r") as zip:
        zip.extractall(basepath)
    for i in os.listdir(basepath):
        _, extension = os.path.splitext(i)
        if i == ".dll":
            mod_folder = basepath
            break
    else:
        mod_folder = os.path.join(basepath, os.listdir(basepath)[0])
    shutil.move(mod_folder, stardew_mods_url)
    shutil.rmtree(basepath)

def backup(file):
    backup_folder_name = os.path.basename(os.path.dirname(file))
    _, e = os.path.splitext(file)
    if e == ".xnb":
        if backup_folder_name == "Portraits":
            shutil.copyfile(file, backup_portrait_url)
        elif backup_folder_name == "Characters":
            shutil.copyfile(file, backup_character_url)
        else:
            print("초상화나 캐릭터 리텍이 아닙니다.")
    print("xnb파일이 아닙니다.")

def openSteamFolder():
    os.stat(steam_url)

def openStardewFolder():
    os.stat(stardew_url)
