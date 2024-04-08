class UnificationError(Exception):
    """Exception raised when type unification fails."""
    pass

class OccursError(Exception):
    """Exception raised when unification would produce infinite type ."""
    pass
