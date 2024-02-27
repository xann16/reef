class ProjectAdvancedSettings():
    '''
    Contains advanced project settings.
    '''

    _COMPILE_COMMANDS_EXPORT_POLICIES = ['auto', 'never', 'always']

    def __init__(self,
                 obj, *,
                 compile_commands_export_policy=None):
        '''
        Constructs ProjectAdvancedSettings object from item dictionary or manual property value overrides.
        '''
        self.compile_commands_export_policy = compile_commands_export_policy if compile_commands_export_policy is not None else (obj['compile_commands_export_policy'] if 'compile_commands_export_policy' in obj else None)
        
    @property
    def compile_commands_export_policy(self):
        ''' Policy for exporting 'compile_commands.json' file. '''
        return self._compile_commands_export_policy if self._compile_commands_export_policy is not None else self._COMPILE_COMMANDS_EXPORT_POLICIES[0]
    
    @compile_commands_export_policy.setter
    def compile_commands_export_policy(self, compile_commands_export_policy):
        ''' Policy for exporting 'compile_commands.json' file. '''
        if compile_commands_export_policy is not None:
            if not isinstance(compile_commands_export_policy, str):
                raise ValueError("'compile_commands_export_policy' property must be a string.")
            if not compile_commands_export_policy:
                raise ValueError("'compile_commands_export_policy' property cannot be an empty string.")
            if compile_commands_export_policy not in self._COMPILE_COMMANDS_EXPORT_POLICIES:
                raise ValueError(f"'compile_commands_export_policy' cannot be '{compile_commands_export_policy}' (supported values include: {', '.join(self._COMPILE_COMMANDS_EXPORT_POLICIES)} ).")
        self._compile_commands_export_policy = compile_commands_export_policy

    def to_dict(self):
        ''' Returns ProjectAdvancedSettings as a dictionary with its properties (convenient for conversion to JSON). '''
        result = {}
        
        if self._compile_commands_export_policy is not None:
            result['compile_commands_export_policy'] = self.compile_commands_export_policy
        
        return result if any(result) else None
    
