from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import AppleTechNews
from .forms import AppleTechNewsForm

class NewsListView(ListView):
    model = AppleTechNews
    template_name = 'news/news.html'  # Pastikan sesuai dengan nama template Anda
    context_object_name = 'news'  # Sesuai dengan variabel di template
    ordering = ['-created_at']
    paginate_by = 9  # Opsional: untuk pagination

class CreateNewsView(LoginRequiredMixin, CreateView):
    model = AppleTechNews
    form_class = AppleTechNewsForm
    template_name = 'news/create_news.html'  # Pastikan sesuai dengan nama template Anda
    success_url = reverse_lazy('news')  # Redirect ke halaman news setelah berhasil

    def form_valid(self, form):
        # Set the author to the current logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Tambahkan class form-control ke semua field
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
        return form