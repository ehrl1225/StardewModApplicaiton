from zipfile import ZipFile
import os
import shutil
import json
from PyQt5.QtGui import QPixmap

# constants
default_steam_url = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\"
unzip_folder = "unzip"
backup_folder = "backup"
backup_portrait_url = os.path.join(backup_folder, "Portraits")
backup_character_url = os.path.join(backup_folder, "Characters")
mods_folder = "mods"
xnb_extract_folder = "XNBExtract"
xnb_extract_packed_folder = os.path.join(xnb_extract_folder,"PACKED")
xnb_extract_unpacked_folder = os.path.join(xnb_extract_folder,"UNPACKED")
current_path = os.getcwd()

# global variables
steam_url = default_steam_url
stardew_url = os.path.join(steam_url, "Stardew Valley")
stardew_mods_url = os.path.join(stardew_url, "Mods")
stardew_portrait_url = os.path.join(stardew_url, "Content", "Portraits")
stardew_character_url = os.path.join(stardew_url, "Content", "Characters")
added_mods = []
updated_mods = []

# settings
backup_file_before_apply_retextures = True
when_backup_if_backup_folder_has_the_file_then_dont = True
if_SMAPI_is_on_then_shutdown = False

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

# for service
if not os.path.isdir(mods_folder):
    os.mkdir(mods_folder)

def loadMods():
    folders = []
    for i in os.listdir(stardew_mods_url):
        if os.path.isdir(os.path.join(stardew_mods_url, i)):
            folders.append(i)
    return folders

def getModData(mod_folder):
    data = {}
    manifest_url = os.path.join(mod_folder, "manifest.json")
    basename = os.path.basename(mod_folder)
    if os.path.isfile(manifest_url):
        with open(manifest_url, encoding='utf-8-sig') as f:
            manifest = json.load(f)
        data["Name"] = manifest["Name"]
        data["Version"] = manifest["Version"]
    else:
        data["Name"] = basename
        data["Version"] = None
    return data

def isModFolder(folder):
    if os.path.isfile(folder):
        return False
    for i in os.listdir(folder):
        _,e = os.path.splitext(i)
        if e in [".dll",".json"]:
            return True
    else:
        return False

def hasModFolder(folder):
    listdir = os.listdir(folder)
    for i in listdir:
        _,e = os.path.splitext(i)
        if e in [".dll",".json"]:
            return True
    else:
        if len(listdir) == 1:
            mod_folder = os.path.join(folder, listdir[0])
            if os.path.isdir(mod_folder):
                for i in os.listdir(mod_folder):
                    _, e = os.path.splitext(i)
                    if e in [".dll", ".json"]:
                        return True
                else:
                    return False

def unzip_mod(file):
    basename = os.path.basename(file)
    basepath = os.path.join(unzip_folder, basename)
    with ZipFile(file, "r") as zip:
        zip.extractall(basepath)
    for i in os.listdir(basepath):
        _, extension = os.path.splitext(i)
        if i in [".dll",".json"]:
            mod_folder = basepath
            break
    else:
        if os.listdir(basepath)==1:
            mod_folder = os.path.join(basepath, os.listdir(basepath)[0])
    return mod_folder

# this only backup portrait and character from stardew vally content files
def backup(file, backup_folder_name = None):
    if backup_folder_name is None:
        backup_folder_name = os.path.basename(os.path.dirname(file))
    _, e = os.path.splitext(file)
    file_base_name = os.path.basename(file)
    if e == ".xnb":
        if backup_folder_name == "Portraits":
            backup_folder_file = os.path.join(backup_portrait_url, file_base_name)
            if when_backup_if_backup_folder_has_the_file_then_dont:
                if not os.path.isfile(backup_folder_file):
                    try:
                        shutil.copyfile(file, backup_portrait_url)
                    except PermissionError:
                        if if_SMAPI_is_on_then_shutdown:
                            shutdown_SMAPI()
            else:
                if os.path.isfile(backup_folder_file):
                    os.remove(backup_folder_file)
                shutil.copyfile(file, backup_portrait_url)

        elif backup_folder_name == "Characters":
            if when_backup_if_backup_folder_has_the_file_then_dont:
                if not os.path.isfile(os.path.join(backup_character_url, file_base_name)):
                    try:
                        shutil.copyfile(file, backup_character_url)
                    except PermissionError:
                        if if_SMAPI_is_on_then_shutdown:
                            shutdown_SMAPI()
            else:
                try:
                    shutil.copyfile(file, backup_character_url)
                except PermissionError:
                    if if_SMAPI_is_on_then_shutdown:
                        shutdown_SMAPI()
        else:
            print("초상화나 캐릭터 리텍이 아닙니다.")
    print("xnb파일이 아닙니다.")

def apply_mod(mod):
    mod_basename = os.path.basename(mod)
    stardew_mod = os.path.join(stardew_mods_url,mod_basename)
    try:
        if os.path.isdir(stardew_mod):
            shutil.rmtree(stardew_mod)
            updated_mods.append(mod_basename)
        else:
            added_mods.append(mod_basename)
        shutil.move(mod, stardew_mod)

    except PermissionError:
        if if_SMAPI_is_on_then_shutdown:
            shutdown_SMAPI()

def apply_retexture(file, apply_folder_name, backup_folder = None):
    if backup_file_before_apply_retextures:
        backup(file)
    try:
        shutil.move(file, apply_folder_name)

    except PermissionError:
        if if_SMAPI_is_on_then_shutdown:
            shutdown_SMAPI()

def shutdown_SMAPI():
    os.system("taskkill -im StardewModdingAPI.exe")

def openSteamFolder():
    os.stat(steam_url)

def openStardewFolder():
    os.stat(stardew_url)

def simple_path(path, parent_path = None):
    if parent_path is None:
        parent_path = current_path
    path = path.replace("/","\\")
    if parent_path in path:
        return path[len(parent_path)+1:]
    else:
        return path

def remove_stardew_mod(mod_folder):
    path = os.path.join(stardew_mods_url, mod_folder)
    shutil.rmtree(path)

def xnb_to_img(file):
    basename = os.path.basename(file)
    shutil.copy(file, xnb_extract_packed_folder)
    os.chdir(xnb_extract_folder)
    os.system("UnpackFiles.bat")
    os.chdir(current_path)
    img, _ = os.path.splitext(basename)
    img = os.path.join(xnb_extract_unpacked_folder,(img + ".png"))
    pixmap = QPixmap(img)
    for i in os.listdir(xnb_extract_unpacked_folder):
        os.remove(os.path.join(xnb_extract_unpacked_folder,i))
    for i in os.listdir(xnb_extract_packed_folder):
        os.remove(os.path.join(xnb_extract_packed_folder,i))
    return pixmap


if __name__ == '__main__':
    # file = "mods\\NPC Map Locations 2.9.3-239-2-9-3-1655579084.zip"
    # unzip_path = unzip_mod(file)
    # apply_mod(unzip_path)
    file = "C:\\js\\programing\\python\\StardewMod\\img\\Caroline.xnb"
    xnb_to_img(file)
