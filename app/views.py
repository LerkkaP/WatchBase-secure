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
        with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM app_watch WHERE brand LIKE '%{search_query}%'")
                filtered_watches = cursor.fetchall()
                for alkio in filtered_watches:
                    items = {"id": alkio[0], "brand": alkio[1], "model": alkio[2]}
                    results.append(items)
                context['filtered_watches'] = results
       except:
           error_message = "There was an error."
           context['error_message'] = error_message
           return render(request, "home.html", context)

    return render(request, "home.html", context)

def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM app_user WHERE username = '{user}'")
                row = cursor.fetchone()
        except:
            error_message = "There was an error."
            return render(request, "login.html", {'error_message': error_message})
        
        if row and row[2] == password and row[1] == user:
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
            with connection.cursor() as cursor:
                cursor.execute(f"UPDATE app_watch SET description = '{description}' WHERE id = '{id}'")
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



    
    



