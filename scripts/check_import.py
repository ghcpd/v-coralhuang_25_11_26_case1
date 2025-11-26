import sys, os
sys.path.insert(0, os.path.abspath(os.getcwd()))
print('cwd:', os.getcwd())
print('sys.path[0]:', sys.path[0])
print('exists user_display_optimized.py:', os.path.exists('user_display_optimized.py'))
try:
    import user_display_optimized
    print('Imported OK')
except Exception as e:
    print('Import failed:', type(e).__name__, e)
    sys.exit(2)
