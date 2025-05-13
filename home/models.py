from django.db import models



class Student(models.Model):
    stu_id = models.CharField(max_length=112,null=True,blank=True)
    name = models.CharField(max_length=250)
    dob = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    
    def __str__(self):
        return self.name
    
    
    
#Following DRF SERIALIZER

class Author(models.Model):
    name = models.CharField(max_length=255)


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()    

class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='book_author',null=True,blank=True)
    publishers = models.ManyToManyField(Publisher, related_name='book_publisher')
    price = models.FloatField()
    pages = models.IntegerField()
