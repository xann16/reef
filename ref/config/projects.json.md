### TOP-LEVEL LIST OF REGISTERED PROJECTS

Top-level list of all created, imported, or otherwise reef-managed projects (both with in-source and out-of-source config).

```json
{
    "projects":
    {
        [
            "name": "test_project",
            "source_path": "/home/user/repos/reef/rf-cmake-ref-exp",
            "config_path": "/home/user/.reef/projects/test_project",
            "default_module": null
        ]
    }, 
    "default_project": "test_project"
}
```

SETTINGS:

- `default_project` (**STRING**; NULLABLE) - name of project that is used by reef CLI as a default;
- `projects` (**ARRAY**; REQUIRED) - list of all *PROJECTS* currently handled via reef.


*PROJECTS* OBJECTS:

- `name` (**STRING**; REQUIRED) - unique name of a project (as represented in reef);
- `source_path` (**STRING(PATH)**; REQUIRED) - path to the top-level directory that contains project sources;
- `config_path` (**STRING(PATH)**; NULLABLE) - path to project-specific reef config files - used for *out-of-source* reef configs, if not defined or null, the project is assumed to have *in-source*reef config, i.e. configuration filer are assumed to be located in `{{source_path}}/.reef`;
- `default_module` (**STRING**; NULLABLE) - name of module that is used by reef CLI as a default for this project.