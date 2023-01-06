from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Movie, User
from .forms import MovieForm, UserForm, LoginForm

class MovieIndex(generic.ListView):

    template_name = "movielist/movie_index.html"
    context_object_name = "movies"

    def get_queryset(self):
        return Movie.objects.all().order_by("-id")

class CurrentMovieView(generic.DetailView):
    model = Movie
    template_name = "movielist/movie_detail.html"

    def get(self, request, pk):
        try:
            movie = self.get_object()
        except:
            return redirect("movie_index")
        return render(request, self.template_name, {"movie": movie})
    
    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("edit_movie", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "You don't have rights to delete movie.")
                    return redirect(reverse("movie_index"))
                else:
                    self.get_object().delete()
        return redirect(reverse("movie_index"))

class CreateMovie(LoginRequiredMixin, generic.edit.CreateView):

    form_class = MovieForm
    template_name = "movielist/create_movie.html"

    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "You don't have rights to add movie.")
            return redirect(reverse("movie_index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    
    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "You don't have rights to add movie.")
            return redirect(reverse("movie_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return render(request, self.template_name, {"form":form})

class UserViewRegister(generic.edit.CreateView):
    form_class = UserForm
    model = User
    template_name = "movielist/user_form.html"
    
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are login, you can't register.")
            return redirect(reverse("movie_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are logged in, you can't register.")
            return redirect(reverse("movie_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            login(request, user)
            redirect("movie_index")
        
        return render(request, self.template_name, {"form": form})

class UserViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "movielist/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in, you cannot log in again.")
            return redirect(reverse("movie_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in, you cannot log in again.")
            return redirect(reverse("movie_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("movie_index")
            else:
                messages.error(request, "This account does not exist")
        return render(request, self.template_name, {"form": form})
    
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "You are not login.")
    return redirect(reverse("login"))

class EditMovie(LoginRequiredMixin, generic.edit.CreateView):
    form_class = MovieForm
    template_name = "movielist/create_movie.html"

    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "You don't have rights to edit movie.")
            return redirect(reverse("movie_index"))
        try:
             movie = Movie.objects.get(pk=pk)
        except:
            messages.error(request, "This movie does not exixt")
            return redirect("movie_index")
        form = self.form_class(instance=movie)
        return render(request, self.template_name, {"form":form})
    
    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "You don't have rights to edit movie.")
            return redirect(reverse("movie_index"))
        form = self.form_class(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            director = form.cleaned_data["director"]
            genre = form.cleaned_data["genre"]
            tags = form.cleaned_data["tags"]
            try:
                movie = Movie.objects.get(pk=pk)
            except:
                messages.error(request, "This movie does not exist")
                return redirect(rverse("movie_index"))
            movie.name = name
            movie.director = director
            movie.genre = genre
            movie.tags.set(tags)
            movie.save()
        return redirect("movie_detail", pk=movie.id)




