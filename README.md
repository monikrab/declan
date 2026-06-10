
``` _____    _______   _____   _          _      _   _
|  __ \  |  ____/  / ____\ | |        / \    | \ | |
| |  | | | |___   | /      | |       /   \   |  \| |
| |  | | |  ___|  | |      | |      /  ∆  \  |     |
| |__| | | |____  | \____  | |___  /  ___  \ | |\  |
|_____/  \______\  \_____/ \_____/ \_/   \_/ |_| \_|


Declarative system configuration for
Arch and Arch-based Linux distributions
```


## &nbsp;
## Configuration

```
{
    "description": "<user>'s <distro> configuration",

    "packages": [],
    
    "services": [],

    "gc": {
        "enabled": true/false,
        "clean": []
    },

    "configs": {
        "enabled": true/false,
        "include": []
    },

    "backup": {
        "enabled": true/false,
        "include": []
    }
}
```


## &nbsp;
## Usage

```
declan <operation> [...]

operations:
declan {-h | help}
declan {-v | version}
declan init
declan clear
declan relay
declan rebuild    [ clean ]
declan gc         [cascade]
declan rice       [ -push ]
declan backup
```
