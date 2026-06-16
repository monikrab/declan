
- INIT
Checks if config of the same name exists
Creates a config file in ~/
Writes config filename to .cache (silently)
Checks environment variable
Warns about mismatch between env-var and chosen path, tell user how to make them match
Creates an environment variable to match
Caches default config in .cache (important)
Tells user to restart shell to use operations



<!-- DONE: -->
- PARSE_CONFIG
Opens config file for reading
Creates a list for parsed config data
Adds all enabled features to code (e.g. "PS" - packages, services)
Records the config's values to their respective index in the parsed list, from 1-5
Makes the code index 0
Returns the full list



- RELAY_REBUILD
Subtracts items in cached list from current list
Checks if there are any packages and services to act on, if not warn the user & exit




- MAIN
Print version if --version
Print usage if --help or no flags passed
Check initialization history in logfile
Init config if user calls init and there's no init history
If any other operation, parse config
