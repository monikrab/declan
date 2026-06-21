
# TODO:

<!-- DONE: Pass --help when no flags passed -->
<!-- DONE: Tell user to restart shell to load config environment variable after init() -->
<!-- DONE: Add more Arch-based distros to table -->
<!-- DONE: Add Yay install script -->
<!-- DONE: Add not Arch Linux warning -->
<!-- DONE: Add caching to detect which packages have been added and removed since last cache -->
<!-- DONE: Check if config path entered matches one in environment variable -->
<!-- DONE: When file already exists in home, try to set environment variable -->
<!-- DONE: Search for cached config in folder with glob instead of hardcoding path -->


Features:
- Add --version
- Add support for optional GC on rebuild (declan rebuild --clean)
- Add functionalities:
    -> clear
    -> gc
    -> rice (with --push)
    -> backup
- Add cascading removal option to relay/rebuild, which catches "n" and continues with -Rns (--casc)

Internal:
- Search for cached configs during init
- Remove all old cached configs before adding new one
- Add support for CachyOS fish config (not in .config)

Errors:
- ConfigNotExistsError needs to be added
- EnvVarNotExists error for getenv() calls
- Catch JSONDecodeError
