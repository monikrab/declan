
import json
from argparse import ArgumentParser
from pathlib import Path
from getpass import getuser
from sys import exit, stdin
from os import environ as env, getenv
from textwrap import dedent
from subprocess import run, Popen, DEVNULL, PIPE
from shutil import copy2, which, rmtree
from datetime import datetime as dt
from re import findall
from glob import glob
from os import geteuid


class DeclanError(Exception):
    pass

class EnvVarExistsError(DeclanError):
    def __init__(self, path):
        super().__init__(
            f"""\n\033[91m error:\033[0m environment variable already exists in {path}
 Make sure it matches your configuration file's path!"""
        )

class EnvVarNotExistsError(DeclanError):
    def __init__(self):
        super().__init__("\033[91merror:\033[0m environment variable unset, retry 'declan init'")

class ConfigAlreadyInitError(DeclanError):
    def __init__(self, path):
        super().__init__(f"""\033[91merror:\033[0m config already initialized at {path}""")


def safe_getenv(env_var):
    if getenv(env_var) is None:
        raise EnvVarNotExistsError()
    else:
        return getenv(env_var)
        
    


# TODO:
"""
- Implement functionalities:
    - clear
    - gc
    - rice (with --push)
    - backup 
"""

parser = ArgumentParser(
    prog="declan",
    usage="declan <operation> [options]",
    add_help=False,
    color=False
)

parser.add_argument(
    "-h", "--help",
    action="store_true"
)

parser.add_argument(
    "-v", "--version",
    action="store_true"
)

parser.add_argument(
    "operation",
    nargs="?",
    choices = ["init", "clear", "relay", "rebuild", "gc", "rice", "backup"]
)

parser.add_argument(
    "--gc",
    action="store_true"
)
parser.add_argument(
    "--casc",
    action="store_true"
)
parser.add_argument(
    "--push",
    action="store_true"
)

args = parser.parse_args()




user = getuser()
cache_path = Path(f"/home/{user}/.cache/declan")
cache_path.parent.mkdir(parents=True, exist_ok=True)



version = "\033[3mversion 1.0\033[0m"

usage = """usage: declan <operation> [options]\n
operations:
    declan {-h | --help}
    declan {-v | --version}
    declan init
    declan clear
    declan relay    [--casc]
    declan rebuild  [--gc] [--casc]
    declan gc
    declan rice     [--push]
    declan backup"""


logo = """\033[1m  _____    _______   _____   _          _      _   _
 |  __ \\  |  ____/  / ____\\ | |        / \\    | \\ | |
 | |  | | | |___   | /      | |       /   \\   |  \\| |
 | |  | | |  ___|  | |      | |      /  ∆  \\  |     |
 | |__| | | |____  | \\____  | |___  /  ___  \\ | |\\  |
 |_____/  \\______\\  \\_____/ \\_____/ \\_/   \\_/ |_| \\_|\033[0m"""




