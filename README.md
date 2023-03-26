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
    done = models.BooleanField(default=False)
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

Wait a minute. `<TodoItem: TodoItem object (1)>` isn’t a helpful representation of this object. Let’s fix that by editing the `TodoItem` model (in the ``code/todo/models.py`` file) and adding a `__str__()` method to `TodoItem`:

```python
from django.db import models

class TodoItem(models.Model):
    # ...
    def __str__(self):
        return self.text
```

It’s important to add `__str__()` methods to your models, not only for your own convenience when dealing with the interactive prompt, but also because objects’ representations are used throughout Django’s automatically-generated admin.

Run `./manage.sh shell` so that we can see if our `__str__()` method worked:

```python
>>> TodoItem.objects.all()
<QuerySet [<TodoItem: Go to the gym>]>
```

Let’s also add a custom method to this `code/todo/models.py`:


```python
from django.db import models

class TodoItem(models.Model):
    # ...
    @property
    def striked_text(self):
        return ''.join([letter + '\u0336' for letter in self.text])
```

Save these changes and start a new Python interactive shell by running `./manage.sh shell` again:

```python
>>> from todo.models import TodoItem

# Make sure our __str__() addition worked.

>>> TodoItem.objects.all()
<QuerySet [<TodoItem: Go to the gym>]>

# Django provides a rich database lookup API that's entirely driven by
# keyword arguments.
>>> TodoItem.objects.filter(id=1)
<QuerySet [<TodoItem: Go to the gym>]>
>>> TodoItem.objects.filter(text__startswith='Go')
<QuerySet [<TodoItem: Go to the gym>]>

# Request an ID that doesn't exist, this will raise an exception.
>>> TodoItem.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: TodoItem matching query does not exist.

# Make sure our custom method worked.
>>> t = TodoItem.objects.get(id=1)
>>> t.striked_text
G̶o̶ ̶t̶o̶ ̶t̶h̶e̶ ̶g̶y̶m̶

# Create three todo items. The create call constructs a new
# TodoItem object, and saves to the database in one step
>>> TodoItem.create(text='Cook dinner', done=False)
<TodoItem: Cook dinner>
>>> TodoItem.create(text='Take out the trash', done=False)
<Choice: Take out the trash>
>>> TodoItem.create(text='Do laundry', done=False)
```
