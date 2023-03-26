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