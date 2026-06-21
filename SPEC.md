
<!-- DONE: -->
## INIT
1. Prints welcome message and asks user for config name
2. Gets the username
3. Checks what distro the user is on
  3.1. If the distro is not listed, exit with an error

4. Tries to create and write the config file 
  4.1. If a config of the same name exists, warn the user and check if env-var exists
    4.1.1. If it doesn't, create the config, write it to a logfile, and write a copy to .cache

5. Check which shell the user uses
6. Look for an environment variable with the config path in their shell config
  6.1. If it already exists, tell user to make sure it matches the current config's path
  6.2. If it doesn't, write the variable

7. Tell the user to restart their shell before using the program 

Post:
  - Config created at ~/
  - Logfile exists at ~/.cache/declan
  - Copy of default config exists at ~/.cache/declan with date of init



<!-- DONE: -->
## PARSE_CONFIG
Pre:
- Config file exists

1. Opens config file for reading
2. Creates a data structure (nested 6-list) for parsed config data
3. Records enabled features in a coded string (e.g. "PS" - packages, services)
4. Records the config's values to their respective index in the parsed list, from 1-5 (e.g. [1] = "vim")
5. Puts the coded string in index 0 of the list
6. Returns the full list

Post:
- Everything is parsed correctly, as specified



## RELAY_REBUILD
Pre:
- There exist packages or services to act on
- There's a cached configuration file from the previous run or init()

1. Parses packages and services to enable from cached list
2. If the operation is relay, find out if there are any packages to act on
  2.1. If there are, list the packages to install and make a list of those to remove by subtracting the new list from the old

3. If the operation is rebuild, get out of date packages (-Quq), pipe them into `column`, and list them
4. If there are packages to remove, list them

2. Subtracts items in cached list from current list, makes a list of packages to remove
3. Given what is listed, tell the user which packages and services are to be added and removed
4. Prompt the user to proceed



## MAIN
1. If no operation is passed
  <!-- TODO: 1.1. Print version if --version -->
  1.2. Print usage if --help or no flags passed
  
2. If operation is init
  2.1. Check in logfile if config has been initialized
    2.1.1. If yes, exit with error
    2.1.2. If not, init()
      
3. If any other operation, parse config

4. If operation is `relay` or `rebuild` 
  4.1. Check if Yay is installed
    4.1.1. If not, install it
  4.2. If there are no packages or services to act on, tell the user and exit
    4.2.1. Else, relay() or rebuild()
