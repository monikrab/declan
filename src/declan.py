#!/usr/bin/env python3

"""
Declan

A tiny utility to manage
Arch-based Linux declaratively 

https://github.com/monikrab/declan
"""


import json                                       # init, parse_config, relay_rebuild
from argparse import ArgumentParser               # global
from getpass import getuser                       # global
from pathlib import Path                          # global, init, clear, main
from textwrap import dedent                       # init
from os import environ as env, getenv             # init, clear
from shutil import copy2, which, rmtree           # init, clear, cache_config, main
from sys import exit, stdin                       # init, parse_config, relay_rebuild, main
from subprocess import run, Popen, DEVNULL, PIPE  # init, relay_rebuild, garbage_collect, rice, backup, main
from datetime import datetime as dt               # init, cache_config
from glob import glob                             # garbage_collect
from os.path import expanduser                    # garbage_collect, backup
from re import findall                            # main



user = getuser()

cache_path = Path(f"/home/{user}/.cache/declan")
cache_path.mkdir(parents=True, exist_ok=True)

version = "\033[3mversion 1.1\033[0m"

usage = """usage: declan <operation> [options]\n
operations:
    declan {-h | --help}
    declan {-v | --version}
    declan init
    declan clear
    declan relay    [--casc]
    declan rebuild  [--gc] [--casc]
    declan gc
    declan rice     [--get]
    declan backup"""


logo = """\033[1m  _____    _______   _____   _          _      _   _
 |  __ \\  |  ____/  / ____\\ | |        / \\    | \\ | |
 | |  | | | |___   | /      | |       /   \\   |  \\| |
 | |  | | |  ___|  | |      | |      /  ∆  \\  |     |
 | |__| | | |____  | \\____  | |___  /  ___  \\ | |\\  |
 |_____/  \\______\\  \\_____/ \\_____/ \\_/   \\_/ |_| \\_|\033[0m"""



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
    "--get",
    action="store_true"
)

args = parser.parse_args()




"""
Exit Codes:
    Success       | (0)
    PythonError   | (1)
    DeclanError   | (2)
    UncaughtError | (3)
    EarlyExit     | (4)
"""

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




def init():
    print(
        logo,
        "\n       \033[3;90mdeclarative system configuration for 󰣇\033[0m",
        sep="", end="\n\n\n"
    )



    cached_cfg = next(cache_path.glob("*.json"), None) # there should only be one

    if cached_cfg is not None:
        read_cached_yn = ""
        while read_cached_yn not in ["y", "n"]:
            read_cached_yn = input(
                "\n\033[93m warning:\033[0m found pre-existing config file in cache\n Would you like to read it? [Y/n]: "
            ).strip().lower()

        if read_cached_yn == "y":
            print(); run(["cat", f"{cached_cfg}"])
            
            keep_cached_yn = input(
                "\n\n\033[35m::\033[0m Would you like to keep this config? [Y/n]: "
            ).strip().lower()

            if keep_cached_yn == "y": use_cached = True

        else: print()

    else: use_cached = False



    cfg_name = ""
    while not cfg_name:
        cfg_name = input(
            " Enter your configuration file's name\n"
            " \033[3m(to be stored under /home/user/name.json)\033[0m\n\n"
            " Spaces will be removed. Do not add a file extension\n\n"
            " Name: "
        ).strip().replace(" ", "")

    cfg_path = Path(f"/home/{user}/{cfg_name}.json")



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
        exit(3)



    default_cfg = json.dumps({
        "description": f"{user}'s {distro} configuration",
        "packages": [],
        "services": [],
        "gc": {
            "enabled": False,
            "include": []
        },
        "rice": {
            "enabled": False,
            "repo": "",
            "include": []
        },
        "backup": {
            "enabled": False,
            "path": "",
            "include": []
        }
    }, indent=4)

    try:
        with open(cfg_path, "x") as c:
            if use_cached:
                copy2(cached_cfg, cfg_path)
            else:
                c.write(default_cfg)

    except FileExistsError:
        print(
            "\033[93m warning:\033[0m file already exists! (", cfg_path, ")",
            "\n\n Trying to set config path environment variable...",
            sep=""
        )

    else:
        print(
            "\n\033[92m Config file created.\n \033[0mPath to config:", cfg_path,
            end="\n"
        )


        with open(cache_path / "declan.log", "a") as l:
            print(
                dt.now(), ": Written config file to ", cfg_path,
                sep="", file=l
            )
        with open(cache_path / (dt.now().strftime('%Y-%m-%d_%H-%M') + ".json"), "w") as c:
            c.write(default_cfg)



    sh = env.get("SHELL")
    if   sh in ["/usr/bin/fish", "/bin/fish"]: sh_cfg_path = ".config/fish/config.fish"
    elif sh in ["/usr/bin/zsh", "/bin/zsh"]:   sh_cfg_path = ".zshrc"
    elif sh in ["/usr/bin/bash", "/bin/bash"]: sh_cfg_path = ".bashrc"

    env_var = dedent(f"""
        # Automatically generated by 'declan init'
        export DECLAN_CONFIG_PATH='{cfg_path}'"""
    )
    with open(f"/home/{user}/{sh_cfg_path}", "a+") as f:
        f.seek(0)
        if "DECLAN_CONFIG_PATH" in f.read(): raise EnvVarExistsError(sh_path)
        else:
            f.write(env_var)
            print(" \033[3m(saved at", sh_cfg_path, "as $DECLAN_CONFIG_PATH)\033[0m", end="\n")



    print(
        "\033[92m\n Initialization complete.\033[0m\n"
        "\033[91m Restart your shell or open a new one before running operations!\033[0m\n"
        " For usage instructions, run 'declan -h' or 'man 1 declan'\n\n"
        "\033[95m Enjoy :V\033[0m"
    )




