from django.shortcuts import render, redirect
from .forms import AppleTechNewsForm
from .models import AppleTechNews

def create_news(request):
    if request.method == 'POST':
        form = AppleTechNewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user 
            news.save()
            return redirect('news')
    else:
        form = AppleTechNewsForm()
    
    return render(request, 'news/create_news.html', {'form': form})

def news(request):
    news = AppleTechNews.objects.all().order_by('-created_at')
    return render(request, 'news/news.html', {'news': news})