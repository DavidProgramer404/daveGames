from django.shortcuts import render, get_object_or_404, redirect
from .models import Game, Category

# Create your views here.
# CREAR VISTAS Y RUTAS

def home(request):
    categories = Category.objects.all()
    games = Game.objects.all().order_by('-release_date')[:6]  # últimos 6 juegos
    return render(request, 'games/home.html', {
        'categories': categories, 
        'games': games
    })

# definir categorias juegos
def category_games(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    games = Game.objects.filter(category=category).order_by('-release_date')
    categories = Category.objects.all()
    return render(request, 'games/category_games.html', {
        'category': category, 
        'games': games,
        'categories': categories
    })

# definir juego detalle
from .forms import CommentForm
from .models import Comment

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    categories = Category.objects.all()
    comments = game.comments.order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.game = game
            comment.save()
            return redirect('game_detail', game_id=game.id)
    else:
        form = CommentForm()
    return render(request, 'games/game_detail.html', {
        'game': game,
        'categories': categories,
        'comments': comments,
        'form': form,
    })