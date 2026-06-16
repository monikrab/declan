
# TODO:

<!-- DONE: Pass --help when no flags passed -->
<!-- DONE: Tell user to restart shell to load config environment variable after init() -->
<!-- DONE: Add more Arch-based distros to table -->

- Add support for optional GC on rebuild (declan rebuild --clean)
- Add searching for cached configs during init
- Add generic "repo" key (becomes "repo/pkg")
- Add non-specified (default for package) repo list to "packages":
- Add caching to detect which packages have been added and removed since last cache
- Add cascading removal option to relay/rebuild, which catches "n" and continues with -Rns (--casc)
- Add Yay install script
- Add functionalities:
    -> clear
    -> gc
    -> rice (with --push)
    -> backup

- ConfigNotExistsError needs to be added
- Search for cached config in folder with glob instead of hardcoding path
- Remove all old cached configs before adding new one
- Add not Arch Linux warning

- Add support for editing CachyOS fish config (not in .config)

- When file already exists in home, try to set environment variable
- Check if config path entered matches one in environment variable
