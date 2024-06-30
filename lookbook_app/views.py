# django_app/views.py
# Import necessary modules and functions
from django.shortcuts import render, redirect, get_object_or_404
from .models import Lookbook, Profile, LookbookImage
from .forms import ProfileUpdateForm, LookbookForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from .utils import process_image_urls, generate_transformation_options, get_public_id_from_url, create_transformed_url
from django.contrib.auth.models import User
import cloudinary.uploader
import ast


def signup(request):

    """
    Handles user signup functionality.

    POST method:
    - Validates user creation form.
    - Redirects to login upon successful signup.

    GET method:
    - Renders signup form.

    """

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request):

    """
    Handles user profile view and updates.

    GET method:
    - Retrieves or creates Profile instance for the current user.
    - Renders profile update form.

    POST method:
    - Validates profile update form.
    - Updates profile information including profile picture.
    - Redirects to profile page upon successful update.

    """

    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile.html', {
        'form': form,
        'profile': profile
    })


@login_required
def create_lookbook(request):

    """
    Handles creation of a new lookbook.

    POST method:
    - Validates lookbook creation form.
    - Saves the new lookbook instance with user-provided data and optional overlay image.
    - Add the lookbook to the user's profile.
    - Saves associated images with transformations.
    - Redirects to display page of the created lookbook upon success.

    GET method:
    - Renders lookbook creation form.

    """
    
    if request.method == 'POST':
        lookbook_form = LookbookForm(request.POST, request.FILES)
        if lookbook_form.is_valid():
            lookbook = lookbook_form.save(commit=False)
            lookbook.user = request.user
            lookbook.orientation = request.POST.get('orientation', 'square')
            lookbook.border_width = request.POST.get('borderWidth', '0px')
            lookbook.border_color = request.POST.get('borderColor', 'black')

            lookbook.save()

            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.my_lookbooks.add(lookbook)

            image_urls = request.POST.get('image_urls')
            process_image_urls(image_urls, lookbook)

            return HttpResponseRedirect(reverse('display', args=[lookbook.id]))
    else:
        lookbook_form = LookbookForm()
    return render(request, 'create_lookbook.html', {'lookbook_form': lookbook_form})


def display(request, lookbook_id):

    """
    Displays a specific lookbook and its images.

    Args:
    - lookbook_id: ID of the lookbook to display.

    """

    lookbook = get_object_or_404(Lookbook, pk=lookbook_id)
    images = lookbook.images.all()
    return render(request, 'display.html', {'photos': images, 'lookbook': lookbook})


@login_required
def edit_lookbook(request, lookbook_id):

    """
    Handles editing of an existing lookbook.

    Args:
    - lookbook_id: ID of the lookbook to edit.

    POST method:
    - Validates lookbook edit form.
    - Updates lookbook information including optional overlay image.
    - Updates associated images with transformations.
    - Deletes selected images.
    - Redirects to display page of the edited lookbook upon success.

    GET method:
    - Retrieves and renders lookbook edit form.

    """

    lookbook = get_object_or_404(Lookbook, pk=lookbook_id, user=request.user)

    if request.method == 'POST':
        form = LookbookForm(request.POST, request.FILES, instance=lookbook)
        if form.is_valid():
            lookbook = form.save(commit=False)
            lookbook.orientation = request.POST.get('orientation', lookbook.orientation)
            lookbook.border_width = request.POST.get('borderWidth', lookbook.border_width)
            lookbook.border_color = request.POST.get('borderColor', lookbook.border_color)
            overlay_image = request.FILES.get('overlay_image')

            if overlay_image:
                lookbook.overlay_image = overlay_image.name.split('.')[0]
                cloudinary.uploader.upload(overlay_image)
            lookbook.save()

            image_urls = request.POST.get('img_urls')
            process_image_urls(image_urls, lookbook)

            for image in lookbook.images.all():
                public_id = get_public_id_from_url(image.image.url)
                transformation_options = generate_transformation_options(lookbook)
                transformed_url = create_transformed_url(public_id, transformation_options)
                image.transformed_image = transformed_url
                image.save()

            if request.POST.get('imagesToDelete'):
                image_ids_to_delete = request.POST.getlist('imagesToDelete')
                LookbookImage.objects.filter(id__in=image_ids_to_delete).delete()

            return HttpResponseRedirect(reverse('display', args=[lookbook.id]))
    else:
        form = LookbookForm(instance=lookbook)

    context = {
        'form': form,
        'lookbook': lookbook,
        'image_urls': json.dumps(list(lookbook.images.values_list('transformed_image', flat=True))),
        'orientation': lookbook.orientation,
        'borderWidth': lookbook.border_width,
        'borderColor': lookbook.border_color,
        'current_overlay': lookbook.overlay_image,
        'images': lookbook.images.all(),
    }
    return render(request, 'edit_lookbook.html', context)


@login_required
def my_lookbooks(request):

    """
    Lists the current user's lookbooks and handles deletion of selected lookbooks.

    GET method:
    - Retrieves or creates Profile instance for the current user.
    - Fetches all lookbooks associated with the user's profile.
    - Renders 'my_lookbooks.html' template with the user's lookbooks.

    POST method:
    - Deletes selected lookbooks based on IDs received from POST data.
    - Redirects to 'my_lookbooks' page after deletion.

    """

    profile, _ = Profile.objects.get_or_create(user=request.user)
    my_lookbooks = profile.my_lookbooks.all().order_by('title')

    if request.method == 'POST':
        temp_ids=request.POST.getlist('lookbook_ids')
        
        for temp in temp_ids:
            ids = ast.literal_eval(temp)
            lookbook_ids = [int(item) for item in ids]
        
        Lookbook.objects.filter(id__in=lookbook_ids).delete()
        return redirect('my_lookbooks')

    return render(request, 'my_lookbooks.html', {'my_lookbooks': my_lookbooks})

# View for listing all lookbooks    
def all_lookbooks(request):
    """
    Lists all lookbooks from selected users or all users.
    GET method:
    - Fetches all users from the database.
    - Retrieves selected user IDs from request GET parameters.
    - If no specific user IDs or 'all' is selected, fetches all users' lookbooks.
    - Renders 'all_lookbooks.html' template with the fetched lookbooks and users.
    """
    
    users = User.objects.all()
    user_ids = request.GET.getlist('user_ids')
    
    if not user_ids or 'all' in user_ids:
        user_ids = [str(user.id) for user in users]
    
    lookbooks = Lookbook.objects.filter(user__id__in=user_ids).order_by('title')
    return render(request, 'all_lookbooks.html', {'lookbooks': lookbooks, 'users': users, 'selected_user_ids': user_ids})
