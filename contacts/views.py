from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from.models import Contact


# Create your views here.
def contact(request):
	if request.method =='POST':
		listing_id=request.POST['listing_id']
		listing=request.POST['listing']
		name=request.POST['name']
		email=request.POST['email']
		phone=request.POST['phone']
		message=request.POST['message']
		user_id=request.POST['user_id']
		realtor_email=request.POST['realtor_email']

		if request.user.is_authenticated:
			has_contacted_=Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
			if has_contacted.exists():
				messages.error(request,'Sorry! Your have already made an inquiry about this listing')
				return redirect('/listings/'+listing_id)

		contact=Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)
		contact.save()
		#send mail
		send_mail(
			'Property Listing Inquiry',
			'There has been an inquiry for '+ listing +'. sign into an admin panel for more info.',
			email,
			[realtor_email,],
			fail_silently=False
		)

		messages.success(request,'Your message has been submitted, a realtor will get back to you soon.')
		return redirect('/listings/'+listing_id)