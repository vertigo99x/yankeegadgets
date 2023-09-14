from .models import Products, AdBanner, Category, WishList, CartList, Customers
from .serializers import ProductSerializer, AdBannerSerializer

from asgiref.sync import sync_to_async

from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import check_password
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.template.defaulttags import register
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

#import asyncio
import requests



default_items_per_page = 12
host = settings.MAINHOSTNAME


@register.filter
def description_strip(value):
    return value[:260]

@register.filter
def length(value):
    return len(value)

@register.filter
def checkTrue(value):
    if value:
        return 'true'
    return 'false'

@register.filter
def firstname(value):
    name = Customers.objects.filter(user__username=value).get()
    if name.firstname:
        return name.firstname.capitalize()
    return ''


@register.filter
def toInt(value):
    return int(value)

"""

def run_async_function_in_thread(async_function, *args, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(async_function(*args, **kwargs))
    loop.close()
    return result

"""

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


def logout(request):
    auth.logout(request)
    return redirect('index')
    
    
def base(request):
    return HttpResponse(request, "HELLO")

"""

class HomeView(View):
    def get(self, request, *args, **kwargs):
        async def getAds():
            return AdBanner.objects.all()
        
        async def getProds(limit):
            return Products.objects.all()[:limit]
        
        async def getWishList():
            return WishList.objects.filter(user=request.user)
        
        
        
        def getCategoryItems(limit):
            categories = [{'id':x.id,"name":x.name,"slug":x.slug} for x in Category.objects.all().order_by('id')]
            category_listing = [
                {
                    'category_id':x['id'],
                    'category_name':x['name'],
                    'category_slug':x['slug'],
                    'products':Products.objects.filter(category=x['id'])
                } for x in categories
                
            ]
            
            return category_listing
        
        context = {}
        
        context['adBanner'] = run_async_function_in_thread(getAds)
        context['new_arrivals']=run_async_function_in_thread(getProds, limit=6)
        #context['categories']=run_async_function_in_thread(getCategories)
        context['category_items']=getCategoryItems(limit=6)
        
        if request.user.is_authenticated:
            wishlist = run_async_function_in_thread(getWishList)
            context['wishlist'] = wishlist
            context['wishlist_count'] = wishlist.count()
        
        return render(request, "index.html", context)

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')
    

class SearchView(View):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('searchphrase','')
        pageNo = request.GET.get('page', 1)
        order=request.GET.get('order','')
        
        search = search.strip(' ')
        
        context = {}
        
        print(search, pageNo, order)
        
        
        async def getSearch():
            return Products.objects.filter(Q(search_tags__icontains=search) | Q(search_tags__icontains=search.replace(' ', '_')))
        
        async def getSearchOrd(order):
            return Products.objects.filter(Q(search_tags__icontains=search) | Q(search_tags__icontains=search.replace(' ', '_'))).order_by(order)
        
        async def getWishList():
            return WishList.objects.filter(user=request.user)
        
        
        
        def getOrderingName(orderName):
            if orderName == "a-z":return "name"
            elif orderName == "z-a":return "-name"
            elif orderName == "l-h":return "price"
            elif orderName == "h-l":return "-price"
            elif orderName == "rat":return "-rating"
            elif orderName == "rel" or orderName=="":return ""
            
        
        if getOrderingName(order):
            products = run_async_function_in_thread(getSearchOrd, order=getOrderingName(order))
        else:
            products = run_async_function_in_thread(getSearch)
        
        
        paginatedProducts = Paginator(products, default_items_per_page)
        total_pages = paginatedProducts.num_pages
        
        if request.user.is_authenticated:
            wishlist = run_async_function_in_thread(getWishList)
            context['wishlist'] = wishlist
            context['wishlist_count'] = wishlist.count()
        
        if total_pages == 0:
            return render(request, "404.html", {"raise":"item_not_found"})
        
        try:
            page_prod = paginatedProducts.page(pageNo)
        except Exception:
            page_prod = paginatedProducts.page(1)
            pageNo = 1
            
            
        if len(page_prod) < default_items_per_page:
            page_items = len(page_prod)
        else:
            page_items = default_items_per_page
        
        
        page_array = [x for x in range(int(pageNo)-1, int(total_pages)+1) if x != 0][:4]

            
        
        
       
        context['products'] = page_prod
        context['products_count'] = products.count()
        context['items_per_page'] = page_items
        context['pageNo'] = pageNo
        context['total_pages'] = total_pages
        context['search_phrase'] = search.capitalize()
        context['order'] = order
        context['page_array'] = page_array
        context['host'] = host
        
        if int(pageNo) < total_pages:
            context['next_page'] = page_prod.next_page_number
        if int(pageNo) > 1:
            context['previous_page'] = page_prod.previous_page_number
        
        return render(request, 'search-products.html', context)



    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')

    
class ProductView(View):
    def get_object(self, category_slug, product_slug):
        try:
            return Products.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Products.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug):
        
        async def getWishList():
            return WishList.objects.filter(user=request.user)
        
        async def getCategories():
            return Category.objects.all()
        
        
        product = self.get_object(category_slug, product_slug)
        context = {}
        context['product'] = product
        category_products = Products.objects.filter(category=product.category).order_by('name')[:15]
        context['category_products'] = category_products
        context['category_length'] = category_products.count()
        context['categories'] = run_async_function_in_thread(getCategories)
        
        if request.user.is_authenticated:
            wishlist = run_async_function_in_thread(getWishList)
            context['wishlist'] = wishlist
            context['wishlist_count'] = wishlist.count()
        
        return render(request, "single-product.html", context)
        

class WishListView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        context = {}
        async def getWishList():
            return WishList.objects.filter(user=request.user)
        
        async def getCategories():
            return Category.objects.all()
    
        wishlist = run_async_function_in_thread(getWishList)
        context['categories'] = run_async_function_in_thread(getCategories)
        context['wishlist'] = wishlist
        context['wishlist_count'] = wishlist.count()
        
        
        return render(request, "wishlist.html", context)

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')

    
    
    
    
    
class AddToWishList(LoginRequiredMixin, APIView):
    def post(self, request, *args, **kwargs):
        async def checkUser(pk):
            return User.objects.filter(id=pk)
          
        async def checkProduct(pk, uid):
            return Products.objects.filter(uid=uid), WishList.objects.filter(user__id=pk, product__uid=uid)
        
        
        
        data = request.data 
        user_id = data['user_id']
        product_uid = data['uid']
        
        user_exists = run_async_function_in_thread(checkUser, pk=user_id)
        prod = run_async_function_in_thread(checkProduct, uid=product_uid, pk=user_id)
        
        product_info, exists_in_list = prod
        
        if user_exists.exists() and product_info.exists():
            if not exists_in_list:
                item = WishList.objects.create(
                    user = user_exists.get(),
                    product = product_info.get()
                )
                item.save();
                return Response({'message':'successful'})
            else:
                return Response({'message':'item_already_exists'})
        
        if not user_exists:
            return Response({'message':'user_not_exist'})
        
        
        return Response({'message':'Unable to Add to Wishlist'})
            
class RemoveFromWishList(LoginRequiredMixin, APIView):
    def post(self, request, *args, **kwargs):
        data = request.data 
        user_id = data['user_id']
        product_uid = data['uid']
        
        if user_id and product_uid:
            WishList.objects.filter(user__id = user_id, product__uid = product_uid).delete()
            return Response({'message':'successful'})

        return Response({'message':'Unable to remove from Wishlist'})
        
    
class AddToUserCart(APIView):
    def post(self, request, *args, **kwargs):
        pass
    

class GetCartDetails(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            cart = CartList.objects.filter(user = request.user)
            
        return Response({"message":None})
        pass
    
    
"""
    
    
    
    
    
    
    

