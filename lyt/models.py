from django.db import models

# Create your models here.
class Images(models.Model):
    # upload_to='user/%y'는 media폴더에 저 경로 추가해서 이미지 저장
    pic = models.ImageField(upload_to="images/")
    # comment 이건 없어도 되는데 그냥 했어 타이틀로 바꿔도되고 빼도돼!
    comment = models.TextField() 

    def getpic(self):
        if self.pic:
            # print(self.pic)
            # print(self.pic.url)
            return self.pic.url
        return "/media/noimage.png"