def clear(cfg_path):
    print(
        "\033[93mwarning:\033[0m this operation nukes declan's data, possibly including:\n",
        " - Your configuration file\n",
        " - Cached files\n",
        " - Declan's environment variable\n",
        "\n\033[91mDeleted files are non-recoverable!",
        sep=""
    )

    if input("\033[35m::\033[0m \033[0mContinue? [Y/n]: ").strip().lower() == "y":
        print(
            "\n\n\033[91mDECLAN CLEAR\n",
            "‾‾‾‾‾‾‾‾‾‾‾‾\033[0m",
            sep=""
        )


        if input("Cache directory: ~/.cache/declan\n\033[35m::\033[0m \033[1mDelete cached files? [Y/n]:\033[0m ").strip().lower() == "y":
            rmtree(f"/home/{user}/.cache/declan/")


        if input("\nEnvironment variable: $DECLAN_CONFIG_PATH\n\033[35m::\033[0m \033[1mWipe environment variable? [Y/n]:\033[0m ").strip().lower() == "y":
            sh = env.get("SHELL")
            if   sh in ["/usr/bin/fish", "/bin/fish"]: sh_cfg_path = ".config/fish/config.fish"
            elif sh in ["/usr/bin/zsh", "/bin/zsh"]:   sh_cfg_path = ".zshrc"
            elif sh in ["/usr/bin/bash", "/bin/bash"]: sh_cfg_path = ".bashrc"

            with open(f"/home/{user}/{sh_cfg_path}", "r") as s:
                sh_cfg_lines = s.readlines()

            for i, line in enumerate(sh_cfg_lines):
                if "# Automatically generated by 'declan" in line:
                    lines_to_rmv = [i, i + 1]
            
            with open(f"/home/{user}/{sh_cfg_path}", "w") as s:
                for i, line in enumerate(sh_cfg_lines):
                    if i not in lines_to_rmv:
                        s.write(line)


        if input(f"\nConfiguration file: {cfg_path}\n\033[35m::\033[0m \033[1mDelete configuration file? [Y/n]:\033[0m ").strip().lower() == "y":
            Path(cfg_path).unlink()




