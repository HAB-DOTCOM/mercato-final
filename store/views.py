from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from category.models import catagory
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct


# Create your views here.

def store(request,catagory_slug=None):
	categories=None
	products=None

	if catagory_slug!= None:
		categories=get_object_or_404(catagory,slug=catagory_slug)
		products=Product.objects.filter(catagory=categories,is_available=True)
		paginator = Paginator(products, 2)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		product_count=products.count()
	else:
		products=Product.objects.all().filter(is_available=True).order_by('id')
		paginator = Paginator(products, 2)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		product_count =products.count()

	context={
		'products':page_obj,
		'product_count':product_count,
		}

	return render(request,'store/store.html',context)

def product_detial(request,catagory_slug,product_slug):
	try:
		single_product = Product.objects.get(catagory__slug=catagory_slug, slug=product_slug)
		in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

	except Exception as e:
		raise e
	if request.user.is_authenticated:

		try:
			orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
		except OrderProduct.DoesNotExist:
			orderproduct = None
	else:
		orderproduct = None
	reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
	product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
	context = {
		'single_product': single_product,
		'in_cart'       : in_cart,
		'orderproduct': orderproduct,
		'reviews': reviews,
		'product_gallery':product_gallery,
	}
	return render(request, 'store/product_detial.html', context)


    # Get the reviews
    

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

