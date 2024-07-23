from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile 
from campos.models import Campo

# Create your views here.
def index(request):
    campos = Campo.objects.all()
    return render(request, 'usuarios/index.html', {'campos': campos})

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('usuarios:index')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'usuarios/profile.html', {'form': form})