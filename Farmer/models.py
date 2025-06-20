from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Products(models.Model):
    name=models.CharField(max_length=50)
    price=models.FloatField()
    product_image=models.ImageField(upload_to="Products")
    offer=models.BooleanField(default=False)
    description=models.TextField(null=True)

class Crop(models.Model):
    Nitrogen=models.CharField(max_length=70)
    Phosphorous=models.CharField(max_length=70)
    Potassium=models.CharField(max_length=70)
    Temperature=models.CharField(max_length=70)
    PH=models.CharField(max_length=70)
    Humidity=models.CharField(max_length=70)
    Rainfall=models.CharField(max_length=70)
    Recommend_Crop=models.CharField(max_length=70)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class CropRecommendationLog(models.Model):
    n = models.FloatField()
    p = models.FloatField()
    k = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    recommended_crop = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recommended_crop} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']

class AddCropData(models.Model):
    n = models.IntegerField(verbose_name='Nitrogen')
    p = models.IntegerField(verbose_name='Phosphorus')
    k = models.IntegerField(verbose_name='Potassium')
    temperature = models.FloatField(help_text='Temperature in Celsius')
    humidity = models.FloatField(help_text='Humidity in percentage')
    ph = models.FloatField(verbose_name='pH')
    rainfall = models.FloatField(help_text='Rainfall in mm')
    label = models.CharField(max_length=70, verbose_name='Crop')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label} (Added: {self.added_at.strftime('%Y-%m-%d')})"

    class Meta:
        verbose_name = 'Add Data to Dataset'
        verbose_name_plural = 'Add Data to Dataset'

class CropDataset(models.Model):
    n = models.FloatField(verbose_name='Nitrogen')
    p = models.FloatField(verbose_name='Phosphorus')
    k = models.FloatField(verbose_name='Potassium')
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField(verbose_name='pH')
    rainfall = models.FloatField()
    label = models.CharField(max_length=70, verbose_name='Crop')
    
    def __str__(self):
        return f"{self.label} (N: {self.n}, P: {self.p}, K: {self.k})"

    class Meta:
        verbose_name = 'Crop Dataset Entry'
        verbose_name_plural = 'Crop Dataset Entries'

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback from {self.user.username} - {self.get_rating_display()}"

    class Meta:
        ordering = ['-created_at']
