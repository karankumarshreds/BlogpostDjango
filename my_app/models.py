from django.db import models
from django.contrib.auth.models import  User
from PIL import Image


class Search(models.Model):
    search = models.CharField(max_length=100),
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.search


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    status = models.TextField(max_length='200')

    def __str__(self):
        return self.user.username
    
    def save(self):
        #call the save function to save image/changes
        #using the super function
        super().save()
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300 :
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)





