### Initialization:
`~/.local/bin/sqlacodegen --outfile utils/db/models.py mysql+pymysql://root:secret@127.0.0.1:3306/example`

###### Generated source code:
```
...
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

...
```
