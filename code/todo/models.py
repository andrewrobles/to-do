from django.db import models

class TodoItem(models.Model):
    text = models.CharField(max_length=200)
    done = models.BooleanField(default=False)

    @property
    def striked_text(self):
        return ''.join([letter + '\u0336' for letter in self.text])
    
    def __str__(self):
        return self.text if not self.done else self.striked_text