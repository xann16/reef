### TOP-LEVEL REEF CONFIG FILE FOR A PROJECT

Top-level configuration file for a reef project.

```json
{
    "name": "project_name",
    "name_short": "pname",
    "default_language": "cpp",
    "cmake":
    {
        "version_required": "3.21"
    },
    "details":
    {
        "descripton": "A sample project.",
        "homepage": "http://www.example.com/"
    },
    "languages":
    {
        "cpp":
        {
            "standard": "c++20",
            "allow_extensions": false
        }
    },
    "modules": "...",
    "advanced":
    {
        "compile_commands_export_policy": "auto"
    },
    "temp":
    {
        "version": "0.1.0",
        "build": 
        {
            "mode": "default"
        },
        "hierarchy":
        {
            "type": "default",
            "is_multiproject": true,
            "separate_public_includes": true
        }
    }
}
```

SETTINGS:

- `name` (**STRING**; REQUIRED) - full name of the project;
- `name_short` (**STRING**; NULLABLE) - short name of the project (if null, defaults to `name`)
- `default_language` (**STRING(LANG)**; NULLABLE) - language used as a default for projects without explicit language defined (defaults to `cpp`)

*CMAKE* OBJECT:

- `version_required` (**STRING(VERSION)**, NULLABLE) - required version of CMake being used (defaults to minimal version required by Reef or given project in particular);

*DETAILS* OBJECT:

- `description` (**STRING**, NULLABLE) - more verbose description of a project;
- `homepage` (**STRING(URI)**; NULLABLE) - an URI to the project's homepage;

*LANGUAGES.CPP* OBJECT:

- `standard` (**STRING(CPP_STANDARD)**, NULLABLE) - default C++ standard used for the project;
- `allow_extensions` (**BOOLEAN**, NULLABLE) - indicates whether non-standard C++ extensions are allowed (defaults to false)

*MODULES* OBJECTS - defined in `module.json.md`
*ADVANCED* OBJECT:

- `compile_commands_export_policy` (**STRING**, NULLABLE) - may be either: `never` (do net export commands as json, may cause errors with options that require it); `auto` (export commands if needed; default setting); `always` (commands are always exported)

*TEMP* OBJECT:

- `version` (**STRING(VERSION)**, NULLABLE) - constant version string for now (defaults to `0.1.0`) - **TODO:** handle different versioning paterns (e.g. SemVer) and policies (from file/git/etc);

*TEMP.BUILD* OBJECT:

- `mode` (**STRING**, NULLABLE) - **TODO:** handle in-source and out-of-source builds; different output paths, etc.

*TEMP.HIERARCHY* OBJECT:

 - `type` (**STRING**, NULLABLE) - **TODO:** handle different file structures - check what is that default for now, detailed options
 - `is_multiproject` (**BOOLEAN**, NULLABLE) - defaults is `true`; **TODO:** handle singular projects;
 - `separate_public_includes` (**BOOLEAN**, NULLABLE) - **TODO:** handle different header file strategies (for C++); move to language-specific options (?)
