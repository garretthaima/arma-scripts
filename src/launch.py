import subprocess
import os
import shutil
import re
from mods import download_mod,create_symlink
from parse_mods import modlist
from dotenv import load_dotenv

load_dotenv()

CONFIG_FILE = os.environ["ARMA_CONFIG"]
KEYS = "/arma3/keys"

if not os.path.exists(KEYS) or not os.path.isdir(KEYS):
    if os.path.exists(KEYS):
        os.remove(KEYS)
    os.makedirs(KEYS)

print("Coping configs and mission files to arma directory")

cp = ["cp", "-r", "/tmp/cfg/", os.environ["ARMA_ROOT"]]
subprocess.run(cp)
# shutil.copytree("/tmp/cfg", os.environ["ARMA_ROOT"] + "cfg/")
cp = ["cp", "-r", "/tmp/mpmissions/", os.environ["ARMA_ROOT"]]
subprocess.run(cp)
# shutil.copytree("/tmp/mpmissions", os.environ["ARMA_ROOT"] + "mpmissions")

steamcmd = ["/steamcmd/steamcmd.sh"]
steamcmd.extend(["+login", os.environ["STEAM_USER"], os.environ["STEAM_PASSWORD"]])
steamcmd.extend(["+force_install_dir", "/arma3"])
steamcmd.extend(["+app_update", "233780"])
if "STEAM_BRANCH" in os.environ and len(os.environ["STEAM_BRANCH"]) > 0:
    steamcmd.extend(["-beta", os.environ["STEAM_BRANCH"]])
if "STEAM_BRANCH_PASSWORD" in os.environ and len(os.environ["STEAM_BRANCH_PASSWORD"]) > 0:
    steamcmd.extend(["-betapassword", os.environ["STEAM_BRANCH_PASSWORD"]])
steamcmd.extend(["validate", "+quit"])
steamcmd.extend(["-no-browser"])
print(steamcmd)
subprocess.run(steamcmd)



root = os.getenv("ARMA_ROOT") # "/games/arma/serverfiles"
steam_path = os.getenv("STEAM_ROOT") #"/games/arma/steamcmd/steamapps/workshop/content/107410/"

mod_list = modlist(os.environ["MOD_FILE"])
mod_string = ""
for mod in mod_list:
    download_mod(mod[1], root + "mods")
    create_symlink(steam_path + mod[1], root + "/mods/" + mod[0])
    mod_string = mod_string + "mods/\\" + mod[0] + ";"



def mods(d):
    launch = "\""
    mods = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    for m in mods:
        launch += m+";"
        keysdir = os.path.join(m,"keys")
        if os.path.exists(keysdir):
            keys = [os.path.join(keysdir,o) for o in os.listdir(keysdir) if os.path.isdir(os.path.join(keysdir,o)) == False]
            for k in keys:
                shutil.copy2(k, KEYS)
        else:
            print("Missing keys:", keysdir)
    return launch+"\""

launch = "{} -limitFPS={} -world={}".format(os.environ["ARMA_BINARY"], os.environ["ARMA_LIMITFPS"], os.environ["ARMA_WORLD"])

if os.path.exists("mods"):
    launch += " -mod={}".format(mods("mods"))

clients = int(os.environ["HEADLESS_CLIENTS"])

print("Headless Clients:", clients)

if clients != 0:
    with open("/arma3/configs/{}".format(CONFIG_FILE)) as config:
        data = config.read()
        regex = r"(.+?)(?:\s+)?=(?:\s+)?(.+?)(?:$|\/|;)"

        config_values = {}

        matches = re.finditer(regex, data, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            config_values[match.group(1).lower()] = match.group(2)

        if not "headlessclients[]" in config_values:
            data += "\nheadlessclients[] = {\"127.0.0.1\"};\n"
        if not "localclient[]" in config_values:
            data += "\nlocalclient[] = {\"127.0.0.1\"};\n"

        with open("/tmp/arma3.cfg", "w") as tmp_config:
            tmp_config.write(data)
        launch += " -config=\"/tmp/arma3.cfg\""

    
    client_launch = launch
    client_launch += " -client -connect=127.0.0.1"
    if "password" in config_values:
        client_launch += " -password={}".format(config_values["password"])

    for i in range(0, clients):
        print("LAUNCHING ARMA CLIENT {} WITH".format(i), client_launch)
        subprocess.Popen(client_launch, shell=True)

else:
    launch += " -config=\"/arma3/cfgs/{}\"".format(CONFIG_FILE)

launch += " -port={} -name=\"{}\" -profiles=\"/arma3/cfgs/profiles\"".format(os.environ["PORT"], os.environ["ARMA_PROFILE"])

if os.path.exists("servermods"):
    launch += " -serverMod={}".format(mods("servermods"))

print("LAUNCHING ARMA SERVER WITH", launch, flush=True)
os.system(launch)
