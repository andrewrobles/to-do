# How To Code a Todo List App


### Project Setup
- Download and install [Git](https://git-scm.com/downloads), [Visual Studio Code](https://code.visualstudio.com/), and [Docker Desktop](https://www.docker.com/)
- In a terminal window, run the following commands to download the project to your `Documents` folder:

    ```bash
    cd ~/Documents
    git clone https://github.com/andrewrobles/todo.git
    ```

- Enable auto save by going to `File > Auto Save`
- Open up the project in Visual Studio Code by drag by going to `File > Open` and navigating to `~/Documents/todo`
- Open up a terminal window by going to `View > Terminal`
- Start the project by running `docker-compose up` and opening the URL provided in the terminal output.

### Create the TodoItem Model

In the `code/todo/models.py` file we define all objects called `Models` - this is a place in which we will define our todo item.

Let's open the `code/todo/models.py` in the code editor, remove everything from it, and write code like this:

```python
from django.db import models

class TodoItem(models.Model):
    text = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
```

All lines starting with `from` or `import` are lines that add some bits from other files. So instead of copying and pasting the same things in every file, we can include some parts with `from ... import ...`.

`class TodoItem(models.Model):` - this line defines our model.
- `class` is a special keyword that indicates that we are defining an object.
- `TodoItem` is the name of our model. We can give it a different name (but we must avoid special characters and whitespace). Always start a class name with an uppercase letter.
- `models.Model` means that the TodoItem is a Django Model, so Django knows that it should be saved in the database.

Now we define the properties we were talking about: `text` and `done`. To do that we need to define the type of each field (Is it text? A number? A date? A relation to another object, like User?)

- `models.CharField` - this is how you define text with a limited number of characters.
- `models.BooleanField` - this is for values that can either be `True` or `False`.


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

By running `makemigrations`, you're telling Django that you've made some changes to your models (in this case, you've made new ones) and that you'd like the changes to be stored as a *migration*.

Migrations are how Django stores changes to your models (and thus your database schema) - they're files on disk. You can read the migration for your model if you like; it's the file `todo/migrations/0001_initial.py`. Don't worry, you're not expected to read them every time Django makes one, but they're designed to be human-editable in case you want to manually tweak how Django changes things.

There's a command that will run the migrations for you and manage your database schema automatically - that's called `migrate`.

Now, run `migrate` again to create those model tables in your database:

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

The `migrate` command takes all the migrations that haven't been applied (Django tracks which ones are applied using a special table in your database called `django_migrations`) and runs them against your database - essentially, synchronizing the changes you made to your models with the schema in the database.

If you ever want to make future changes to your `models.py` file again, remember the three-step guide to making model changes:

- Change your models (in `models.py`).
- Run `python manage.py makemigrations` to create migrations for those changes
- Run `python manage.py migrate` to apply those changes to the database.

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
