from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from . models import Product,ProductGallery,ReviewRating
from category.models import Category
from carts.models import CartItem,Cart
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.contrib import messages

# Create your views here.
# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    sort_option = request.GET.get('sort')

    if sort_option == 'price-low-to-high':
        products = products.order_by('price')
    elif sort_option == 'price-high-to-low':
        products = products.order_by('-price')
    elif sort_option == 'name-a-to-z':
        products = products.order_by('product_name')
    elif sort_option == 'name-z-to-a':
        products = products.order_by('-product_name')
    elif sort_option == 'category-a-to-z':
        products = products.order_by('category__category_name')
    elif sort_option == 'category-z-to-a':
        products = products.order_by('-category__category_name')
    elif sort_option == 'color':
        products = products.order_by('variation__variation_value')
    elif sort_option == 'color-reverse':
        products = products.order_by('-variation__variation_value')
    elif sort_option == 'size':
        products = products.order_by('variation__variation_value')
    elif sort_option == 'size-reverse':
        products = products.order_by('-variation__variation_value')

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_product,
        'product_count': product_count,
    }
    return render(request, 'greatkart/store/store.html', context)

def get_related_products(product):
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return related_products

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()
        if single_product.is_available=='False':
            return redirect('store')
    
    except Exception as e:
        raise e
    product = Product.objects.get(category__slug=category_slug,slug=product_slug) 
    related_products = get_related_products(product)  
    # images = ProductGallery.objects.filter(product=product)
    # print(images)  # Print the query results   
 # Retrieve only the images that belong to the specific product
    product_images = ProductGallery.objects.filter(product=single_product)
    
    if request.method == 'POST':
        rating = request.POST['rating']
        review = request.POST['review']

        # Create a new ReviewRating object
        review_rating = ReviewRating(
            product=single_product,
            user=request.user,
            rating=rating,
            review=review,
            )
        # Save the ReviewRating object to the database
        review_rating.save()

    reviews = ReviewRating.objects.filter(product=single_product, status=True)
    
     
    context = {
        
        'single_product':single_product,
        'related_products': related_products,
        'in_cart':in_cart, 
         'reviews': reviews,
            
            'product_images': product_images,
    }
     
    

    return render(request,'greatkart/store/product_detail.html',context)





def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if 'keyword':
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q( product_name__icontains=keyword))
            product_count=products.count()
    context = {
        'products':products,
        'product_count':product_count,
    }
    
    return render(request,'greatkart/store/store.html',context)


def add_review(request, product_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        product = Product.objects.get(id=product_id)
        ReviewRating.objects.create(product=product, user=request.user, rating=rating, review=review)
        product.rating = (product.rating * product.num_reviews + int(rating)) / (product.num_reviews + 1)
        product.num_reviews += 1
        product.save()
        messages.success(request, 'Review added successfully!')
        return redirect('product_detail', product.category.slug, product.slug)