class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass

class InvalidPasswordException(Exception):
    """Custom exception for invalid password"""
    pass

class UsernameOrEmailExistsException(Exception):
    """Custom exception for existing usesrname"""
    pass

class LLMResponseException(Exception):
    """Custom exception for llm response failures"""
    pass

