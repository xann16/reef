class ProjectManager():

    def __init__(self):
        """
            ctor
        """
        pass

    def info(self):
        """
            info
        """
        pass

    def get_list(self):
        """
            get_list
        """
        pass

    def describe(self, project_name=None):
        """
            describe
        """
        pass

    def create(self, project_name, project_template_name, base_path):
        """
            create
        """
        pass

    def import_from(self, base_path, project_name=None):
        """
        import
        """
        pass

    def refresh(self, project_name=None):
        """
            refresh
        """
        pass

    def delete(self, project_name, are_files_removed=False):
        """
            delete
        """
        pass

    def get_default(self):
        """
            get_default
        """
        pass

    def set_default(self, project_name):
        """
            set_default
        """
        pass

    def get_default_module(self, project_name):
        """
            get_default_module
        """
        pass

    def set_default_module(self, module_name, project_name=None):
        """
            set_default_module
        """
        pass

    def config_get_entry(self, key, project_name=None):
        """
            config_get_entry
        """
        pass

    def config_set_entry(self, key, value, project_name=None):
        """
            config_set_entry
        """
        pass

    def config_list_entries(self, key, project_name=None):
        """
            config_list_entries
        """
        pass

    def config_reset_entry(self, key, project_name=None):
        """
            config_reset_entry
        """
        pass

    def config_add_entry_item(self, key, value, project_name=None):
        """
            config_add_entry_item
        """
        pass

    def config_remove_entry_item(self, key, value, project_name=None):
        """
            config_remove_entry_item
        """
        pass

    def config_clear_entry_items(self, key, project_name=None):
        """
            config_clear_entry_items
        """
        pass
