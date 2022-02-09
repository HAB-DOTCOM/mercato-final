from django.db import models
from category.models import catagory
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count

# Create your models here.
class Product(models.Model):
	product_name     =  models.CharField(max_length=200,unique=True)
	slug        =  models.SlugField(max_length=200,unique=True)
	description =  models.TextField(max_length=500,blank=True)
	price       =  models.IntegerField()
	image       =  models.ImageField(upload_to='photos/Product')
	stock       =  models.IntegerField()
	is_available=  models.BooleanField(default=True)
	catagory    =  models.ForeignKey(catagory,on_delete=models.CASCADE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)
 	
	def __str__(self):
		
 		return self.product_name

	def get_url(self):
		return reverse('product_detial',args=[self.catagory.slug,self.slug])

	def averageReview(self):
		reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
		avg = 0
		if reviews['average'] is not None:
			avg = float(reviews['average'])
		return avg


	def countReview(self):
		reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
		count = 0

		if reviews['count'] is not None:
			count = int(reviews['count'])
		return count
        

class VariationManager(models.Manager):
	def colors(self):
		return super(VariationManager,self).filter(varation_category='color',is_active=True)
	def sizes(self):
		return super(VariationManager,self).filter(varation_category='size',is_active=True)
varation_category_choice =(
	('color', 'color'),
	('size', 'size'),

	)

class Variation(models.Model):
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	varation_category = models.CharField(max_length=100,choices= varation_category_choice)
	varation_value = models.CharField(max_length=100)
	is_active  = models.BooleanField(default=True)
	created_date = models.DateTimeField(auto_now = True)
	objects = VariationManager()

	def __str__(self):
		return self.varation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/images/gallery/')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
