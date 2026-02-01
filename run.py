#!/usr/bin/env python3
"""
IWS-WinCare - Main entry point.
"""

import sys
from pathlib import Path

root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from src.app import main

if __name__ == '__main__':
    sys.exit(main())
