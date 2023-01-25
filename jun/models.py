from django.db import models

# Create your models here.
class Img(models.Model):
    date = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='images/')

    def getpic(self):
        if self.pic:
            return self.pic.url
        return "/media/noimage.png"