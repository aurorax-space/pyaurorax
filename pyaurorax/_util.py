import warnings


def show_warning(message: str, stacklevel: int = 1) -> None:
    """
    This is a helper method for within the library to ensure warnings are displayed. Jupyter notebooks
    within VSCode suppress warnings by default, so this way ensures that they are shown.

    NOTE: This is a private method only meant for use within the library.
    """
    warnings.simplefilter("always", UserWarning)
    warnings.warn(message, UserWarning, stacklevel=stacklevel)
    warnings.resetwarnings()
