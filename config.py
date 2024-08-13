import os


FLUIDFRAME_SCRIPTS_DIR = "src"
FLUIDFRAME_BUILD_DIR = "fluidpack"
FLUIDFRAME_LIB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODE_MODULE = os.path.join(FLUIDFRAME_LIB_DIR, "node_modules")