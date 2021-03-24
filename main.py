from mods import download_mod,create_symlink
from parse_mods import modlist
import os
from dotenv import load_dotenv

load_dotenv()

root = os.getenv["ARMA_ROOT"] # "/games/arma/serverfiles"
steam_path = os.getenv["STEAM_ROOT"] #"/games/arma/steamcmd/steamapps/workshop/content/107410/"

mod_list = modlist("arma_mods.html")

for mod in mod_list:
    download_mod(mod[1], root + "/mods")
    create_symlink(steam_path + mod[1], root + mod[0])