def parse_config(path):
    with open(path, "r") as p:
        try:
            cfg = json.load(p)
        except json.JSONDecodeError as e:
            print(f"\033[91merror:\033[0m invalid JSON formatting: {e.msg.lower()} at line {e.lineno}, character {e.colno}")
            exit(1)

    """
    Data Codes:
        P -> Packages | [1]
        S -> Services | [2]
        G -> Garbage  | [3]
        R -> Rice     | [4]
        B -> Backup   | [5]
    """
    features = ""
    cfg_data = [None, [], [], [], [], []]

    if cfg["packages"]:
        features += "P"
        packages = cfg["packages"]; cfg_data[1] = packages

    if cfg["services"]:
        features += "S"
        services = cfg["services"]; cfg_data[2] = services

    if cfg["gc"]["enabled"]:
        features += "G"
        gc = cfg["gc"]["include"]; cfg_data[3] = gc

    if cfg["rice"]["enabled"]:
        features += "R"
        rice = cfg["rice"]["include"]; repo = cfg["rice"]["repo"]
        cfg_data[4] = [rice, repo]

    if cfg["backup"]["enabled"]:
        features += "B"
        backup = cfg["backup"]["include"]; path = cfg["backup"]["path"]
        cfg_data[5] = [backup, path]

    cfg_data[0] = features
    return cfg_data




