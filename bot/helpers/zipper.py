"""ZIP packaging utility for playlist / gallery downloads."""

import os
import zipfile


def create_zip(file_paths: list[str], zip_path: str) -> str:
    """Create a ``.zip`` archive from *file_paths*.

    Each file is stored using only its basename (no directory prefix) so
    the archive is flat and easy to extract.

    Returns the *zip_path* on success.
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for fpath in file_paths:
            if os.path.isfile(fpath):
                zf.write(fpath, arcname=os.path.basename(fpath))
    return zip_path
