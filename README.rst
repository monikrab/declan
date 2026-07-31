
.. code-block ::

     _____    _______   _____   _          _      _   _
    |  __ \  |  ____/  / ____\ | |        / \    | \ | |
    | |  | | | |___   | /      | |       /   \   |  \| |
    | |  | | |  ___|  | |      | |      /  ∆  \  |     |
    | |__| | | |____  | \____  | |___  /  ___  \ | |\  |
    |_____/  \______\  \_____/ \_____/ \_/   \_/ |_| \_|




Configuration
_____________

.. code-block :: json

    {
        "description": "<user>'s <distro> configuration",

        "packages": [],
    
        "services": [],

        "gc": {
            "enabled": true,
            "include": [
                "~/*"
            ]
        },

        "rice": {
            "enabled": false,
            "remote": "user/repo",
            "include": [
                "app/"
            ]
        },

        "backup": {
            "enabled": true,
            "path": "~/name.tar.xz",
            "include": [
                "~/"
            ]
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

        declan relay    [--casc]
        declan rebuild  [--gc] [--casc]
        declan gc

        declan rice
        declan backup
