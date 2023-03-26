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

By running **makemigrations**, you're telling Django that you've made some changes to your models (in this case, you've made new ones) and that you'd like the changes to be stored as a *migration*.

Migrations are how Django stores changes to your models (and thus your database schema) - they're files on disk. You can read the migration for your model if you like; it's the file **todo/migrations/0001_initial.py**. Don't worry, you're not expected to read them every time Django makes one, but they're designed to be human-editable in case you want to manually tweak how Django changes things.

There's a command that will run the migrations for you and manage your database schema automatically - that's called **migrate**.

Now, run **migrate** again to create those model tables in your database:

```bash
./manage.sh migrate
```

You should see something similar to the following:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, todo, sessions
Running migrations:
  Rendering model states... DONE
  Applying todo.0001_initial... OK
```

The **migrate** command takes all the migrations that haven't been applied (Django tracks which ones are applied using a special table in your database called **django_migrations**) and runs them against your database - essentially, synchronizing the changes you made to your models with the schema in the database.

Migrations are very powerful and let you change your models over time, as you develop your project, without the need to delete your database or tables and make new ones - it specializes in upgrading your database live, without losing data. We’ll cover them in more depth in a later part of the tutorial, but for now, remember the three-step guide to making model changes:

- Change your models (in `models.py`).
- Run `python manage.py makemigrations` to create migrations for those changes
- Run `python manage.py migrate` to apply those changes to the database.

The reason that there are separate commands to make and apply migrations is because you’ll commit migrations to your version control system and ship them with your app; they not only make your development easier, they’re also usable by other developers and in production.


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

Run `./manage.sh shell` again:

```python
# Make sure our __str__() addition worked.
>>> TodoItem.objects.all()
<QuerySet [<TodoItem: Go to the gym>]>
```

Let’s update the contents of `code/todo/models.py` to:

```python
from django.db import models

class TodoItem(models.Model):
    text = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    @property
    def striked_text(self):
        STRIKE_CHARACTER = '\u0336' 
        new_text = ''
        for letter in self.text:
            new_text = new_text + letter + STRIKE_CHARACTER
        return new_text
    
    def __str__(self):
        if self.done == True:
            return self.striked_text
        else:
            return self.text
```

Save these changes and start a new Python interactive shell by running `./manage.sh shell` again:

```python
>>> from todo.models import TodoItem

# Make sure our custom method worked.
>>> t = TodoItem.objects.get(id=1)
>>> t.striked_text
G̶o̶ ̶t̶o̶ ̶t̶h̶e̶ ̶g̶y̶m̶

# Request an ID that doesn't exist, this will raise an exception.
>>> TodoItem.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: TodoItem matching query does not exist.

# Create three todo items. The create call constructs a new
# TodoItem object, and saves to the database in one step
>>> TodoItem.create(text='Cook dinner', done=True)
<TodoItem: Cook dinner>
>>> TodoItem.create(text='Take out the trash', done=True)
<Choice: Take out the trash>

# Another useful function is the ability to filter objects by its attributes:
# First show all todo items
>>> TodoItem.objects.all()
<QuerySet [<TodoItem: G̶o̶ ̶t̶o̶ ̶g̶y̶m̶>, <TodoItem: Cook dinner>, <TodoItem: Take out the trash>]>

# Filter todo items by those marked as done
>>> TodoItem.filter(done=True)
<QuerySet [<TodoItem: G̶o̶ ̶t̶o̶ ̶g̶y̶m̶>]>
```
