from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Tag(models.Model):
    tag_title = models.CharField(max_length=64, verbose_name="Tags")

    def __str__(self):
        return f"{self.tag_title}"
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Genre(models.Model):
    genre_name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.genre_name}"
    
    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        


class Movie(models.Model):
    name = models.CharField(max_length=256, verbose_name="Movie name")
    director = models.CharField(max_length=256, verbose_name="Director")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, verbose_name="Genre")

    tags = models.ManyToManyField(Tag)

    def __init__(self, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)

    def __str__(self):
        tags = [i.tag_title for i in self.tags.all()]

        return f"Name: {self.name}, Director: {self.director}, Genre: {self.genre} Tag: {tags}"

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=256, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    
    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"Email: {self.email}"
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True


