from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, FavoriteProduct
from .forms import UserUpdateForm, ProfileUpdateForm
from ecommerceapp.models import Product



@login_required
def editprofile(request):
    # Pastikan profil selalu ada
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('view_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'myprofile/edit_profile.html', context)


@login_required
def view_profile(request):
    profile = Profile.objects.get(user=request.user)
    favorite_products = FavoriteProduct.objects.filter(user=request.user)
    
    context = {
        'profile': profile,
        'favorite_products': favorite_products,
    }
    
    return render(request, 'myprofile/view_profile.html', context)

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Cek apakah produk sudah ada di favorit
    favorite, created = FavoriteProduct.objects.get_or_create(
        user=request.user, 
        product=product
    )
    
    if not created:
        # Jika sudah ada, hapus dari favorit
        favorite.delete()
        messages.warning(request, f"{product.product_name} removed from favorites")
    else:
        messages.success(request, f"{product.product_name} added to favorites")
    
    # Kembali ke halaman sebelumnya
    return redirect(request.META.get('HTTP_REFERER', 'product'))