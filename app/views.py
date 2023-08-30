from django.shortcuts import render
from .models import Watch
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    search_query = request.GET.get('search')
    context = {'filtered_watches': []}

    if search_query:
        if Watch.objects.filter(brand__icontains=search_query).exists():
            filtered_watches = Watch.objects.filter(brand__icontains=search_query)

            context['filtered_watches'] = [{"id": i.id, "brand": i.brand, "model": i.model} for i in filtered_watches]
        else:
            context = {'error_message': 'No results found'}

    return render(request, "home.html", context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user) 
            return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, "registration/login.html", {'error_message': error_message})

    return render(request, "registration/login.html")

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ('Logout successful!'))

def watches(request):
    items = Watch.objects.all().order_by('brand')
    return render(request, "watches.html", {"watches": items})

def details(request, id):
    item = get_object_or_404(Watch, id=id)
    return render(request, "details.html", {'watch': item})

@login_required
def handle_description(request, id):
    item = get_object_or_404(Watch, id=id)

    if request.method == 'POST':
        description = request.POST.get('description')
 
        try:
            Watch.objects.filter(pk=id).update(description=description)
            return redirect('details', id=id)
        except:
            error_message = "There was an error."
            return render(request, "details.html", {'watch': item, 'error_message': error_message })

    return render(request, "details.html", {'watch': item})

@login_required
def add_watch(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')

        added_by_user = request.user
        Watch.objects.create(brand=brand, model=model, added_by=added_by_user)

    return redirect('watches')

@login_required
def delete_watch(request, id):
    item = Watch.objects.get(id=id)
    if request.method == 'POST':
        item.delete()

    return redirect('watches')





    
    



