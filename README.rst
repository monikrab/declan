
.. code-block ::

     _____    _______   _____   _          _      _   _
    |  __ \  |  ____/  / ____\ | |        / \    | \ | |
    | |  | | | |___   | /      | |       /   \   |  \| |
    | |  | | |  ___|  | |      | |      /  ∆  \  |     |
    | |__| | | |____  | \____  | |___  /  ___  \ | |\  |
    |_____/  \______\  \_____/ \_____/ \_/   \_/ |_| \_|

    Declarative system configuration for
    Arch and Arch-based Linux distributions




Configuration
_____________

.. code-block :: json

    {
        "description": "<user>'s <distro> configuration",

        "packages": [],
    
        "services": [],

        "gc": {
            "enabled": true/false,
            "include": [
                "~/directory/*"
                "/directory/file"
            ]
        },

        "config": {
            "enabled": true/false,
            "include": []
        },

        "backup": {
            "enabled": true/false,
            "include": []
        }
    }


Usage
_____

.. code-block ::

    declan <operation> [options]

    operations:
        declan {-h | --help}
        declan {-v | --version}

        declan init
        declan clear

        declan relay    [--gc] [--casc]
        declan rebuild  [--gc] [--casc]
        declan gc

        declan rice     [--push]
        declan backup
