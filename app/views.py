from django.shortcuts import render
from .models import Watch, User
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def home(request):
    results = []
    context = {'is_authenticated': request.session.get('username')}

    search_query = request.GET.get('search')
    if search_query:
       try:
        filtered_watches = Watch.objects.filter(brand__icontains=search_query)
        for i in filtered_watches:
            items = {"id": i.id, "brand": i.brand, "model": i.model}
            results.append(items)
        context['filtered_watches'] = results
       except:
           error_message = "There was an error."
           context['error_message'] = error_message
           return render(request, "home.html", context)

    return render(request, "home.html", context)

def login(request):
    results = []
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            info = User.objects.filter(username=user)
            for i in info:
                results.append(i.username)
                results.append(i.password)
        except:
            error_message = "There was an error."
            return render(request, "login.html", {'error_message': error_message})
        
        if info and results[0] == user and results[1] == password:
            request.session['username'] = user
            return redirect('home')
        else:
            messages.success(request, ('Invalid username or password'))
            return redirect('login')
    return render(request, "login.html")

def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')

def watches(request):
    items = Watch.objects.all()
    return render(request, "watches.html", {"watches": items, 'is_authenticated': request.session.get('username')})

def details(request, id):
    item = Watch.objects.get(id=id)
    return render(request, "details.html", {'watch': item, 'is_authenticated': request.session.get('username')})

def handle_description(request, id):
    item = Watch.objects.get(id=id)

    if request.method == 'POST':
        description = request.POST.get('description')
 
        try:
            Watch.objects.filter(pk=id).update(description=description)
            return redirect('details', id=id)
        except:
            error_message = "There was an error."
            return render(request, "details.html", {'watch': item, 'error_message': error_message })

    return render(request, "details.html", {'watch': item})

def add_watch(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')

        added_by_user = User.objects.get(username=request.session.get('username'))
        Watch.objects.create(brand=brand, model=model, added_by=added_by_user)

    return redirect('watches')

def delete_watch(request, id):
    item = Watch.objects.get(id=id)
    if request.method == 'POST':
        item.delete()

    return redirect('watches')



    
    



