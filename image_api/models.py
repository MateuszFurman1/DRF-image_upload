from users import models
from PIL import Image

class BasicAccount(models.Model):
    name = models.CharField(max_length=50, null=True)
    thumbnail_low = models.ImageField(upload_to="images/", height_field=200, width_field=None, max_length=None)
    
    
class PremiumAccount(models.Model):
    name = models.CharField(max_length=50, null=True)
    thumbnail_low = models.ImageField(upload_to="images/", height_field=200, width_field=None, max_length=None)
    thumbnail_high = models.ImageField(upload_to="images/", height_field=400, width_field=None, max_length=None)
    thumbnail_org = models.ImageField(upload_to="images/", max_length=None)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Generate the thumbnail
        if self.thumbnail_org:
            img = Image.open(self.thumbnail_org.path)
            img.thumbnail((img.width, img.height), Image.ANTIALIAS)
            img.save(self.thumbnail_org.path)
            

class EnterpriseAccount(models.Model):
    name = models.CharField(max_length=50, null=True)
    thumbnail_low = models.ImageField(upload_to="images/", height_field=200, width_field=None, max_length=None)
    thumbnail_high = models.ImageField(upload_to="images/", height_field=400, width_field=None, max_length=None)
    thumbnail_org = models.ImageField(upload_to="images/", max_length=None)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Generate the thumbnail
        if self.thumbnail_org:
            img = Image.open(self.thumbnail_org.path)
            img.thumbnail((img.width, img.height), Image.ANTIALIAS)
            img.save(self.thumbnail_org.path)
            
            
class AccountTiers(models.Model):
    
    PLAN_CHOICES = (
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('Enterprise', 'Enterprise'),
    )

    name = models.CharField(max_length=50, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField()