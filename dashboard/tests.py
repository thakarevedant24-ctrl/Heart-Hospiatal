import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from appointments.models import Appointment
from departments.models import Department
from doctors.models import Doctor
from core.models import ContactMessage


class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create normal user without is_staff (to verify "remove staff" requirement)
        self.regular_user = User.objects.create_user(
            username='clinic_manager',
            password='ComplexPassword123!',
            is_staff=False,
            is_superuser=False
        )

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin_boss',
            password='AdminPassword123!',
            email='admin@example.com'
        )

        # Create test department & doctor
        self.dept = Department.objects.create(
            name='Internal Medicine',
            slug='internal-medicine',
            icon='bi-capsule',
            short_description='Primary and acute internal care',
            full_description='Comprehensive adult primary care'
        )
        self.doctor = Doctor.objects.create(
            name='Rachel Zane',
            department=self.dept,
            specialization='General Internist',
            qualification='MD',
            experience_years=8,
            bio='General medicine specialist',
            available_days='Mon-Fri',
            is_active=True
        )

        # Create appointments
        self.today = datetime.date.today()
        self.pending_appt = Appointment.objects.create(
            patient_name='Arthur Dent',
            email='adent@example.com',
            phone='+1 (555) 111-2222',
            department=self.dept,
            doctor=self.doctor,
            preferred_date=self.today,
            preferred_time=datetime.time(10, 0),
            notes='Annual wellness physical',
            status='pending'
        )

        # Create contact message
        self.unread_msg = ContactMessage.objects.create(
            name='Ford Prefect',
            email='fprefect@example.com',
            phone='+1 (555) 333-4444',
            subject='Visiting Hours Inquiry',
            message='What are the ICU visiting hours on weekends?',
            is_read=False
        )

    def test_login_page_renders_and_aliases_work(self):
        """Login page renders at /login/, /admin-login/, and /staff-login/."""
        for path in ['/login/', '/admin-login/', '/staff-login/']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'dashboard/login.html')
            self.assertContains(response, 'Administrative Login')

    def test_login_success_and_redirect(self):
        """Logging in with valid credentials redirects to dashboard."""
        response = self.client.post(reverse('admin_login'), {
            'username': 'clinic_manager',
            'password': 'ComplexPassword123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'clinic_manager')

    def test_login_invalid_credentials(self):
        """Invalid credentials show error without authenticating."""
        response = self.client.post(reverse('admin_login'), {
            'username': 'clinic_manager',
            'password': 'WrongPassword!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/login.html')
        self.assertContains(response, 'Invalid username or password')

    def test_dashboard_unauthenticated_redirects(self):
        """Unauthenticated access redirects to login."""
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_dashboard_accessible_by_non_staff_user(self):
        """Non-staff authenticated user can access the dashboard (satisfying 'remove staff')."""
        self.client.login(username='clinic_manager', password='ComplexPassword123!')
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'Operational Dashboard')
        self.assertContains(response, 'Arthur Dent')
        self.assertContains(response, 'Ford Prefect')

    def test_dashboard_metrics_counts(self):
        """Dashboard displays accurate operational metrics."""
        self.client.login(username='clinic_manager', password='ComplexPassword123!')
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['appointments_today_count'], 1)
        self.assertEqual(response.context['pending_appointments_count'], 1)
        self.assertEqual(response.context['unread_messages_count'], 1)

    def test_update_appointment_status_confirm_via_ajax(self):
        """AJAX POST confirming appointment updates database and returns JSON."""
        self.client.login(username='clinic_manager', password='ComplexPassword123!')
        url = reverse('dashboard:update_appointment_status', kwargs={'pk': self.pending_appt.pk})

        response = self.client.post(
            url,
            data={'action': 'confirm'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'confirmed')

        self.pending_appt.refresh_from_db()
        self.assertEqual(self.pending_appt.status, 'confirmed')

    def test_update_appointment_status_cancel_via_standard_post(self):
        """Standard form POST cancelling appointment updates database and redirects."""
        self.client.login(username='clinic_manager', password='ComplexPassword123!')
        url = reverse('dashboard:update_appointment_status', kwargs={'pk': self.pending_appt.pk})

        response = self.client.post(url, data={'action': 'cancel'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

        self.pending_appt.refresh_from_db()
        self.assertEqual(self.pending_appt.status, 'cancelled')

    def test_mark_message_read_via_ajax(self):
        """AJAX POST marking message read updates is_read flag and returns JSON."""
        self.client.login(username='clinic_manager', password='ComplexPassword123!')
        url = reverse('dashboard:mark_message_read', kwargs={'pk': self.unread_msg.pk})

        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])

        self.unread_msg.refresh_from_db()
        self.assertTrue(self.unread_msg.is_read)

    def test_admin_logout(self):
        """Logging out clears session and redirects to login."""
        self.client.login(username='clinic_manager', password='ComplexPassword123!')
        response = self.client.get(reverse('admin_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
