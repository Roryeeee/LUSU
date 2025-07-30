from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  # Only this import

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()  # Use the same form here too
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def dashboard_view(request):
    user = request.user
    is_admin = user.groups.filter(name='Admin').exists()
    is_moderator = user.groups.filter(name='Moderator').exists()

    return render(request, 'accounts/dashboard.html', {
        'is_admin': is_admin,
        'is_moderator': is_moderator,
    })