class LoginView(View):
    def get(self, request, *args, **kwargs):
        async def getCategories():
            return Category.objects.all()
        
        if request.user.is_authenticated:
            return redirect('index')
        
        context = {
            'show':'login',
            'categories':run_async_function_in_thread(getCategories)
        }
        
        return render(request, "login-register.html", context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        
        messages.error(request, 'User Does Not Exist!')
        return redirect('login-page')
    
    
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        async def getCategories():
            return Category.objects.all()
        
        if request.user.is_authenticated:
            return redirect('index')
        
        context = {
            'show':'register',
            'categories':run_async_function_in_thread(getCategories)
        }
        
        return render(request, "login-register.html", context)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        firstname = request.POST['firstname']
        phone = request.POST['phone']
        lastname = request.POST['lastname']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.error(request, "Passwords dont match!")
            return redirect('register')
        
        if len(password)<8:
            messages.error(request, "Passwords must be at least 8 digits")
            return redirect('register')
            
        user = User.objects.filter(Q(username = email) | Q(email=email))
        
        if user.exists():
            messages.error(request, "Email Already in Use!")
            return redirect('register')
        
        user = User.objects.create_user(
                username = email,
                password = password,
                email=email,
            )
            
        user.save(); 
        customer = Customers.objects.create(
            user = user,
            phone_number = phone,
            firstname = firstname,
            lastname = lastname,
        )  
        customer.save();
            
        
        messages.success(request, "Sign Up Was Successful")
        return redirect('login-page')
        
    