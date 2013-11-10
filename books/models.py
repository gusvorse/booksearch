from django.db import models

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
	
    def __unicode__(self):
        return self.name
		
    class Meta:
        ordering = ['name', 'city']

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
	
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()
    number_of_reviews = models.IntegerField()
	
    def __unicode__(self):
        return self.title

class Review(models.Model):
    name_of_reviewer = models.CharField(max_length=100)
    book = models.ForeignKey(Book)
    text = models.TextField()
	
    def __unicode__(self):
        return self.name_of_reviewer
