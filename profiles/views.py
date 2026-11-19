
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import StudentProfileForm
from .models import StudentProfile


def home(request):
    return render(request, 'home.html')


@login_required
def create_profile(request):

    if hasattr(request.user, 'studentprofile'):
        return redirect('view_profile')

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            return redirect('view_profile')

    else:
        form = StudentProfileForm()

    return render(
        request,
        'profiles/create_profile.html',
        {'form': form}
    )


@login_required
def view_profile(request):

    profile = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    return render(
        request,
        'profiles/view_profile.html',
        {'profile': profile}
    )


@login_required
def edit_profile(request):

    profile = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect('view_profile')

    else:
        form = StudentProfileForm(instance=profile)

    return render(
        request,
        'profiles/create_profile.html',
        {'form': form}
    )
