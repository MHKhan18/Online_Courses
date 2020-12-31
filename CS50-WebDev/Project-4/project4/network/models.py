from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver 


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name="submissions")
    content = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f'Author : {self.author.username}, \n \
                Content : {self.content}, \n \
                Likes: {self.likes}, \n \
                Created At: {self.created}, \n \
                Last Modified: {self.updated}'

    def serialize(self):
        return {
            'Author ' : self.author.username,
            'Content ' : self.content,
            'Likes ' : self.likes,
            'Created At ' : self.created,
            'Last Modified ': self.updated
        }

    class Meta:
        ordering = ['-created']

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    followers = models.ManyToManyField(User , related_name='following')

# signals to trigger profile creation when a new user is registered
@receiver(post_save , sender=User)
def create_profile(sender , instance , created , **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save , sender=User)
def update_profile(sender , instance , created , **kwargs):
    if not created:
        instance.profile.save() 

class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="likes")
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="likes")

    def __str__(self):
        return f'User: {self.user.username}, \n \
                 Post: {self.post.id}'