from datetime import datetime
import weakref

class ValidatedProperty:
    def __init__(self, validator=None, default=None):
        self.validator = validator
        self.default = default
        self.name = None  # Will be set by __set_name__
        
    def __set_name__(self, owner, name):
        self.name = f"_{name}"  # Create private storage name
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
            
        # If value isn't set and we have a default, return the default
        value = getattr(instance, self.name, None)
        if value is None and self.default is not None:
            return self.default
        return value
        
    def __set__(self, instance, value):
        if self.validator and value is not None:
            if not self.validator(value):
                raise ValueError(f"Invalid value for {self.name[1:]}")
        setattr(instance, self.name, value)

class UserProfileManager:
    # Class-level cache using weak references
    _profile_cache = weakref.WeakValueDictionary()
    
    # Validators
    def _validate_username(value):
        return isinstance(value, str) and len(value) > 0
        
    def _validate_email(value):
        return isinstance(value, str) and "@" in value and "." in value
    
    # Properties with validation
    username = ValidatedProperty(validator=_validate_username)
    email = ValidatedProperty(validator=_validate_email)
    last_login = ValidatedProperty(default=None)
    
    def __init__(self):
        self._username = None
        self._email = None
        self._last_login = None
    
    @classmethod
    def add_to_cache(cls, profile):
        cls._profile_cache[id(profile)] = profile
    
    @classmethod
    def get_from_cache(cls, profile_id):
        return cls._profile_cache.get(profile_id) 