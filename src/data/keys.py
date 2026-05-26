from __future__ import annotations
import os
from dotenv import load_dotenv

# load in .env
load_dotenv()

PREVIEW_KEY = os.getenv("PREVIEW_KEY")

# for import
__all__ = [
    "PREVIEW_KEY"
]