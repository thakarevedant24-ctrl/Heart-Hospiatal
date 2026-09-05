from django.test import TestCase, Client
from django.urls import reverse
from departments.models import Department
from doctors.models import Doctor


class SiteWideSEOResponsivenessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.dept = Department.objects.create(
            name="General Surgery",
            slug="general-surgery",
            icon="bi-bandaid",
            short_description="Specialized surgical intervention",
            full_description="State-of-the-art general and laparoscopic surgery"
        )
        self.doctor = Doctor.objects.create(
            name="John Watson",
            department=self.dept,
            specialization="General Surgery",
            qualification="MD, FACS",
            experience_years=10,
            bio="Experienced general surgeon.",
            available_days="Mon-Fri",
            is_active=True
        )

    def test_base_seo_elements_present_on_home(self):
        """Home page includes meta description, OG tags, favicon, skip link, and floating buttons."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

        # Meta SEO & Open Graph
        self.assertContains(response, '<meta name="description"')
        self.assertContains(response, '<meta property="og:title"')
        self.assertContains(response, '<meta property="og:description"')
        self.assertContains(response, '<meta property="og:image"')
        self.assertContains(response, '<meta property="og:url"')
        self.assertContains(response, '<meta name="twitter:card"')

        # Favicon
        self.assertContains(response, 'favicon.')

        # Accessibility
        self.assertContains(response, 'skip-to-main-link')
        self.assertContains(response, 'id="main-content"')

        # Floating Action Buttons
        self.assertContains(response, 'id="backToTopBtn"')
        self.assertContains(response, 'whatsapp-btn')
        self.assertContains(response, 'wa.me/15550107890')

        # Scroll-reveal classes
        self.assertContains(response, 'reveal-on-scroll')

    def test_about_page_seo_and_structure(self):
        """About page renders with customized meta description and timeline."""
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Discover Harborlight Multispecialty Hospital')
        self.assertContains(response, 'reveal-on-scroll')

    def test_contact_page_seo_and_accessibility(self):
        """Contact page includes proper meta tags, iframe title, and form labels."""
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Harborlight Multispecialty Hospital')
        self.assertContains(response, 'title="Harborlight Multispecialty Hospital Location"')

    def test_departments_and_doctors_meta_tags(self):
        """Department and Doctor pages contain custom titles and meta descriptions."""
        dept_url = reverse('departments:department_detail', kwargs={'slug': self.dept.slug})
        resp_dept = self.client.get(dept_url)
        self.assertEqual(resp_dept.status_code, 200)
        self.assertContains(resp_dept, self.dept.name)

        doc_url = reverse('doctors:doctor_detail', kwargs={'pk': self.doctor.pk})
        resp_doc = self.client.get(doc_url)
        self.assertEqual(resp_doc.status_code, 200)
        self.assertContains(resp_doc, f"Dr. {self.doctor.name}")
        self.assertContains(resp_doc, "Book an appointment with Dr. John Watson")
