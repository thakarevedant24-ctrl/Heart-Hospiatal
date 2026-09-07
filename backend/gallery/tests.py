from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import GalleryImage

class GalleryViewTests(TestCase):
    def setUp(self):
        # Create a small dummy image for testing
        dummy_image = SimpleUploadedFile(
            name='test_hospital.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )
        self.image = GalleryImage.objects.create(
            title='Main Surgical Pavilion',
            image=dummy_image
        )

    def tearDown(self):
        if self.image and self.image.image:
            self.image.image.delete(save=False)

    def test_gallery_list_page_loads(self):
        response = self.client.get(reverse('gallery:gallery_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery/gallery_list.html')
        self.assertContains(response, 'Main Surgical Pavilion')
        self.assertContains(response, 'id="galleryLightbox"')

    def test_gallery_does_not_contain_old_category_tabs(self):
        response = self.client.get(reverse('gallery:gallery_list'))
        # Should not contain category buttons or old filter tabs
        self.assertNotContains(response, 'id="galleryFilterTabs"')
        self.assertNotContains(response, 'data-category="Hospital"')
        self.assertNotContains(response, 'data-category="Equipment"')
        self.assertNotContains(response, 'data-category="Rooms"')
        self.assertNotContains(response, 'data-category="Events"')
