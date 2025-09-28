# Placeholder for service classes
# Example: UserService, AuthService, etc.

class BaseService:
    """Base service class with common methods."""
    
    def __init__(self):
        pass
    
    @staticmethod
    def paginate_query(query, page=1, per_page=20):
        """Paginate a SQLAlchemy query."""
        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )