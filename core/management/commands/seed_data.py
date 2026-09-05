from django.core.management.base import BaseCommand
from departments.models import Department, Service
from doctors.models import Doctor
from core.models import Testimonial

class Command(BaseCommand):
    help = 'Seeds initial demonstration data for Harborlight Hospital'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial data...')

        # 1. Departments
        depts_data = [
            {
                'name': 'Cardiology & Vascular Center',
                'icon': 'bi-heart-pulse-fill',
                'short_description': 'Advanced diagnostics, catheterization laboratory, and non-invasive cardiac intensive care.',
                'full_description': 'Our Cardiology department provides comprehensive preventive, diagnostic, and therapeutic heart care with state-of-the-art hybrid catheterization labs and echocardiography suites.'
            },
            {
                'name': 'Neurology & Neurosurgery',
                'icon': 'bi-cpu-fill',
                'short_description': 'Comprehensive brain, spine, and nervous system care with a 24/7 dedicated stroke emergency team.',
                'full_description': 'Specialized neurology department equipped with modern electroencephalogram (EEG), electromyogram (EMG), and stereotactic neurosurgical operating facilities.'
            },
            {
                'name': 'Pediatrics & Child Wellness',
                'icon': 'bi-emoji-smile-fill',
                'short_description': 'Gentle, compassionate medical care for infants, adolescents, and children, backed by Level-III NICU.',
                'full_description': 'Dedicated to the holistic wellness and acute medical care of children from newborn to adolescence with family-centered care suites.'
            },
            {
                'name': 'Orthopedics & Sports Medicine',
                'icon': 'bi-person-arms-up',
                'short_description': 'Minimally invasive joint replacements, robotic spine surgery, and sports injury rehabilitation.',
                'full_description': 'Specializing in computer-assisted arthroplasty, complex trauma repair, spine stabilization, and physical rehabilitation.'
            },
            {
                'name': 'Emergency & Trauma Care',
                'icon': 'bi-hospital-fill',
                'short_description': 'Round-the-clock level-1 trauma readiness with dedicated ambulance dispatch and ICU triage.',
                'full_description': 'Rapid resuscitation and emergency stabilization center operational 24 hours a day, 365 days a year.'
            },
            {
                'name': 'Oncology & Infusion Center',
                'icon': 'bi-shield-shaded',
                'short_description': 'Integrated medical and surgical cancer care with compassionate infusion and oncology suites.',
                'full_description': 'State-of-the-art chemotherapy administration, precision oncology, immunotherapy, and dedicated patient support counseling.'
            },
        ]

        departments_dict = {}
        for d in depts_data:
            dept, created = Department.objects.get_or_create(
                name=d['name'],
                defaults={
                    'icon': d['icon'],
                    'short_description': d['short_description'],
                    'full_description': d['full_description']
                }
            )
            departments_dict[dept.name] = dept
            if created:
                self.stdout.write(f"Created Department: {dept.name}")

        # 2. Doctors
        doctors_data = [
            {
                'name': 'Elena Rostova',
                'department': departments_dict['Cardiology & Vascular Center'],
                'specialization': 'Interventional Cardiologist',
                'qualification': 'MD, FACC, FSCAI',
                'experience_years': 16,
                'bio': 'Pioneering specialist in structural heart disease, complex angioplasty, and preventative cardiology.',
                'available_days': 'Mon - Thu',
                'is_active': True,
            },
            {
                'name': 'Marcus Chen',
                'department': departments_dict['Neurology & Neurosurgery'],
                'specialization': 'Senior Neurosurgeon',
                'qualification': 'MD, FACS, FAANS',
                'experience_years': 18,
                'bio': 'Internationally recognized for minimally invasive brain surgery, spinal decompression, and cerebrovascular therapy.',
                'available_days': 'Mon, Wed, Fri',
                'is_active': True,
            },
            {
                'name': 'Sarah Jenkins',
                'department': departments_dict['Pediatrics & Child Wellness'],
                'specialization': 'Consultant Pediatrician',
                'qualification': 'MD, FAAP',
                'experience_years': 12,
                'bio': 'Passionate advocate for pediatric preventive care, neonatal stabilization, and developmental health.',
                'available_days': 'Mon - Fri',
                'is_active': True,
            },
            {
                'name': 'David Thorne',
                'department': departments_dict['Orthopedics & Sports Medicine'],
                'specialization': 'Orthopedic & Joint Surgeon',
                'qualification': 'MBBS, MS (Ortho), FAAOS',
                'experience_years': 15,
                'bio': 'Expert in robotic total knee and hip replacements and arthroscopic sports tendon reconstructions.',
                'available_days': 'Tue, Thu, Sat',
                'is_active': True,
            },
            {
                'name': 'Amina Al-Mansoor',
                'department': departments_dict['Emergency & Trauma Care'],
                'specialization': 'Emergency Care Director',
                'qualification': 'MD, FACEP',
                'experience_years': 14,
                'bio': 'Dedicated to rapid trauma triage, critical care resuscitation, and emergency patient stabilization.',
                'available_days': '24/7 Roster',
                'is_active': True,
            },
            {
                'name': 'Jonathan Ross',
                'department': departments_dict['Oncology & Infusion Center'],
                'specialization': 'Medical Oncologist',
                'qualification': 'MD, PhD, FACP',
                'experience_years': 20,
                'bio': 'Focusing on targeted genomic cancer therapies, immunotherapy protocols, and compassionate oncology care.',
                'available_days': 'Mon - Thu',
                'is_active': True,
            },
        ]

        for doc_info in doctors_data:
            doc, created = Doctor.objects.get_or_create(
                name=doc_info['name'],
                department=doc_info['department'],
                defaults={
                    'specialization': doc_info['specialization'],
                    'qualification': doc_info['qualification'],
                    'experience_years': doc_info['experience_years'],
                    'bio': doc_info['bio'],
                    'available_days': doc_info['available_days'],
                    'is_active': doc_info['is_active'],
                }
            )
            if created:
                self.stdout.write(f"Created Doctor: Dr. {doc.name}")

        # 3. Testimonials
        testimonials_data = [
            {
                'patient_name': 'Eleanor Vance',
                'message': 'The cardiology team at Harborlight provided extraordinary care during my surgery. Every doctor and nurse treated me with deep kindness and patience.',
                'rating': 5,
                'is_approved': True,
            },
            {
                'patient_name': 'Robert Martinez',
                'message': 'From the moment I checked in at Emergency to my discharge after orthopedic rehabilitation, the staff went above and beyond. Truly modern medicine with a human touch.',
                'rating': 5,
                'is_approved': True,
            },
            {
                'patient_name': 'Sophie Lin & Family',
                'message': 'Dr. Jenkins took such great care of our daughter during her hospital stay. Harborlight’s pediatric department is warm, reassuring, and second to none.',
                'rating': 5,
                'is_approved': True,
            },
            {
                'patient_name': 'Thomas Sterling',
                'message': 'The state-of-the-art facilities and knowledgeable specialists made all the difference in my recovery. Booking was seamless and the care was outstanding.',
                'rating': 5,
                'is_approved': True,
            },
        ]

        # 4. Services
        services_data = [
            {
                'title': 'Echocardiography & Doppler Study',
                'department': departments_dict['Cardiology & Vascular Center'],
                'icon': 'bi-activity',
                'short_description': 'Advanced non-invasive cardiac imaging evaluating heart chambers, valves, and systemic blood circulation.'
            },
            {
                'title': 'Cardiac Catheterization & Angioplasty',
                'department': departments_dict['Cardiology & Vascular Center'],
                'icon': 'bi-heart-pulse-fill',
                'short_description': 'Minimally invasive diagnostic angiograms, stent placements, and coronary artery disease interventions.'
            },
            {
                'title': 'Comprehensive Stroke Unit & Thrombolysis',
                'department': departments_dict['Neurology & Neurosurgery'],
                'icon': 'bi-lightning-fill',
                'short_description': 'Rapid response acute stroke assessment, clot-busting thrombolysis, and endovascular interventions.'
            },
            {
                'title': 'Minimally Invasive Spine & Brain Surgery',
                'department': departments_dict['Neurology & Neurosurgery'],
                'icon': 'bi-cpu-fill',
                'short_description': 'Microscopic and endoscopic neurosurgical interventions for spinal discs, tumors, and cranial conditions.'
            },
            {
                'title': 'Level-III Neonatal Intensive Care (NICU)',
                'department': departments_dict['Pediatrics & Child Wellness'],
                'icon': 'bi-shield-heart',
                'short_description': 'Dedicated multi-bed intensive care nursery for premature infants and critically ill newborns.'
            },
            {
                'title': 'Pediatric Wellness & Immunization',
                'department': departments_dict['Pediatrics & Child Wellness'],
                'icon': 'bi-emoji-smile-fill',
                'short_description': 'Comprehensive infant developmental checkups, preventative pediatric screenings, and scheduled vaccines.'
            },
            {
                'title': 'Robotic Total Joint Replacement',
                'department': departments_dict['Orthopedics & Sports Medicine'],
                'icon': 'bi-gear-wide-connected',
                'short_description': 'Computer-assisted robotic total hip and knee arthroplasty designed for rapid mobility and joint longevity.'
            },
            {
                'title': 'Sports Medicine & Arthroscopic Surgery',
                'department': departments_dict['Orthopedics & Sports Medicine'],
                'icon': 'bi-person-arms-up',
                'short_description': 'Keyhole minimally invasive surgery for ACL tears, rotator cuff repairs, and athletic trauma recovery.'
            },
            {
                'title': '24/7 Trauma Resuscitation & ER',
                'department': departments_dict['Emergency & Trauma Care'],
                'icon': 'bi-hospital-fill',
                'short_description': 'Immediate triage, shock stabilization, advanced airway support, and acute trauma resuscitation.'
            },
            {
                'title': 'Critical Care Ambulance & Dispatch',
                'department': departments_dict['Emergency & Trauma Care'],
                'icon': 'bi-truck',
                'short_description': 'Advanced cardiac life support (ACLS) mobile units equipped with onboard telemetry and ventilator systems.'
            },
            {
                'title': 'Chemotherapy & Targeted Infusion',
                'department': departments_dict['Oncology & Infusion Center'],
                'icon': 'bi-droplet-fill',
                'short_description': 'Outpatient oncology infusion suites with personalized clinical oncology nursing and targeted biologic therapy.'
            },
            {
                'title': 'Comprehensive Cancer Screening & Biopsy',
                'department': departments_dict['Oncology & Infusion Center'],
                'icon': 'bi-search',
                'short_description': 'Early detection mammography, image-guided fine needle biopsies, and preventive oncology consultations.'
            },
        ]

        for s_info in services_data:
            srv, created = Service.objects.get_or_create(
                title=s_info['title'],
                defaults={
                    'department': s_info['department'],
                    'icon': s_info['icon'],
                    'short_description': s_info['short_description'],
                }
            )
            if created:
                self.stdout.write(f"Created Service: {srv.title}")

        # 5. Gallery Images (Professional Hospital Photography)
        from gallery.models import GalleryImage
        import urllib.request
        from PIL import Image, ImageDraw
        import io
        from django.core.files.base import ContentFile

        gallery_data = [
            {
                'title': 'Main Hospital Pavilion & Healthcare Campus',
                'file_name': 'hospital_main_campus.jpg',
                'url': 'https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Advanced Surgical Operating Theatre',
                'file_name': 'hospital_operating_theatre.jpg',
                'url': 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Modern Hospital Wing & Patient Corridors',
                'file_name': 'hospital_patient_corridor.jpg',
                'url': 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Physician & Specialist Consultation Suite',
                'file_name': 'hospital_consultation_suite.jpg',
                'url': 'https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Private Inpatient Recovery & Healing Room',
                'file_name': 'hospital_recovery_suite.jpg',
                'url': 'https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Intensive Care Unit (ICU) Monitoring Station',
                'file_name': 'hospital_icu_monitoring.jpg',
                'url': 'https://images.unsplash.com/photo-1516549655169-df83a0774514?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Biomedical & Clinical Pathology Laboratory',
                'file_name': 'hospital_diagnostic_lab.jpg',
                'url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Digital Nursing & Patient Telemetry Hub',
                'file_name': 'hospital_nursing_station.jpg',
                'url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': '24/7 Rapid Emergency & Trauma Response Bay',
                'file_name': 'hospital_emergency_bay.jpg',
                'url': 'https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Multidisciplinary Surgical Team in Operative Care',
                'file_name': 'hospital_surgical_team.jpg',
                'url': 'https://images.unsplash.com/photo-1551076805-e1869033e561?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Precision Medical Technology & Monitoring',
                'file_name': 'hospital_medical_technology.jpg',
                'url': 'https://images.unsplash.com/photo-1530497610245-94d3c16cda28?w=1200&auto=format&fit=crop&q=80'
            },
            {
                'title': 'Outpatient Medical Pavilion & Clinic Architecture',
                'file_name': 'hospital_clinic_architecture.jpg',
                'url': 'https://images.unsplash.com/photo-1512678080530-7760d81faba6?w=1200&auto=format&fit=crop&q=80'
            }
        ]

        headers = {'User-Agent': 'Mozilla/5.0'}
        for g in gallery_data:
            if not GalleryImage.objects.filter(title=g['title']).exists():
                downloaded = False
                try:
                    req = urllib.request.Request(g['url'], headers=headers)
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        content = resp.read()
                        item = GalleryImage(title=g['title'], category='Hospital')
                        item.image.save(g['file_name'], ContentFile(content), save=True)
                        downloaded = True
                        self.stdout.write(f"Downloaded Gallery Photo: {item.title}")
                except Exception:
                    pass

                if not downloaded:
                    # Offline fallback
                    img = Image.new('RGB', (800, 560), color='#0F3D69')
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([20, 20, 780, 540], outline='#0284C7', width=3)
                    draw.rectangle([40, 240, 760, 320], fill='#FFFFFF')
                    draw.text((60, 260), "HARBORLIGHT HOSPITAL", fill='#0F3D69')
                    draw.text((60, 285), g['title'], fill='#0F172A')
                    buf = io.BytesIO()
                    img.save(buf, format='JPEG', quality=90)
                    item = GalleryImage(title=g['title'], category='Hospital')
                    item.image.save(g['file_name'], ContentFile(buf.getvalue()), save=True)
                    self.stdout.write(f"Created Fallback Photo: {item.title}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with Harborlight demonstration data!'))