def init():
    print(logo,
          "\n       \033[3;90mdeclarative system configuration for 󰣇\033[0m",
          sep="", end="\n\n"
      )

    
    cached_config = next(cache_path.glob("*.json"), None)

    if cached_config is not None:
        read_cached = ""

        while read_cached not in ["y", "n"]:
            read_cached = str(input(
                "\n\033[93m warning:\033[0m found pre-existing config file in cache\n Would you like to read it? [Y/n]: "
            )).lower()

        if read_cached == "y":
            print()
            run(["cat", f"{cached_config}"])
            
            keep_cached = str(input("\n\n Would you like to keep this config? [Y/n]: ")).lower()
            if keep_cached == "y": use_cached = True
        
        else: print()
    
    else:
        use_cached = False 

        
    config_name = ""
    while not config_name.strip():
        config_name = str(input("\n Enter the name for your configuration file.\n"
                                " Do not add a file extension.\n\n"
                                " Name: "))
    config_path = Path(f"/home/{user}/{config_name}.json")


    release = Path("/etc/os-release").read_text()
    if   "ID=cachyos" in release:     distro = "CachyOS"
    elif "ID=arch" in release:        distro = "Arch Linux"
    elif "ID=manjaro" in release:     distro = "Manjaro"
    elif "ID=endeavouros" in release: distro = "EndeavourOS"
    elif "ID=omarchy" in release:     distro = "Omarchy"
    elif "ID=garuda" in release:      distro = "Garuda Linux"
    elif "ID=biglinux" in release:    distro = "BigLinux"
    elif "ID=artix" in release:       distro = "Artix Linux"
    elif "ID=archcraft" in release:   distro = "Archcraft"
    else:
        print("\033[91m error:\033[0m unsupported operating system")
        exit(1)


    default_config = json.dumps({
        "description": f"{user}'s {distro} configuration",
        "packages": [],
        "services": [],
        "gc": {
            "enabled": False,
            "include": []
        },
        "configs": {
            "enabled": False,
            "include": []
        },
        "backup": {
            "enabled": False,
            "include": []
        }
    }, indent=4)

    
    try:
        with open(config_path, "x") as f:
            if use_cached: copy2(cached_config, config_path)
            else: f.write(default_config)
    except FileExistsError:
        print("\033[93m warning:\033[0m file already exists! (", config_path, ")",
              "\n\n Trying to set config path environment variable...", sep="")
    else:
        print("\n\033[92m Config file created.\n \033[0mPath to config:", config_path, end="\n")

        with open(cache_path / "declan.log", "a") as log:
            print(dt.now(), ": Written config file to ", config_path, sep="", file=log)

        with open(cache_path / (dt.now().strftime('%Y-%m-%d_%H-%M') + ".json"), "w") as default_log:
            default_log.write(default_config)



    user_sh = env.get("SHELL")
    if   user_sh in ["/usr/bin/fish", "/bin/fish"]: sh_path = ".config/fish/config.fish" 
    elif user_sh in ["/usr/bin/zsh", "/bin/zsh"]:   sh_path = ".zshrc"
    elif user_sh in ["/usr/bin/bash", "/bin/bash"]: sh_path = ".bashrc"

    env_var = dedent(f"""
        # Automatically generated by `declan init`
        export DECLAN_CONFIG_PATH='{config_path}'"""
    )
    with open(f"/home/{user}/{sh_path}", "a+") as f:
        f.seek(0)
        if "DECLAN_CONFIG_PATH" in f.read(): raise EnvVarExistsError(sh_path)
        else:
            f.write(env_var)
            print(" \033[3m(saved at", sh_path, "as $DECLAN_CONFIG_PATH)\033[0m", end="\n")


        print("\033[92m\n Initialization finished.\033[0m\n"
              "\033[91m Please restart your shell before using Declan!\033[0m\n"
              " For usage instructions, type 'declan --h' or 'man 1 declan' into your shell\n\n"
          "\033[95m Enjoy :V\033[0m")        




def parse_config(path):
    with open(path, "r") as f:
        try:
            declan = json.load(f)
        except json.JSONDecodeError as error:
            print(f"\033[91merror:\033[0m invalid JSON formatting: {error.msg.lower()} at line {error.lineno}, character {error.colno}")
            exit(1)
    
    # TODO: Catch JSONDecodeError
    """
    Codes:
        P -> Packages | [1]
        S -> Services | [2]
        G -> Garbage  | [3]
        C -> Configs  | [4]
        B -> Backup   | [5]
    """

    enabled_features = ""
    config_data = [None, [], [], [], [], []]

    if declan["packages"]:
        enabled_features += "P"
        packages = declan["packages"]; config_data[1] = packages

    if declan["services"]:
        enabled_features += "S"
        services = declan["services"]; config_data[2] = services

    if declan["gc"]["enabled"]:
        enabled_features += "G"
        gc = declan["gc"]["include"]; config_data[3] = gc

    if declan["configs"]["enabled"]:
        enabled_features += "C"
        configs = declan["configs"]["include"]; config_data[4] = configs

    if declan["backup"]["enabled"]:
        enabled_features += "B"
        backup = declan["backup"]["include"]; config_data[5] = backup

    config_data[0] = enabled_features
    return config_data




