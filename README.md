# How To Code a Todo List App


Edit the `code/todo/models.py` file so it looks like this:

```python
from django.db import models

class TodoItem(models.Model):
    text = models.CharField(max_length=200)
```

Run the following command:
```bash
./manage.sh migrate
```

