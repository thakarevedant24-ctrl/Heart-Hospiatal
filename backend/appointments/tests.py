import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.utils.html import escape

from departments.models import Department
from doctors.models import Doctor
from appointments.models import Appointment

class AppointmentBookingTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create test departments
        self.dept_cardio = Department.objects.create(
            name="Cardiology & Vascular Center",
            slug="cardiology-vascular-center",
            icon="bi-heart-pulse-fill",
            short_description="Comprehensive cardiovascular diagnostics and surgical intervention.",
            full_description="State-of-the-art heart care center with emergency cardiac catheterization."
        )
        self.dept_neuro = Department.objects.create(
            name="Neurology & Brain Sciences",
            slug="neurology-brain-sciences",
            icon="bi-activity",
            short_description="Comprehensive neurological diagnosis and stroke rehabilitation.",
            full_description="Full neurology department."
        )

        # Create test doctors
        self.doc_cardio = Doctor.objects.create(
            name="Rajesh",
            department=self.dept_cardio,
            specialization="Interventional Cardiology",
            qualification="MD, FACC",
            experience_years=16,
            bio="Leading cardiovascular interventionalist.",
            available_days="Mon-Thu",
            is_active=True
        )
        self.doc_neuro = Doctor.objects.create(
            name="Arjun",
            department=self.dept_neuro,
            specialization="Adult Neurology",
            qualification="MD, PhD",
            experience_years=12,
            bio="Specialist in complex neurodegenerative conditions.",
            available_days="Tue-Sat",
            is_active=True
        )

        self.tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.yesterday = datetime.date.today() - datetime.timedelta(days=1)

    def test_book_appointment_get(self):
        """GET /appointments/ renders form with status 200."""
        response = self.client.get(reverse('appointments:book_appointment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/book_appointment.html')
        self.assertContains(response, 'Patient Full Name')
        self.assertContains(response, 'Preferred Consultation Date')
        self.assertContains(response, '09:00 AM')

    def test_book_alias_route_get(self):
        """GET /book/ route alias also renders booking form."""
        response = self.client.get('/book/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/book_appointment.html')

    def test_prefill_by_doctor_id(self):
        """Deep-link ?doctor=<id> pre-selects doctor and their department."""
        url = f"{reverse('appointments:book_appointment')}?doctor={self.doc_cardio.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Booking with Dr. {self.doc_cardio.name}")
        self.assertEqual(response.context['form']['department'].value(), self.dept_cardio.id)
        self.assertEqual(response.context['form']['doctor'].value(), self.doc_cardio.id)

    def test_prefill_by_department_slug(self):
        """Deep-link ?department=<slug> pre-selects department."""
        url = f"{reverse('appointments:book_appointment')}?department={self.dept_cardio.slug}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Booking in {escape(self.dept_cardio.name)}")
        self.assertEqual(response.context['form']['department'].value(), self.dept_cardio.id)

    def test_api_doctors_by_department(self):
        """AJAX endpoint returns active doctors for requested department."""
        url = f"{reverse('appointments:api_doctors')}?department_id={self.dept_cardio.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('doctors', data)
        self.assertEqual(len(data['doctors']), 1)
        self.assertEqual(data['doctors'][0]['id'], self.doc_cardio.id)
        self.assertEqual(data['doctors'][0]['name'], self.doc_cardio.name)

    def test_book_appointment_post_valid(self):
        """Submitting valid booking data creates appointment with pending status, sends email, and redirects."""
        post_data = {
            'patient_name': 'Sarah Connor',
            'email': 'sconnor@example.com',
            'phone': '+1 (555) 345-6789',
            'department': self.dept_cardio.id,
            'doctor': self.doc_cardio.id,
            'preferred_date': self.tomorrow.isoformat(),
            'preferred_time': '10:30:00',
            'notes': 'Routine annual cardiac stress test checkup.',
        }

        response = self.client.post(reverse('appointments:book_appointment'), data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/booking_confirmation.html')

        # Check database
        appointment = Appointment.objects.filter(email='sconnor@example.com').first()
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.patient_name, 'Sarah Connor')
        self.assertEqual(appointment.department, self.dept_cardio)
        self.assertEqual(appointment.doctor, self.doc_cardio)
        self.assertEqual(appointment.status, 'pending')
        self.assertEqual(appointment.preferred_date, self.tomorrow)

        # Check confirmation message and reference on confirmation page
        ref_code = f"CHH-{appointment.id:05d}"
        self.assertContains(response, ref_code)
        self.assertContains(response, 'Sarah Connor')

        # Check confirmation email was dispatched
        self.assertGreaterEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[-1]
        self.assertIn(ref_code, sent_mail.subject)
        self.assertIn('Sarah Connor', sent_mail.body)
        self.assertIn('sconnor@example.com', sent_mail.to)

    def test_book_appointment_post_past_date_fails(self):
        """Past dates must fail validation."""
        post_data = {
            'patient_name': 'John Reese',
            'email': 'jreese@example.com',
            'phone': '+1 (555) 999-0000',
            'department': self.dept_cardio.id,
            'doctor': self.doc_cardio.id,
            'preferred_date': self.yesterday.isoformat(),
            'preferred_time': '10:00:00',
        }

        response = self.client.post(reverse('appointments:book_appointment'), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'preferred_date', 'Preferred appointment date cannot be in the past.')
        self.assertEqual(Appointment.objects.filter(email='jreese@example.com').count(), 0)

    def test_book_appointment_post_doctor_department_mismatch(self):
        """Selecting a doctor that belongs to another department must fail validation."""
        post_data = {
            'patient_name': 'Miles Dyson',
            'email': 'mdyson@example.com',
            'phone': '+1 (555) 777-8888',
            'department': self.dept_cardio.id,
            'doctor': self.doc_neuro.id,  # Neuro doctor with Cardio department!
            'preferred_date': self.tomorrow.isoformat(),
            'preferred_time': '11:00:00',
        }

        response = self.client.post(reverse('appointments:book_appointment'), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'],
            'doctor',
            f"Dr. {self.doc_neuro.name} is in the {self.dept_neuro.name} department, not {self.dept_cardio.name}."
        )
        self.assertEqual(Appointment.objects.filter(email='mdyson@example.com').count(), 0)

    def test_booking_confirmation_view(self):
        """Direct access to confirmation page renders summary and reference code."""
        appointment = Appointment.objects.create(
            patient_name='Grace Hopper',
            email='ghopper@example.com',
            phone='+1 (555) 123-4567',
            department=self.dept_neuro,
            doctor=self.doc_neuro,
            preferred_date=self.tomorrow,
            preferred_time=datetime.time(14, 30),
            notes='Follow-up headache assessment',
            status='pending'
        )

        url = reverse('appointments:booking_confirmation', kwargs={'pk': appointment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"CHH-{appointment.id:05d}")
        self.assertContains(response, "Grace Hopper")
        self.assertContains(response, escape(self.dept_neuro.name))
        self.assertContains(response, self.doc_neuro.name)