def relay_rebuild(packages, services):    
    to_remove = set(); to_disable = set()

    cached_config_path = next(cache_path.glob("*.json"), None)
    try:
        with open(cached_config_path, "r") as path:
            cached_config = json.load(path)
        cached = True
    except TypeError:
        cached = False


    # Packages
    if args.operation == "relay":
        to_install = packages - (set(cached_config["packages"]) & packages)
        if to_install:
            print("\033[1mPackages to install:\033[0m\n", '\n'.join(to_install), sep="", end="\n\n")

    elif args.operation == "rebuild":
        print("\033[1mPackages to update:\033[0m")

        pending_updates = run(
            ["pacman", "-Quq"], stdout=PIPE
        )
        run(
            ["column", "-S", "2"], input=pending_updates.stdout
        )

        if pending_updates.stdout: to_install = "updates"
        
        print()

    if cached:
        to_remove = set(cached_config["packages"]) - packages
    if to_remove:
        print("\033[1mPackages to remove:\033[0m\n", '\n'.join(to_remove), sep="", end="\n\n")


    # Services
    to_enable = services - (set(cached_config["services"]) & services)
    if to_enable:
        print("\033[1mServices to enable:\033[0m\n", '\n'.join(to_enable), sep="", end="\n\n")

    if cached:
        to_disable = set(cached_config["services"]) - services
    if to_disable:
        print("\033[1mServices to disable:\033[0m\n", '\n'.join(to_disable), sep="", end="\n\n")

    if any(i for i in (to_install, to_enable, to_remove, to_disable)):
        while 1:
            proceed = str(input("\033[35m::\033[0m Proceed? [Y/n]: ")).strip().lower(); print()
            if proceed in ["y", "n"]:
                if proceed == "n": exit(0)
                break
    else:
        print("there is nothing to do")
        exit(0)


    
    # Apply changes
    run(["sudo", "-v"])

    if to_install:
        if args.operation == "relay":
            run(
                ["yay", "-S", "--asexplicit",
                "--noconfirm", "--noprogressbar", "--needed", *to_install],
            )
        elif args.operation == "rebuild":        
            run(
                ["yay", "-Syu", "--noconfirm", "--noprogressbar"],
            )

    if to_remove:
        if args.casc:
            for pkg in to_remove:
                p = Popen(
                    ["sudo", "pacman", "-Rncs", "--noprogressbar", pkg],
                    stdin=PIPE, # ls pid/fd: 0 -> 'pipe:[123456]'
                    text=True
                )
                char = stdin.read(2)
                if char:
                    if char[0] == "n":
                        _, _ = p.communicate() # close the first command
                        print("\033[1;3;32m\nRemoving without cascade...\n\n\033[0m")
                        run(
                            ["yay", "-Rns", "--noconfirm", "--noprogressbar", pkg],
                            stdout=DEVNULL
                        )

                    _, _ = p.communicate() # close remaining command
        


    if to_enable:
        if to_install: print()
        print("Enabling services...", end="\n")
        run(
            ["sudo", "systemctl", "enable", "--now", *to_enable],
        )
        print("Done.")

    if to_disable:
        if to_enable: print()
        print("Disabling services...", end="\n")
        run(
            ["sudo", "systemctl", "disable", "--now", *to_disable],
        )
        print("Done.")





def garbage_collect(paths):
    hard_paths = [Path(path).expanduser() for path in paths]

    for path in hard_paths:
        if "*" in str(path):
            glob_paths = glob(str(path))
            
            hard_paths.remove(path)

            for glob_path in glob_paths:
                hard_paths.append(glob_path)

    rm_paths = [Path(hard_path) for hard_path in hard_paths]


    ask_sudo = True

    for path in rm_paths:
        try:
            if path.is_dir():
                rmtree(path)
            else:
                path.unlink()

        except FileNotFoundError as e:
            if geteuid() != 0:
                print(f"\033[93mwarning:\033[0m file/directory not found: {e.filename}, skipping...\n")

        except PermissionError:
            if not ask_sudo:
                continue
        
            while 1:
                run_sudo = str(input(
                            "\033[93mwarning:\033[0m certain listed include(s) under root ownership\n" +
                            "Re-run garbage-collection as root? [Y/n]: "
                          )).strip().lower()

                if run_sudo == "y":
                    run(["sudo", "-E", "python3", "/home/monikrab/dev/declan/src/declan.py", "gc"])
                    exit(0)

                elif run_sudo == "n":
                    ask_sudo = False
                    break
                else:
                    print()




def backup(includes):
    hard_paths = [Path(path).expanduser() for path in includes]

    location = Path(input("Backup path:\033[92m ")).expanduser()
    filename = str(input("\033[0mBackup name:\033[92m "))
    compression_lvl = input("\033[0mCompression level [1-9]:\033[92m ")
    print("\033[90m")


    wc_size = run(
        ["wc", "-c", *hard_paths],
        capture_output=True,
        text=True
    )
    for line in wc_size.stdout.splitlines():
        if "total" in line:
            size = line.split()[0]
        elif not wc_size.stdout.splitlines()[1]:
            size = line.split()[0]


    options= { "XZ_OPT": f"-T0 -{compression_lvl}" }

    tar_cf = Popen(
        ["tar", "cf", "-", *hard_paths],
        env=options,
        stdout=PIPE,
    )
    progress_bar = Popen(
        ["pv", "-w", "100", "-s", f"{size}"],
        stdin=tar_cf.stdout,
        stdout=PIPE
    )
    tar_cf.stdout.close()

    with open(location / (filename + ".tar.xz"), "wb") as backup_file:
        run(
            ["xz"],
            stdin=progress_bar.stdout,
            stdout=backup_file
        )

        progress_bar.stdout.close()
    



