import os,sys,grp,subprocess,json,utils

if not os.path.exists("/var/lib/zany") or not os.path.exists("/etc/zany") or not os.path.exists("/var/cache/zany"):
    print("Incomplete installation!")
    if os.geteuid() != 0:
        print("Please run zany as root next run; zany needs to create folders and files that do not exist, as well as set up their permissions.")
        exit(1)
    group = None
    try:
        group = grp.getgrnam("zany")
    except KeyError:
        subprocess.run(["groupadd","--system","zany"],check=True)
        group = grp.getgrnam("zany")
    gid = group.gr_gid

    os.makedirs("/etc/zany",exist_ok=True) # config
    os.makedirs("/var/lib/zany",exist_ok=True) # state
    os.makedirs("/var/cache/zany",exist_ok=True) # cache
    os.chown("/etc/zany",0,0)
    os.chown("/var/lib/zany",0,gid)
    os.chown("/var/cache/zany",0,gid)
    os.chmod("/etc/zany",0o2775)
    os.chmod("/var/lib/zany",0o2775)
    os.chmod("/var/cache/zany",0o2775)
    os.makedirs("/etc/zany/repos",exist_ok=True) # repos

    defaultState = {
        "packages":[] # each entry is of form ["repo","name","version"]
    }
    defaultConfig = {}
    with open("/etc/zany/conf.json","a+") as f:
        f.seek(0)
        data = f.read()
        if data != "":
            data = json.loads(data)
        else:
            data = {}
        f.truncate(0)
        f.seek(0)
        if not isinstance(data,dict):
            raise TypeError("zany config is of the wrong type!")
        f.write(json.dumps(utils.defaultDict(data,defaultConfig)))
    with open("/var/lib/zany/state.json","a+") as f:
        f.seek(0)
        data = f.read()
        if data != "":
            data = json.loads(data)
        else:
            data = {}
        f.truncate(0)
        f.seek(0)
        if not isinstance(data,dict):
            raise TypeError("zany config is of the wrong type!")
        f.write(json.dumps(utils.defaultDict(data,defaultState)))

def getState():
    with open("/var/lib/zany/state.json","r") as f:
        return json.loads(f.read())