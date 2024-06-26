# django_app/utils.py
# Import necessary modules and classes
from cloudinary import CloudinaryImage
from urllib.parse import urlparse
import json
from .models import LookbookImage

def generate_transformation_options(lookbook):

    """
    Generate Cloudinary transformation options based on the lookbook's attributes.

    Args:
    - lookbook: Lookbook instance from which transformation options are generated.

    Returns:
    - transformation_options: Dictionary containing Cloudinary transformation options.
    """

    # Determine width and height based on orientation
    if lookbook.orientation == 'portrait':
        width, height = 400, 500
    elif lookbook.orientation == 'landscape':
        width, height = 800, 600
    else:  # square
        width, height = 800, 800

    # Initialize transformation list if not already present
    transformation_options = {                    }

    if 'transformation' not in transformation_options:
        transformation_options['transformation'] = []

    # Apply border style if border width is not '0px'
    if lookbook.border_width != '0px':
        transformation_options['border'] = f'{lookbook.border_width}_solid_{lookbook.border_color}'
                    
    # Define base transformation options
    all_transformation = [
        {'quality': 'auto',
        'width': width,
        'height': height,
        'crop': 'pad',
        'background': 'gen_fill:ignore-foreground_true'}
    ]
    transformation_options['transformation'].insert(0, all_transformation)

    # Apply overlay image if provided
    if lookbook.overlay_image:
        overlay_transformation = [
            {'overlay': lookbook.overlay_image, 'gravity': 'north_east', 'width': 100, 'flags': 'layer_apply', 'x': 20, 'y': 20, 'opacity': 80}
        ]
        transformation_options['transformation'].insert(1, overlay_transformation)

    # Add a scale transformation to make the width 800
    transformation_options['transformation'].insert(2, {'width': 800, 'crop': 'scale'})
    return transformation_options

def get_public_id_from_url(url):

    """
    Extracts public ID from a Cloudinary URL.

    Args:
    - url: Cloudinary URL of the image.

    Returns:
    - public_id: Public ID extracted from the URL.
    """

    parsed_url = urlparse(url)
    return parsed_url.path.split('/')[-1].split('.')[0]

def create_transformed_url(public_id, transformation_options):

    """
    Creates a transformed URL using CloudinaryImage build_url method.

    Args:
    - public_id: Public ID of the image on Cloudinary.
    - transformation_options: Dictionary containing transformation options.

    Returns:
    - transformed_url: URL of the transformed image.
    """

    return CloudinaryImage(public_id).build_url(**transformation_options)

def process_image_urls(image_urls, lookbook):
    
    """
    Processes a list of image URLs, applies transformations, and saves to database.

    Args:
    - image_urls: JSON string containing image URLs.
    - lookbook: Lookbook instance associated with the images.
    """

    if image_urls:
        image_urls = json.loads(image_urls)
        for url in image_urls:
            public_id = get_public_id_from_url(url)
            transformation_options = generate_transformation_options(lookbook)
            transformed_url = create_transformed_url(public_id, transformation_options)
            LookbookImage.objects.create(
                lookbook=lookbook,
                image=url,
                transformed_image=transformed_url
            )