def cache_config(user, home_config):
    stats = home_config.stat()
    last_modification = dt.fromtimestamp(stats.st_mtime)
    date_l_m = last_modification.strftime("%Y-%m-%d_%H-%M")

    try:
        old_cached_config = next(
            cache_path.glob("*.json"),
            None
        )
        old_cached_config.unlink()
    except AttributeError:
        pass
    
    copy2(home_config, cache_path / (date_l_m + ".json"))




def main():
    if args.operation is None:
        if args.version:
            print(
                logo, " " + version,
                "\n This program may be freely redistributed under",
                " the terms of the GNU General Public License, version 2.0",
                sep="\n", end="\n\n"
             )
            exit(0)

        if args.help: print(usage)
        else: print(usage)


    if args.gc and args.operation != "rebuild":
        print("\033[91merror:\033[0m option '--gc' can only be used with operation(s): rebuild",
              usage, sep="\n\n")
        exit(1)

    if args.casc and args.operation not in ["relay", "rebuild"]:
        print("\033[91merror:\033[0m option '--casc' can only be used with operation(s): relay, rebuild",
              usage, sep="\n\n")
        exit(1)

    if args.push and args.operation != "rice":
        print("\033[91merror:\033[0m option '--push' can only be used with operation(s): rice",
              usage, sep="\n\n")
        exit(1)


    if args.operation == "init":
        try:
            with open(cache_path / "declan.log", "r") as log:
                file = log.read()
            
            paths = findall(r"/\S+\.json", file)
            if paths:
                if Path(paths[-1]).exists() == False:
                    raise FileNotFoundError

            if "Written config file to" in file:
                raise ConfigAlreadyInitError(safe_getenv("DECLAN_CONFIG_PATH"))
        
        except FileNotFoundError:
            init()
            exit(0)


    config_path = Path(safe_getenv("DECLAN_CONFIG_PATH"))

    
    try:
	    features = parse_config(config_path)
    except FileNotFoundError:
        print("\033[91merror:\033[0m config file not found")
        
        cached_config = next(cache_path.glob("*.json"), None)
        if cached_config is not None:
            read_cached = ""

            while read_cached not in ["y", "n"]:
                read_cached = str(input(
                  "\n\033[93mwarning:\033[0m found pre-existing config file in cache\nWould you like to read it? [Y/n]: "
                )).lower()

            if read_cached == "y":
                print()
                run(["cat", f"{cached_config}"])
            
            keep_cached = str(input("\nWould you like to keep this config? [Y/n]: ")).lower()
            if keep_cached == "y": copy2(cached_config, config_path)
        
        exit(1)


    if args.operation in ["relay", "rebuild"]:
        if which("yay") is None:
            install_yay = str(input("\033[91m error:\033[0m yay (AUR helper) is not installed\n\n"
                                    " Without it, the following operations are unavailable:\n"
                                    " relay, rebuild\n\n"
                                    " Would you like to install it now? [Y/n]: "))
            
            if install_yay.lower() == "y":
                run("yay -Y --gendb && yay -Y --devel --save", shell=True)
                run("sudo pacman -S --needed git base-devel", shell=True)
                run("git clone https://aur.archlinux.org/yay-bin.git && cd yay-bin && makepkg -si",
                    shell=True)
            else:
                exit(0)

        
        if "P" in features[0] or "S" in features[0]:
            if "S" not in features[0]:
                relay_rebuild(set(features[1]), set())
            elif "P" not in features[0]:
                relay_rebuild(set(), set(features[2]))
            else:
                relay_rebuild(set(features[1]), set(features[2]))

            if args.gc: garbage_collect(features[3])
            cache_config(user, config_path)
            
        else:
            print("there is nothing to do")
            return


    if args.operation == "gc":
        if "G" in features[0]:
            if not features[3]:
                print("\033[91merror:\033[0m no garbage collection paths specified")
            else:
                garbage_collect(features[3])
        else:
            print("\033[91merror:\033[0m garbage collection disabled in config")


    if args.operation == "backup":
        if which("pv") is None:
            install_pv = str(input(
                                "\033[91m error:\033[0m pv (backup progress tracker) is not installed\n\n"
                                " Would you like to install it now? [Y/n]: "
                            ))
            if install_pv.lower() == "y":
                run(["sudo", "pacman", "-S", "pv"])
            else:
                exit(0)
            
            
        if "B" in features[0]:
            if not features[5]:
                print("\033[91merror:\033[0m no paths to back up")
            else:
                backup(features[5])
        else:
            print("\033[91merror:\033[0m backups disabled in config")



try:
    main()
except DeclanError as error:
    print(error)
except (KeyboardInterrupt, EOFError):
    print("\n\n\033[91merror:\033[0m execution interrupted by user!")
