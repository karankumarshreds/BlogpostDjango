from django.db import models
from django.contrib.auth.models import  User
from PIL import Image
from django.urls import reverse

class Post(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    content     = models.TextField(max_length=600)
    date        = models.DateTimeField(auto_now=True)
    likes       = models.ManyToManyField(User, blank=True, related_name='post_likes')

    ################################################
    ####  This will fetch the url 'post_detail' ####
    ####  and take the 'pk' value and get the   ####
    ####  object with that pk  and  pass it to  ####
    ####     to the classView with object       ####
    ################################################  
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    def instance(self):
        return self.user

class Likes(models.Model):
    # user = models.ManyToManyField(User)
    # count = models.IntegerField(default=0)
    liked_posts = models.IntegerField()


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






