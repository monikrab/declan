
<!-- DONE: -->
## INIT
1. Checks if config of the same name exists
  1.1. If not, creates a config file in ~/
2. Writes logfile of the same name to .cache (silently)
3. Checks if config path environment variable exists
  3.1. If there's mismatch between env-var and chosen path, tell user to make them match and how
  3.2. If it doesn't, creates an environment variable to match
4. Caches default config in .cache (name == dt.now())
5. Tells user to restart shell to use operations

Post:
  - Config created at ~/
  - Logfile exists at ~/.cache with date of init
  - Copy of default config exists at ~/.cache



<!-- DONE: -->
## PARSE_CONFIG
Pre:
- Config file exists

1. Opens config file for reading
2. Creates a data structure (nested list) for parsed config data
3. Records enabled features in a coded string (e.g. "PS" - packages, services)
4. Records the config's values to their respective index in the parsed list, from 1-5 (e.g. [1] = "vim")
5. Puts the coded string in index 0 of the list
6. Returns the full list

Post:
- Everything is parsed correctly, as specified


- RELAY_REBUILD
Subtracts items in cached list from current list
Checks if there are any packages and services to act on, if not warn the user & exit




- MAIN
Print version if --version
Print usage if --help or no flags passed
Check initialization history in logfile
Init config if user calls init and there's no init history
If any other operation, parse config