def relay_rebuild(packages, services):
    to_remove = set(); to_disable = set() # empty sets

    cached_cfg_path = next(cache_path.glob("*.json"), None) # there should only be one
    try:
        with open(cached_cfg_path, "r") as p:
            cached_cfg = json.load(p)
        use_cached = True

    except TypeError: # if it's None instead of a file
        use_cached = False


    """
    Packages
    """
    if args.operation == "relay":
        # install only what's unique to the current config
        to_install = packages - (set(cached_cfg["packages"]) & packages)
        if to_install:
            print(
                "\033[1mPackages to install:\033[0m\n", '\n'.join(to_install),
                sep="", end="\n\n"
            )

    elif args.operation == "rebuild":
        print("\033[1mPackages to update:\033[0m")

        pending_updates = run(
            ["pacman", "-Quq"], stdout=PIPE
        )
        run(
            # pipe into column with 2+ spaces
            ["column", "-S", "2"], input=pending_updates.stdout
        )

        if pending_updates.stdout: to_install = "updates"
        print()


    if use_cached:
        # remove what's not present anymore
        to_remove = set(cached_cfg["packages"]) - packages
    if to_remove:
        print("\033[1mPackages to remove:\033[0m\n", '\n'.join(to_remove), sep="", end="\n\n")


    """
    Services
    """
    to_enable = services - (set(cached_cfg["services"]) & services) # update services given either operation
    if to_enable:
        print(
            "\033[1mServices to enable:\033[0m\n", '\n'.join(to_enable),
            sep="", end="\n\n"
        )

    if use_cached:
        to_disable = set(cached_cfg["services"]) - services
    if to_disable:
        print(
            "\033[1mServices to disable:\033[0m\n", '\n'.join(to_disable),
            sep="", end="\n\n"
        )



    # short-circuit once something to do is found
    if any(i for i in (to_install, to_enable, to_remove, to_disable)):
        while 1:
            proceed_yn = input(
                "\033[35m::\033[0m Proceed? [Y/n]: "
            ).strip().lower()

            print()

            if proceed_yn in ["y", "n"]:
                if proceed_yn == "n": exit(4)
                break
    else:
        print("there is nothing to do")
        exit(4)


    # start applying changes
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
            # iterate over packages to avoid dangerous removals
            for pkg in to_remove:
                p = Popen(
                    ["sudo", "pacman", "-Rncs", "--noprogressbar", pkg],
                    stdin=PIPE, # pacman reads from python's pipe
                    text=True
                )

                char = stdin.read(2) # declan reads from global stdin

                if char:
                    if char[0].lower() != "y":
                        _, _ = p.communicate() # close the cascading removal
                        print("\033[1;3;32m\nRemoving without cascade...\n\n\033[0m")
                        run(
                            ["yay", "-Rns", "--noconfirm", "--noprogressbar", pkg],
                            stdout=DEVNULL
                        )

                    _, _ = p.communicate() # close the remaining removal


    if to_enable:
        if to_install: print()

        print("Enabling services...", end="\n")

        run(
            ["sudo", "systemctl", "enable", "--now", *to_enable], # don't forget the --now
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
    full_paths = []
    for p in paths:
        hard_path = expanduser(p)

        # only the * wildcard is supported
        if "*" in hard_path:
            globbed_paths = glob(hard_path) # returns a list
            for g in globbed_paths:
                full_paths.append(g) # add everything in the list to the full list

        else:
            full_paths.append(hard_path)

    run(["sudo", "-v"])
    print("\033[90m", end="", flush=True)

    # change to -rfv to debug
    # HACK for https://gitlab.archlinux.org/pacman/pacman/-/work_items/297
    run(["sudo", "rm", "-rf", *full_paths + glob("/var/cache/pacman/pkg/download-*")])

    # Remove orphaned packages
    run(["yay", "-Yc", "--noconfirm", "--noprogressbar"])

    # Remove packaged cache (proper command)
    run(["yay", "-Scc"])


    print("\n\033[92mDone!\033[0m\n")




# pre: no git files in .config, clarify in manpage
def rice(paths, remote):
    remote = "https://github.com/" + remote + ".git" # remote should be user/repo
    dot_config = f"/home/{user}/.config/"


    github_auth = run(
        ["gh", "auth", "status"],
        capture_output=True,
        cwd=dot_config,
        text=True
    )
    if "Logged in" not in github_auth.stdout:
        print("\033[91merror:\033[0m not authenticated to GitHub\nComplete 'gh auth' and retry")
        exit(3)
    else:
        pass


    if args.get:
        rmtree(dot_config + "declan-rice", ignore_errors=True)
        Path(dot_config + "declan-rice").mkdir(exist_ok=True)

        run(["git", "clone", f"{remote[:-4]}", "declan-rice"], cwd=dot_config)

        print("\n\033[92mCopied rice into ~/.config/declan-rice\033[0m" +
              "\nTo overwrite the current rice from inside ~/.config, run 'cp -r declan-rice/* .'")
        exit(0)


    git_status = run(
        ["git", "status"],
        capture_output=True,
        cwd=dot_config,
        text=True
    )
    if "On branch" not in git_status.stdout:
        run(["git", "init"], cwd=dot_config)


    git_remotes = run(
        ["git", "remote", "-v"],
        capture_output=True,
        cwd=dot_config,
        text=True
    )
    if remote not in git_remotes.stdout:
        run(["git", "remote", "add", "origin", remote], cwd=dot_config)


    # stop tracking every file
    run(["git", "rm", "-r", "--cached", "."], stdout=DEVNULL, cwd=dot_config)

    # then add currently listed ones again before committing
    run(["git", "add", *paths], stdout=DEVNULL, cwd=dot_config)
    run(
        ["git", "commit", "-m", f"declan rice commit — {dt.now().strftime('%Y-%m-%d %H:%M')}"],
        stdout=DEVNULL,
        cwd=dot_config
    )


    print("\033[90m", end="", flush=True)
    git_push = run(
        ["git", "push", "-uf", "origin", "main"],
        stdout=PIPE,
        cwd=dot_config,
        text=True
    )
    for l in git_push.stdout.splitlines():
        print(l) # show output of git push

    if "Writing objects" in git_push.stdout:
        print("\n\033[92mDone!\033[0m")
    else:
        print("\033[0mNo changes found, repo up to date", end="")




def backup(paths, location):
    location = expanduser(location) # get hard path

    files = []
    for p in paths:
        files.append(expanduser(p))


    # https://wiki.gentoo.org/wiki/Xz-utils#Usage
    cmp_lvl = input("\033[0mCompression level [1-9]:\033[92m ").strip()
    print("\033[90m")


    wc_size = run(
        ["wc", "-c", *files],
        capture_output=True,
        text=True
    )
    for line in wc_size.stdout.splitlines():
        if "total" in line:
            # e.g.
            # [0]  [1]
            # 1234 file1
            # 4321 file2
            # 5555 total
            size = line.split()[0]

        elif len(wc_size.stdout.splitlines()) < 2:
            size = line.split()[0]

    # backups are large, GB is a good default
    print("Total size to back up:", round(int(size)/1e9, 2), "GB")


    # remove leading slash, avoid warnings and extraction into /
    files = [f[1:] for f in files]

    # -T0 for parallel xz
    options = { "XZ_OPT": f"-T0 -{cmp_lvl}" }

    # tar -I selects the following command in place of a typical compressor (z, J, etc.)
    # in this case, it goes through pv, which calculates progress, and then passes data to xz
    tar = run([
            "sudo", "tar", "-I", f"pv -u shaded -s {size} -w 97 | xz", # -u shaded doesn't work?
            "-cf", location,
            "-C", "/", *files, # look in / but don't store paths without the /
        ],
        env=options,
        text=True,
    )

    print("\n\033[92mBackup complete!\033[0m")




def cache_config(user, home_cfg_path):
    stats = home_cfg_path.stat() # get the config in /home's metadata

    last_mod = dt.fromtimestamp(stats.st_mtime) # last modification time
    date_last_mod = last_mod.strftime("%Y-%m-%d_%H-%M")


    try:
        old_cached_cfg = next(cache_path.glob("*.json"), None)
        old_cached_cfg.unlink()

    except AttributeError: # if .unlink() is applied to None
        pass


    copy2(home_cfg_path, cache_path / (date_last_mod + ".json"))
    # e.g. 2026-07-12_14-41.json




def main():
    if args.operation is None:
        if args.version:
            print(
                logo, " " + version,
                "\n This program may be freely redistributed under the",
                " terms of the GNU General Public License, version 2.0",
                sep="\n", end="\n\n"
            )
            exit(0)


        if args.help:
            print(usage + "\n\nFor more detailed instructions, see 'man declan'")
            exit(0)

        # print usage if no args passed
        else:
            print(usage)
            exit(0)



    if args.gc and args.operation != "rebuild":
        print("\033[91merror:\033[0m option '--gc' can only be used with operation(s): rebuild",
              usage, sep="\n\n")
        exit(3)


    if args.casc and args.operation not in ["relay", "rebuild"]:
        print("\033[91merror:\033[0m option '--casc' can only be used with operation(s): relay, rebuild",
              usage, sep="\n\n")
        exit(3)

    if args.get and args.operation != "rice":
        print("\033[91merror:\033[0m option '--get' can only be used with operation(s): rice",
              usage, sep="\n\n")
        exit(3)



    if args.operation == "init":
        try:
            with open(cache_path / "declan.log", "r") as l:
                file = l.read()

            r"""
            Regex:
                / matches /
                \S+ matches any non-whitespace char
                \. matches .
                json matches json
                e.g.: "foo bar /baz.json
            """
            previous_paths = findall(r"/\S+\.json", file)

            if previous_paths:
                if not Path(previous_paths[-1]).exists():
                    # if the last file logged in declan.log after
                    # being created in init() doesn't exist
                    raise FileNotFoundError

            if "Written config file to" in file:
                raise ConfigAlreadyInitError(safe_getenv("DECLAN_CONFIG_PATH"))

        # if no logfile present
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
            read_cached_yn = ""
            while read_cached_yn not in ["y", "n"]:
                read_cached_yn = input(
                  "\n\033[93mwarning:\033[0m found pre-existing config file in cache\nWould you like to read it? [Y/n]: "
                ).strip().lower()

            if read_cached_yn == "y":
                print(); run(["cat", f"{cached_config}"])

            keep_cached_yn = input("\n\033[35m::\033[0m Would you like to keep this config? [Y/n]: ").strip().lower()
            if keep_cached_yn == "y":
                copy2(cached_config, config_path)

            exit(0)

        else:
            exit(1)



    if args.operation == "clear":
        clear(config_path)



    if args.operation in ["relay", "rebuild"]:
        if which("yay") is None:
            get_yay_yn = input(
                "\033[91merror:\033[0m yay (AUR helper) is not installed\n"
                "Without it, 'relay', 'rebuild', and 'gc' are unavailable:\n\n"
                "\033[35m::\033[0m Would you like to install it now? [Y/n]: "
            ).strip().lower()

            if get_yay_yn == "y":
                run("yay -Y --gendb && yay -Y --devel --save", shell=True)
                run("sudo pacman -S --needed git base-devel", shell=True)
                run(
                    "git clone https://aur.archlinux.org/yay-bin.git && cd yay-bin && makepkg -si",
                    shell=True,
                    cwd=f"/home/{user}/.cache/"
                )
                exit(0)

            else:
                exit(4)


        if "P" in features[0] or "S" in features[0]:
            if "S" not in features[0]:
                relay_rebuild(set(features[1]), set()) # pass in empty sets as stand-ins
            elif "P" not in features[0]:
                relay_rebuild(set(), set(features[2]))
            else:
                relay_rebuild(set(features[1]), set(features[2]))


            # --gc only supports rebuild
            if args.operation == "rebuild" and args.gc:
                garbage_collect(features[3])

            # always cache the config after relay/rebuild
            cache_config(user, config_path)

        else:
            print("there is nothing to do")
            exit(4)



    if args.operation == "gc":
        if which("yay") is None:
            get_yay_yn = input(
                "\033[91merror:\033[0m yay (AUR helper) is not installed\n"
                "Without it, 'relay', 'rebuild', and 'gc' are unavailable:\n\n"
                "\033[35m::\033[0m Would you like to install it now? [Y/n]: "
            ).strip().lower()

            if get_yay_yn == "y":
                run("yay -Y --gendb && yay -Y --devel --save", shell=True)
                run("sudo pacman -S --needed git base-devel", shell=True)
                run(
                    "git clone https://aur.archlinux.org/yay-bin.git && cd yay-bin && makepkg -si",
                    shell=True,
                    cwd=f"/home/{user}/.cache/"
                )
                exit(0)

            else:
                exit(4)

        if "G" in features[0]:
            if not features[3]:
                print("\033[93mwarning:\033[0m no garbage collection paths specified")

            garbage_collect(features[3])
    
        else:
            print("\033[91merror:\033[0m garbage collection disabled in config")
            exit(3)



    if args.operation == "rice":
        if which("gh") is None:
            get_gh_yn = input(
                "\033[91merror:\033[0m the GitHub CLI is not installed\n"
                "Without it, 'rice' is unavailable\n\n"
                "\033[35m::\033[0m Would you like to install it now? [Y/n]: "
            ).strip().lower()

            if get_gh_yn == "y":
                run(["sudo", "pacman", "-S", "github-cli"])
                exit(0)
            else:
                exit(4)

        if "R" in features[0]:
            if not features[4][0]:
                print("\033[91merror:\033[0m no contents of ~/.config specified")
                exit(3)
            else:
                rice(features[4][0], features[4][1])

        else:
            print("\033[91merror:\033[0m ~/.config management disabled in config file")
            exit(3)



    if args.operation == "backup":
        if which("pv") is None:
            get_pv_yn = input(
                "\033[91merror:\033[0m pv (backup progress tracker) is not installed\n"
                "Without it, 'backup' is unavailable\n\n"
                "\033[35m::\033[0m Would you like to install it now? [Y/n]: "
            ).strip().lower()

            if get_pv_yn == "y":
                run(["sudo", "pacman", "-S", "pv"])
                exit(0)
            else:
                exit(4)

        if "B" in features[0]:
            if not features[5]:
                print("\033[91merror:\033[0m no paths to back up")
                exit(3)
            else:
                backup(features[5][0], features[5][1])

        else:
            print("\033[91merror:\033[0m backups disabled in config")
            exit(3)




try:
    main()

except DeclanError as error:
    print(error)

except (KeyboardInterrupt, EOFError):
    print("\n\n\033[91merror:\033[0m execution interrupted by user!")
