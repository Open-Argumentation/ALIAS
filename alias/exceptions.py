class _AliasException(Exception):
    """Root for alias exceptions.  Used to define further exceptions.  Never raised"""
    pass

class _ArgumentException(_AliasException):
    pass

class _FrameworkException(_AliasException):
    pass

class _LabellingException(_AliasException):
    pass

class _ParsingException(_AliasException):
    pass

class _DbException(_AliasException):
    pass