import sys
print(f"Python Executable: {sys.executable}")
print(f"Python Path: {sys.path}")

try:
    import pyod
    print(f"PyOD Version: {pyod.__version__}")
    print(f"PyOD File: {pyod.__file__}")
    from pyod.models.ecod import ECOD
    print("ECOD imported successfully")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
