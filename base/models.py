from django.db import models
from django.utils import timezone
from datetime import datetime
import json
from django.conf import settings
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib.auth.models import User, AbstractUser
import uuid
from uuslug import uuslug as slugify

host = settings.MAINHOSTNAME



def generate_search_tags(product_name, color, brand):
    tags = []
    # Include the entire product name as a search tag
    tags.append(product_name.lower())

    # Include color and brand as search tags
    if color:
        tags.append(color.lower())
    if brand:
        tags.append(brand.lower())

    # Generate combinations of product name, color, and brand
    if product_name and color:
        tags.append(f"{product_name.lower()}_{color.lower()}")
    if product_name and brand:
        tags.append(f"{product_name.lower()}_{brand.lower()}")
    if color and brand:
        tags.append(f"{color.lower()}_{brand.lower()}")
    if product_name and color and brand:
        tags.append(f"{product_name.lower()}_{color.lower()}_{brand.lower()}")

    return tags





def run_async_function_in_thread(async_function, *args, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_function(*args, **kwargs))
    loop.close()
    return result


class Customers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    phone_number = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    

class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField()

    class Meta:
        ordering = ('id', 'name',)
    
    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name 
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, instance=self)
        super(Category, self).save(*args, **kwargs)
    
    

class Products(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, max_length=255,blank=False, null=False)
    name = models.CharField(max_length=255,blank=True, null=True) 
    description = models.TextField(max_length=4096,blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    thumbnail = models.ImageField(upload_to="products/thumbnails/", null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    image_lists =  models.CharField(max_length=8192,blank=True, null=True)
    sales_price =  models.DecimalField(max_digits=8, decimal_places=0, null=True,blank=True)
    sales_date_from =  models.DateTimeField(blank=True, null=True)
    sales_date_to =  models.DateTimeField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    is_in_stock = models.BooleanField(default=True)
    color = models.CharField(max_length=32,blank=True, null=True)
    brand = models.CharField(max_length=32,blank=True, null=True)
    size = models.CharField(max_length=32,blank=True, null=True)
    search_tags = models.TextField(max_length=2555,blank=True, null=True)
    
    
    class Meta:
        ordering = ('-date_added',)
        
        
    def __unicode__(self):
        return self.name 
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, instance=self)
        desc = f"Brand: {self.brand.capitalize()}\nColor: {self.color}\nSize: {self.size}\n\n{self.description}\n".replace("None","-")
        if 'Brand' not in self.description:
            self.description = desc

        new_tag = generate_search_tags(self.name, self.color, self.brand)
        tags = ','.join(new_tag)
        self.search_tags = tags
        super(Products, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'
    
    def get_product_image(self):
        if self.image:
            return host + self.image.url
        return ""
    
    def get_image_list(self):
        if self.image_lists:
            image_list = str(self.image_lists).split(',')
            image_list.insert(0, self.thumbnail.url)
            host_list=[host+x for x in image_list]
            return host_list
        else:
            if self.thumbnail:
                host_list=[host + self.thumbnail.url]
                return host_list
        return []
        
    def get_image_list_string(self):
        if self.image_lists:
            image_list = str(self.image_lists).split(',')
            image_list.insert(0, self.thumbnail.url)
            host_list=[host+x for x in image_list]
            return host_list
        else:
            if self.thumbnail:
                host_list=[host + self.thumbnail.url]
                return ''.join(host_list)
        return ""
        
    def get_thumbnail(self):
        if self.thumbnail:
            return host + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return host + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)
        thumbnail = File(thumb_io, name=image.name)
        
        return thumbnail
    
    def get_colored_stars(self):
        if self.rating:
            colored = [x for x in range(1, int(round(self.rating, ndigits=0)) + 1)]
            return colored
        return []
        
    def get_blank_stars(self):
        if self.rating:
            colored = [x for x in range(1, 5 - int(round(self.rating, ndigits=0)) + 1)]
            return colored
        return [x for x in range(1,6)]
    
    def get_percentage_discount(self):
        if self.sales_price and (float(self.price) > float(self.sales_price)) and str(self.sales_date_from) <= str(datetime.now()) <= str(self.sales_date_to):
            return int(round((100 - (float(self.sales_price) * 100 / float(self.price))), ndigits=0))        
        return None
    
   
    
    
class AdBanner(models.Model):
    offer_event = models.CharField(max_length=255,blank=True, null=True) 
    product_name = models.CharField(max_length=255,blank=True, null=True) 
    starting_price = models.CharField(max_length=255,blank=True, null=True) 
    date_added = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to="ads/", null=True, blank=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return f"Sale offer {self.offer_event} this Week for {self.product_name}.starting at {self.starting_price}"
    
    def get_image(self):
        if self.image:
            return host + self.image.url
        return ""
    
    
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True)
    product= models.ForeignKey(Products, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f"{self.user} -> {self.product.name}"
    
    
class CartList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank= True)
    product= models.ForeignKey(Products, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f"{self.user} -> {self.product.name}"
    
    
    