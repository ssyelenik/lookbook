# django_app/forms.py

# Import necessary modules and classes
from django import forms
from .models import Lookbook, Profile, LookbookImage
from cloudinary import CloudinaryImage

class ProfileUpdateForm(forms.ModelForm):

    """
    Form for updating user profile information, including profile picture and bio.

    Fields:
    - profile_picture: User's profile picture.
    - bio: User's biography.

    Methods:
    - __init__: Initializes form fields and modifies profile_picture label and widget.
    - save: Saves updated profile information, including handling profile picture upload to Cloudinary.
    """

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']  # 'profile_url' is not included as it seems to be derived from 'profile_picture'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].label = 'Upload Profile Picture'
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'profile_picture' in self.changed_data:
            
            # Save the instance first to ensure the profile picture is uploaded
            if commit:
                instance.save()

            # Extract the public_id from the CloudinaryField
            public_id = instance.profile_picture.public_id
            
            # Generate the profile URL with transformations
            profile_url = CloudinaryImage(public_id).build_url(quality='auto', width=600, height=600, crop='auto', gravity='face')
            instance.profile_url = profile_url
        if commit:
            instance.save()
        return instance


class LookbookForm(forms.ModelForm):

    """
    Form for creating or updating a lookbook.

    Fields:
    - title: Title of the lookbook.
    - description: Description of the lookbook.
    - overlay_image: Optional overlay image for the lookbook.

    Methods:
    - __init__: Initializes form fields and dynamically adds overlay_image field.
    - save: Saves the lookbook instance.
    """

    class Meta:
        model = Lookbook
        fields = ['title', 'description', 'overlay_image']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class LookbookImageForm(forms.ModelForm):
    
    """
    Form for handling LookbookImage model.

    Fields:
    - image: Image field for LookbookImage.

    Methods:
    - save: Saves the LookbookImage instance, including generating a transformed image URL using Cloudinary.
    """

    class Meta:
        model = LookbookImage
        fields = ['image']

    def save(self, commit=True, image_url=None):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
