# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from books.models import Book, Publisher, Author
from books.forms import ReviewForm, SearchForm
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from actstream.actions import follow, unfollow, is_following
from actstream.models import following, user_stream
from actstream.signals import action

class Index(FormView):
    template_name = 'search_book.html'
    form_class = SearchForm

    def form_valid(self, search_form):
        objects = []
        if search_form.cleaned_data['search_creteria'] == 'book':
            objects = Book.objects.filter(title__icontains=search_form.cleaned_data['query'])
            message = 'book title'
        elif search_form.cleaned_data['search_creteria'] == 'author':
            authors = Author.objects.filter(last_name__icontains=search_form.cleaned_data['query'])
            if authors:
                for author in authors:
                    objects += author.book_set.all()
            message = "author's last name"
        else:
            publishers = Publisher.objects.filter(name__icontains=search_form.cleaned_data['query'])
            if publishers:
                for publisher in publishers:
                    objects += publisher.book_set.all()
            message = 'publisher'   
        return render(self.request, 'search_book.html',
                               {'form': self.get_form(self.form_class), 'books': objects, 'query': search_form.cleaned_data['query'], 'info': message})

class Login_user(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return HttpResponseRedirect(reverse('profile', args=(user.username,)))

class Create_user(FormView):
    template_name = 'create_user.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        newuser = form.save()
        return HttpResponseRedirect(reverse('login'))

@login_required
def logout_user(request):
    logout(request)
    return redirect('searchform')

def detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'GET':
        form = ReviewForm()
        return render(request, 'detail.html', {'book': book, 'form': form})
    #if request.method == 'POST':
    form = ReviewForm(request.POST)
    if form.is_valid():
        review_instance = form.save(commit=False)
        review_instance.book = book
        review_instance.save()
        book.number_of_reviews = book.review_set.all().count()
        book.save()
        action.send(book, verb='was reviewed', reviewer=review_instance.name_of_reviewer, text=review_instance.text)
        return HttpResponseRedirect(reverse('detail', args=(book.pk,)))
    return render(request, 'detail.html', {'book': book, 'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    actors = following(user)
    return render(request, 'profile.html', {'user': username, 'actors': actors})

@login_required
def follow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not is_following(request.user, book):
        follow(request.user, book)
        return render(request, 'detail.html', {'book': book, 'form': ReviewForm, 'message': 'You are following this book.'})
    return render(request, 'detail.html', {'book': book, 'form': ReviewForm, 'message': 'You already follow this book.'})

@login_required
def unfollow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if is_following(request.user, book):
        unfollow(request.user, book)
        return render(request, 'detail.html', {'book': book, 'form': ReviewForm(), 'message': 'You unfollowed this book.'})    
    return render(request, 'detail.html', {'book': book, 'form': ReviewForm(), 'message': 'You do not follow this book yet.'})

@login_required
def timeline(request):
    actions = user_stream(request.user)
    try:
        selected_actions = actions[0:5]
    except IndexError:
        selected_actions = actions
    #import ipdb; ipdb.set_trace()
    return render(request, 'timeline.html', {'actions': selected_actions, 'username': request.user.username})    