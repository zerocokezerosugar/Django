from distutils.command.upload import upload
from django.db import models
from acc.models import User
# Create your models here.
class Topic(models.Model):
    subject = models.TextField()
    maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="maker")
    content = models.TextField()
    voter = models.ManyToManyField(User, blank=True, related_name="voter")
    pubdate = models.DateTimeField()

    def __str__(self):
        return self.subject

    def summary(self):
        return f"{self.content[0:15]}..."

class Choice(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    chname = models.CharField(max_length=100)
    chpic = models.ImageField(upload_to="vote/%y")
    chcom = models.TextField()

    choicer = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return f"{self.topic}_{self.chname}"

    def getpic(self):
        if self.chpic:
            return self.chpic.url
        return "/media/noimg.png"
        