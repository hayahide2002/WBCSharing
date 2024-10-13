from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)  # グループ名は一意
    members = models.ManyToManyField(User, related_name='custom_groups')  # 逆参照名を 'custom_groups' に設定

    def __str__(self):
        return self.name

class WellBeingCard(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cards/')

    def __str__(self):
        return self.name

class CardSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    selected_cards = models.ManyToManyField(WellBeingCard)

    def __str__(self):
        return f'{self.user.username} - {self.group.name}'