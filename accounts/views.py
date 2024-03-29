from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from contacts.models import Contact
# Create your views here.
def register(request):
	if request.method=='POST':
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		username=request.POST['username']
		email=request.POST['email']
		password=request.POST['password']
		password2=request.POST['password2']

		#check if password match
		if password==password2:
			#check username
			if User.objects.filter(username=username):
				messages.error(request, 'Username is already taken.')
				return redirect('register')	
			elif User.objects.filter(email=email):
				messages.error(request, 'Email is already used.')
				return redirect('register')
			else:
				user=User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
				#login after register
				# auth.login(request, user)
				# messages.success(request, 'You are now logged in')
				# return redirect('index')
				user.save()
				messages.success(request, 'You are now registered and can logged in')
				return redirect('login')
		else:
			messages.error(request, 'Password do not match.')
			return redirect('register')
	else:
		return render(request,'accounts/register.html')

def login(request):
	if request.method =='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			messages.success(request, 'You are now logged in')
			return redirect('dashboard')
		else:
			messages.error(request, 'Invalid credentials')
			return redirect('login')
	else:
		return render(request,'accounts/login.html')

def logout(request):
	if request.method=='POST':
		auth.logout(request)
		messages.success(request, 'You are now successfully logout')
		return redirect('index')

def dashboard(request):
	user_id=request.user.id
	contacts=Contact.objects.order_by('-contact_date').filter(user_id=user_id)
	context={
		'contacts':contacts,
	}
	return render(request,'accounts/dashboard.html', context)
