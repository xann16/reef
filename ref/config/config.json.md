### TOP-LEVEL CONFIG

Basic config set in top-level *reef* settings directory.

```json
{
    "config_path": "/home/user/.reef",
    "exec_path": "/home/user/repos/reef/rf-exp",
    "version": "0.1.0"
}
```

SETTINGS:

- `config_path` (**STRING(PATH)**; REQUIRED) - path to the directory containing top-level config file (i.e. this file);
- `exec_path` (**STRING(PATH)**; REQUIRED) - path to the directory containing executable (script) for reef currently in use;
- `version` (**STRING(VERSION)**; REQUIRED) - version number (*semver*) of currently used reef.
