class InvalidWktPointArgument(Exception):
    """Raised when the WKT string is not a valid point"""

    pass


class SearchException(Exception):
    """Raised when search endpoint returned a non 200 statuscode"""

    pass
