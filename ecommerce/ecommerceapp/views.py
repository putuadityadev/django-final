from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView, 
    CreateView, 
    DetailView
)
from django.urls import reverse_lazy
from django.db.models import Q
from math import ceil
from ecommerceapp.models import Contact, Product, OrderUpdate, Orders



class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        allProds = []
        catprods = Product.objects.values('category', 'id')
        cats = {item['category'] for item in catprods}
        
        for cat in cats:
            prod = Product.objects.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n/4) - (n//4))
            allProds.append([prod, range(1, nSlides), nSlides])
        
        context['allProds'] = allProds
        return context

class ContactView(CreateView):
    model = Contact
    template_name = 'contact.html'
    fields = ['name', 'email', 'desc', 'phone_number']
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        # Simpan form dan dapatkan objek
        self.object = form.save()
        
        # Tambahkan pesan
        messages.success(self.request, 'We will get back to you soon...')
        
        return super().form_valid(form)

class ProductView(TemplateView):
    template_name = 'product.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ambil parameter dari request
        search_query = self.request.GET.get('search', '')
        category_filter = self.request.GET.get('category', '')
        sort_by = self.request.GET.get('sort', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')

        # Query dasar produk
        products = Product.objects.all()

        # Filtering berdasarkan search
        if search_query:
            products = products.filter(
                Q(product_name__icontains=search_query) | 
                Q(desc__icontains=search_query)
            )

        # Filtering berdasarkan kategori
        if category_filter:
            products = products.filter(category=category_filter)

        # Filtering berdasarkan harga
        if min_price and max_price:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
                products = products.filter(price__range=(min_price, max_price))
            except ValueError:
                # Jika konversi ke float gagal, abaikan filter harga
                pass
        elif min_price:
            try:
                min_price = float(min_price)
                products = products.filter(price__gte=min_price)
            except ValueError:
                pass
        elif max_price:
            try:
                max_price = float(max_price)
                products = products.filter(price__lte=max_price)
            except ValueError:
                pass

        # Sorting
        if sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')
        elif sort_by == 'newest':
            products = products.order_by('-id')

        # Persiapkan data untuk template
        allProds = []
        catprods = products.values('category', 'id')
        cats = {item['category'] for item in catprods}
        
        for cat in cats:
            prod = products.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n/4) - (n//4))
            allProds.append([prod, range(1, nSlides), nSlides])
        
        # Tambahkan data ke context
        context['allProds'] = allProds
        
        # Tambahkan daftar kategori untuk filter
        context['categories'] = list(set(Product.objects.values_list('category', flat=True)))
        
        # Tambahkan parameter search untuk mempertahankan filter
        context['search_query'] = search_query
        context['selected_category'] = category_filter
        context['sort_by'] = sort_by
        context['min_price'] = min_price
        context['max_price'] = max_price

        return context
class CheckoutView(LoginRequiredMixin, CreateView):
    model = Orders
    template_name = 'checkout.html'
    fields = ['items_json', 'name', 'amount', 'email', 'address1', 
            'address2', 'city', 'state', 'zip_code', 'phone']
    success_url = reverse_lazy('home')  # Sesuaikan dengan nama URL home Anda

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Login & Try Again")
            return redirect('/auth/login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Tambahkan logika OrderUpdate
        update = OrderUpdate(
            order_id=self.object.order_id, 
            update_desc="the order has been placed"
        )
        update.save()
        
        return response

class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail-product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'