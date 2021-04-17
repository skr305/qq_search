from django.db import models

class Account(models.Model):
    QQNum = models.IntegerField()
    Nick = models.CharField(max_length=80)
    Age = models.IntegerField()
    Gender = models.IntegerField()
    Auth = models.IntegerField()
    QunNum = models.IntegerField()

    def __str__(self):
        return str({
            'QQNum':self.QQNum,
            'Nick':self.Nick,
            'Age':self.Age,
            'Gender':self.Gender,
            'Auth':self.Auth,
            'QunNum':self.QunNum
        })