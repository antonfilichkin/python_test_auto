import time
import importlib
from __shared__ import pages_to_parse


scripts_to_execute = {
    'Async': 'hw9_async',
    'Multithread': 'hw9_multithread',
    'Sync': 'hw9_sync'
}


for name, script in scripts_to_execute.items():
    start = time.time()
    total = getattr(importlib.import_module(script), "execute")(pages_to_parse())
    end = time.time()
    print(f'{name} - parsed [{total}] companies execution time: {end - start:.2f} seconds.')
