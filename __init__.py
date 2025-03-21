"""
Ensure file_extraction can be imported as a module
"""

import os

if "FILE_EXTRACTION_HOME" not in os.environ:
    # find sensible default
    os.environ["FILE_EXTRACTION_HOME"] = os.path.dirname(__file__)
