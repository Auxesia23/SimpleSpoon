from django.urls import reverse_lazy
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import requests
from .models import Recipe, Like
from django.conf import settings




class IndexView(View) :
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)
    
class RecipeListView(ListView):
    model = Recipe
    template_name = 'list_resep.html'  
    context_object_name = 'recipes'       
    paginate_by = 6    

   
    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')
        search_query = self.request.GET.get('q', '')

        if search_query:
            search_terms = search_query.split()
            query = Q()
            for term in search_terms:
                query &= Q(
                    Q(name__icontains=term) |
                    Q(category__icontains=term) |
                    Q(area__icontains=term) |
                    Q(ingredients__icontains=term)
                )
            queryset = queryset.filter(query)
        return queryset



class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'detail_resep.html'
    context_object_name = 'recipe'

    YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY
    YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        user = self.request.user

        # Hitung jumlah likes
        context['like_count'] = Like.objects.filter(recipe=recipe).count()

        # Periksa apakah user sudah menyukai resep
        context['is_liked'] = Like.objects.filter(recipe=recipe, user=user).exists() if user.is_authenticated else False

        # Cari video YouTube berdasarkan recipe.name
        context['youtube_videos'] = self.search_youtube_videos(recipe.name)

        return context

    def search_youtube_videos(self, query):
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'key': self.YOUTUBE_API_KEY,
            'maxResults': 5,  # Batasi hasil pencarian
        }

        try:
            response = requests.get(self.YOUTUBE_API_URL, params=params)
            response.raise_for_status()
            results = response.json()

            # Extract video data
            videos = [
                {
                    'title': item['snippet']['title'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'thumbnail': item['snippet']['thumbnails']['high']['url'],
                }
                for item in results.get('items', [])
            ]
            return videos

        except requests.exceptions.RequestException as e:
            print(f"Error fetching YouTube videos: {e}")
            return []

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(request.path)

        recipe = self.get_object()
        user = request.user

        # Periksa apakah user sudah menyukai resep
        existing_like = Like.objects.filter(recipe=recipe, user=user)

        if existing_like.exists():
            # Jika sudah di-like, lakukan unlike
            existing_like.delete()
            action = 'unliked'
        else:
            # Jika belum di-like, tambahkan like
            Like.objects.create(recipe=recipe, user=user)
            action = 'liked'
        return redirect(request.path)



class CreateRecipeView(LoginRequiredMixin,View):
    template_name = 'tambah_resep.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Ambil data resep
        name = request.POST.get('name')
        category = request.POST.get('category')
        area = request.POST.get('area')
        instructions = request.POST.get('instructions')
        raw_url = request.POST.get('videoUrl')
        image = request.FILES.get('image')
        author = request.user

        videoUrl = self.convert_to_embed_url(raw_url)

        # Ambil data ingredients
        ingredient_names = request.POST.getlist('ingredients[][name]')
        ingredient_values = request.POST.getlist('ingredients[][value]')

        # Format data menjadi list of dictionaries
        ingredients = [
            {'name': ing_name, 'value': ing_value}
            for ing_name, ing_value in zip(ingredient_names, ingredient_values)
        ]

        # Simpan ke database
        Recipe.objects.create(
            name=name, 
            ingredients=ingredients,
            category=category,
            area=area,
            instructions=instructions,
            videoUrl=videoUrl,
            image=image,
            author=author
        )

        # Redirect ke halaman yang sama setelah menyimpan data
        return redirect('index')
    
    def convert_to_embed_url(self, url):
        if 'youtu.be' in url:
            video_id = url.split('/')[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        return url 


class MyRecipesListView(LoginRequiredMixin ,ListView) :
    template_name = 'list_resep_saya.html'
    model = Recipe
    context_object_name = 'recipes'       
    paginate_by = 6    

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)



class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('resep-saya')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class RecipeEditView(LoginRequiredMixin, UserPassesTestMixin, DetailView) :
    model = Recipe
    template_name = 'edit_resep.html'
    context_object_name = 'recipe'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author
    
    def post(self, request, *args, **kwargs):
        recipe = self.get_object()

        # Ambil data resep yang diupdate
        name = request.POST.get('name')
        category = request.POST.get('category')
        area = request.POST.get('area')
        instructions = request.POST.get('instructions')
        raw_url = request.POST.get('videoUrl')
        image = request.FILES.get('image')  # Jika ada gambar baru, akan diambil
        author = request.user

        # Jika video URL baru ada, konversi ke embed URL
        videoUrl = self.convert_to_embed_url(raw_url)

        # Ambil data ingredients
        ingredient_names = request.POST.getlist('ingredients[][name]')
        ingredient_values = request.POST.getlist('ingredients[][value]')

        # Format data menjadi list of dictionaries
        ingredients = [
            {'name': ing_name, 'value': ing_value}
            for ing_name, ing_value in zip(ingredient_names, ingredient_values)
        ]

        # Update data resep yang ada
        recipe.name = name
        recipe.category = category
        recipe.area = area
        recipe.instructions = instructions
        recipe.videoUrl = videoUrl
        recipe.ingredients = ingredients
        recipe.author = author
        
        # Jika ada gambar baru, update gambar
        if image:
            recipe.image = image
        
        # Simpan perubahan ke database
        recipe.save()

        # Redirect ke halaman resep yang sudah diupdate
        return redirect('resep-saya')

    def convert_to_embed_url(self, url):
        if 'youtu.be' in url:
            video_id = url.split('/')[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        elif 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        return url


class MyFavouritesListView(LoginRequiredMixin, ListView) :
    template_name = 'list_resep_favorit.html'
    model = Recipe
    context_object_name = 'recipes'       
    paginate_by = 6    

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(like__user=user)


class ExternalRecipesView(View):
    template_name = 'external_list.html'

    def get(self, request):
        search_query = self.request.GET.get('c')
        if search_query :
            response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?c={search_query}')
        else :
            response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?c=seafood')
        data = response.json()
        
        return render(request, self.template_name, {'meals': data.get('meals', [])})
    
class ExternalDetailView(View):
    template_name = 'detail_external.html'

    def get(self, request, idMeal):
        # Fetch detail data for a specific meal
        response = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={idMeal}')
        data = response.json()

        meal = data.get('meals', [])[0] if data.get('meals') else None

        if meal:
            # Prepare ingredients and measurements as a list of tuples
            ingredients = [
                (meal.get(f"strIngredient{i}"), meal.get(f"strMeasure{i}"))
                for i in range(1, 21)
                if meal.get(f"strIngredient{i}")
            ]
        else:
            ingredients = []

        # Pass meal and ingredients to the template
        return render(request, self.template_name, {'meal': meal, 'ingredients': ingredients})