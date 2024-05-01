"""It will allow to change storage type
directly by using an environment variable
"""

import os
if 'HBNB_TYPE_STORAGE' in os.environ.keys():
    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        from models.engine.db_storage import DBStorage
        storage = DBStorage()
        storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
