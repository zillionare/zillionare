import sys
from pathlib import Path

startup_module = Path("~/workspace/cheese_course/docs/factor-analysis/assets/startup.py").expanduser()
sys.path.append(str(startup_module.parent))
from startup import *
