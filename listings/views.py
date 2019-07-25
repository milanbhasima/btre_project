from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Listing
from listings.choices import price_choices, bedroom_choices, state_choices 

# Create your views here.
def index(request):
	listings=Listing.objects.order_by('-list_date').filter(is_published=True)
	paginator = Paginator(listings, 6)
	page = request.GET.get('page')
	paged_listings = paginator.get_page(page)
	context={
	'listings':paged_listings
	}
	return render(request, 'listings/listings.html',context)

def listing(request, listing_id):
	listing=get_object_or_404(Listing, id=listing_id)
	context={
		'listing':listing,
	}
	return render(request, 'listings/listing.html',context)

def search(request):
	queryset_list=Listing.objects.order_by('-list_date')
	#keyword
	if 'keywords' in request.GET:
		keywords=request.GET.get('keywords')
		if keywords:
			queryset_list=Listing.objects.filter(description__icontains=keywords)
	#city
	if 'city' in request.GET:
		city=request.GET.get('city')
		if city:
			queryset_list=queryset_list.filter(city__iexact=city)
	#city
	if 'state' in request.GET:
		state=request.GET.get('state')
		if state:
			queryset_list=queryset_list.filter(state__iexact=state)
	#city
	if 'bedrooms' in request.GET:
		bedrooms=request.GET.get('bedrooms')
		if bedrooms:
			queryset_list=queryset_list.filter(bedrooms__lte=bedrooms)
	#city
	if 'price' in request.GET:
		price=request.GET.get('price')
		if price:
			queryset_list=queryset_list.filter(price__lte=price)
	# query_list=request.GET.get('q')
	# if query_list is not None:
	# 	lookups=(
	# 		Q(title__icontains=query)| 
	# 		Q(description__icontains=query)|
	# 		Q(tag__title__icontains=query)
	# 		)
	# 	queryset=Product.objects.filter(lookups).distinct()
	# else:
	# 	queryset=Product.objects.featured()
	# context={
	# 	'object_list':queryset,
	# 	'query':query,
	# }
	context={
		'listings':queryset_list,
		'state_choices':state_choices,
		'bedroom_choices':bedroom_choices,
		'price_choices':price_choices
	}
	return render(request, 'listings/search.html', context)
