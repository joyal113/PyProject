
# Create your views here.
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.db.models import F

from .models import CustomUser, UserBook
from .forms import CustomUserCreationForm, UserLoginForm, PasswordResetForm

# create a function


def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def reset_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                user = CustomUser.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                return redirect('login')
            else:
                raise ValueError('Passwords do not match')
    else:
        form = PasswordResetForm()
    data = {'form': form}
    return render(request, "reset.html", data)

def home(request):
    if request.user.is_authenticated:
        data = {}
        search = request.GET.get('search')
        print(search)
        books = UserBook.objects.filter(user=request.user)
        recently_viewed = books.filter(category="recently_viewed").annotate(title=F('book__title'), image_url=F('book__image_url'), pdf_url=F('book__pdf_url')).values('title', 'image_url', 'pdf_url')
        suggested = books.filter(category="suggested").annotate(title=F('book__title'), image_url=F('book__image_url'), pdf_url=F('book__pdf_url')).values('title', 'image_url', 'pdf_url')
        explore_more = books.filter(category="explore_more").annotate(title=F('book__title'), image_url=F('book__image_url'), pdf_url=F('book__pdf_url')).values('title', 'image_url', 'pdf_url')
        data["explore_more_books"] = explore_more
        if search:
            searched_books = books.filter(book__title__icontains=search)
            data["search"] = search
            data['searched_books'] = searched_books.annotate(title=F('book__title'), image_url=F('book__image_url'), pdf_url=F('book__pdf_url')).values('title', 'image_url', 'pdf_url')
            print(data)
            return render(request, "library.html", data)
        data["recently_viewed"] = recently_viewed
        data["suggested_books"] = suggested
        
        return render(request, "library.html", data)
    return redirect("login")


def login_user(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})


def login_admin(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect(reverse('admin:index'))
                return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, "admin.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect('login') 


def new(request):
    return render(request, 'new.html')