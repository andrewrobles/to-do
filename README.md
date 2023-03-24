# How To Code a Todo List App


### Requirements

Download and install [Git](https://git-scm.com/downloads), [Visual Studio Code](https://code.visualstudio.com/), and [Docker Desktop](https://www.docker.com/). Once Docker Desktop is downloaded, make sure that it is running.

### Project Setup

In a terminal window, run the following commands to download the project to your `Documents` folder:
```bash
cd ~/Documents
git clone https://github.com/andrewrobles/todo.git
```

### Create the Todo Item

With the project opened up in Visual Studio Code, edit the `code/todo/models.py` file so that it looks like this:

```python
from django.db import models

class TodoItem(models.Model):
    text = models.CharField(max_length=200)
```

Run the following command:
```bash
./manage.sh migrate
```

