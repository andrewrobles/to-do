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
./manage.sh makemigrations
```

You should see something similar to the following:
```
Migrations for 'todo':
  todo/migrations/0001_initial.py
    - Create model TodoItem
```

Now, run **migrate** to create those model tables in your database:

```bash
./manage.sh migrate
```

### Playing with the API

Now, let’s hop into the interactive Python shell and play around with the free API Django gives you. To invoke the Python shell, use this command:

```bash
./manage.sh shell
```

Once you’re in the shell, explore the database API:

```python
>>> from todo.models import TodoItem  # Import the model classes we just wrote.

# No todo items are in the system yet.
>>> TodoItem.objects.all()
<QuerySet []>

# Create a new TodoItem.
>>> t = TodoItem(text="Go for a run", done=False)

# Save the object into the database. You have to call save() explicitly.
>>> t.save()

# Now it has an ID.
>>> t.id
1

# Access model field values via Python attributes.
>>> q.text
"Go for a run"

# Change values by changing the attributes, then calling save().
>>> q.text = "Go to the gym"
>>> q.save()

# objects.all() displays all the todo items in the database.
>>> TodoItem.objects.all()
<QuerySet [<TodoItem: TodoItem object (1)>]>
```