from django.db import models

# Create your models here.
class App(models.Model):
    name = models.CharField(max_length=255)
    code = models.TextField()
    
    def __unicode__(self):
    	return self.name
