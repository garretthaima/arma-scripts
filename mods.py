import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

def download_mod(mod_id, path):
    steamcmd = ["steamcmd"]
    steamcmd.extend(["+login", os.getenv("STEAM_USER"), os.getenv("STEAM_PASS")])
    # steamcmd.extend(["+login", os.environ["STEAM_USER"]])
    # steamcmd.extend(["+force_install_dir", path])
    steamcmd.extend(["+workshop_download_item", "107410 " + mod_id])
    steamcmd.extend(["validate", "+quit"])
    print("Downloading mod")
    subprocess.run(steamcmd)

def create_symlink(source, dest):
    print("Creating symlink")
    cmd = ["ln"]
    cmd.extend(["-s"])
    cmd.extend([source])
    cmd.extend([dest])
    subprocess.run(cmd)
