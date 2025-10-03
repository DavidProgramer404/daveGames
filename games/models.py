from django.db import models

# Create your models here.

# crear las clases en ingles

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    # definición str
    def __str__(self):
        return self.name
    

# Agregar la clase de juego

class Game(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    min_requirements = models.TextField(blank=True, null=True)
    max_requirements = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/')
    trailer_url = models.URLField(blank=True, null=True)
    download_link = models.URLField()
    release_date = models.DateField()

    def __str__(self):
        return self.title


# Modelo para comentarios de usuarios en juegos
class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments')
    nickname = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname} - {self.game.title}"
