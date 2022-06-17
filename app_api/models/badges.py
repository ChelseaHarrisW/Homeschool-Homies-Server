from django.db import models

class BadgeType(models.Model):
    label = models.CharField(max_length=50)
    
    #Django creates id for you unlike sql
    # note that in the badge type in the corresponding fixtures module 
    #the "pk" is added to denote the primary key
    #the fields obj is te items that we are filling into the fields from the table that we created when creating
    # #when adding in the seed data through the "fixtures model"