from django.core.management.base import BaseCommand
from departments.models import Department, Service
from doctors.models import Doctor
from core.models import Testimonial

class Command(BaseCommand):
    help = 'Seeds initial demonstration data for City Heart Hospital'

    def handle(self, *args, **options):
        self.stdout.write('Seeding initial cardiac specialty data for City Heart Hospital...')

        # Clean existing non-cardiac or demo data cleanly
        Service.objects.all().delete()
        Doctor.objects.all().delete()
        Department.objects.all().delete()
        Testimonial.objects.all().delete()

        # 1. Departments (6 Dedicated Cardiac Divisions)
        depts_data = [
            {
                'name': 'Interventional Cardiology & Cath Lab',
                'icon': 'bi-heart-pulse-fill',
                'short_description': 'Advanced coronary angiograms, primary angioplasty (PAMI), complex stenting, and structural heart catheterization.',
                'full_description': 'Our state-of-the-art hybrid catheterization laboratories operate 24/7 with zero-delay STEMI activation. Specialists perform complex coronary interventions, intravascular ultrasound (IVUS), optical coherence tomography (OCT), fractional flow reserve (FFR), and chronic total occlusion (CTO) revascularization with radial artery access.'
            },
            {
                'name': 'Cardiothoracic & Vascular Surgery (CTVS)',
                'icon': 'bi-shield-plus',
                'short_description': 'Minimally invasive cardiac surgery (MICS), coronary artery bypass grafting (CABG), valve repair, and aortic aneurysm surgery.',
                'full_description': 'Equipped with ultra-clean laminar flow cardiac operating suites, our CTVS surgical faculty delivers world-class outcomes in beating-heart bypass surgeries, complex multivalve replacements, aortic root repairs, and heart-lung machine perfusion protocols.'
            },
            {
                'name': 'Cardiac Electrophysiology & Arrhythmia Center',
                'icon': 'bi-activity',
                'short_description': 'Advanced 3D cardiac mapping, radiofrequency & cryoballoon catheter ablation, pacemaker & ICD implantation.',
                'full_description': 'Dedicated to diagnosing and correcting complex heart rhythm disorders, atrial fibrillation (AFib), ventricular tachycardia, and heart block. We utilize high-density 3D mapping systems and implant leadless pacemakers, biventricular devices (CRT-D), and subcutaneous ICDs.'
            },
            {
                'name': 'Pediatric & Congenital Heart Center',
                'icon': 'bi-emoji-smile-fill',
                'short_description': 'Compassionate cardiac care for neonates, infants, and children with congenital heart defects and structural anomalies.',
                'full_description': 'Specialized pediatric cardiology unit providing neonate-to-adolescent structural heart interventions, pediatric echocardiography, ASD/VSD device closures, and congenital defect corrective surgeries backed by a dedicated Pediatric Cardiac ICU.'
            },
            {
                'name': 'Non-Invasive Cardiology & Advanced Diagnostics',
                'icon': 'bi-clipboard2-pulse-fill',
                'short_description': '3D Echocardiography, transesophageal echo (TEE), cardiac CT angiography, stress testing (TMT), and 24/7 Holter monitoring.',
                'full_description': 'High-precision cardiac imaging and physiological diagnostics identifying coronary artery calcification, myocardial ischemia, valvular hemodynamics, and heart failure markers with minimal patient discomfort and zero radiation options.'
            },
            {
                'name': '24/7 Chest Pain & Acute STEMI Emergency Center',
                'icon': 'bi-hospital-fill',
                'short_description': 'Immediate emergency triage, rapid door-to-balloon angioplasty protocol (< 45 mins), and dedicated Mobile Cardiac ICU ambulances.',
                'full_description': 'Round-the-clock emergency facility designed for rapid resuscitation of acute myocardial infarction, unstable angina, cardiogenic shock, and life-threatening arrhythmias, staffed by on-site cardiac intensivists and interventional cardiologists.'
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
            self.stdout.write(f"Created Cardiac Department: {dept.name}")

        # 2. Doctors (6 Cardiac Specialists)
        doctors_data = [
            {
                'name': 'Elena Rostova',
                'department': departments_dict['Interventional Cardiology & Cath Lab'],
                'specialization': 'Chief Interventional Cardiologist',
                'qualification': 'MD, DM (Cardiology), FACC, FSCAI',
                'experience_years': 18,
                'bio': 'Pioneering interventional cardiologist with over 4,500 successful coronary angioplasties and transcatheter aortic valve replacements (TAVR). Nationally recognized for complex radial stenting and acute STEMI interventions.',
                'available_days': 'Mon - Fri',
                'is_active': True,
            },
            {
                'name': 'Marcus Vance',
                'department': departments_dict['Cardiothoracic & Vascular Surgery (CTVS)'],
                'specialization': 'Chief Cardiothoracic Surgeon',
                'qualification': 'MD, MCh (CTVS), FACS, FETCS',
                'experience_years': 22,
                'bio': 'Internationally acclaimed cardiac surgeon specializing in minimally invasive beating-heart coronary bypass (CABG), aortic aneurysm repair, and mitral valve reconstruction with exceptional clinical safety records.',
                'available_days': 'Mon, Wed, Fri',
                'is_active': True,
            },
            {
                'name': 'David Thorne',
                'department': departments_dict['Cardiac Electrophysiology & Arrhythmia Center'],
                'specialization': 'Senior Cardiac Electrophysiologist',
                'qualification': 'MD, DM (Cardio), FHRS, CEPS',
                'experience_years': 16,
                'bio': 'Leading expert in complex cardiac electrophysiology, 3D anatomical mapping, radiofrequency catheter ablation for AFib, and implantation of biventricular CRT-D and leadless pacemakers.',
                'available_days': 'Tue, Thu, Sat',
                'is_active': True,
            },
            {
                'name': 'Sarah Jenkins',
                'department': departments_dict['Pediatric & Congenital Heart Center'],
                'specialization': 'Director of Pediatric Cardiology',
                'qualification': 'MD, FAAP, FACC',
                'experience_years': 15,
                'bio': 'Specializing in neonatal and pediatric congenital heart disease, fetal echocardiography, and percutaneous transcatheter device closure of atrial and ventricular septal defects.',
                'available_days': 'Mon - Thu',
                'is_active': True,
            },
            {
                'name': 'Amina Al-Mansoor',
                'department': departments_dict['24/7 Chest Pain & Acute STEMI Emergency Center'],
                'specialization': 'Director of Cardiac Critical Care & STEMI Unit',
                'qualification': 'MD, FCCP, FESC',
                'experience_years': 17,
                'bio': 'Pioneered our rapid < 45 minute door-to-balloon primary angioplasty protocol. Specialist in acute coronary syndromes, cardiogenic shock management, ECMO, and cardiac ICU resuscitation.',
                'available_days': '24/7 Roster',
                'is_active': True,
            },
            {
                'name': 'Jonathan Ross',
                'department': departments_dict['Non-Invasive Cardiology & Advanced Diagnostics'],
                'specialization': 'Consultant Non-Invasive Cardiologist & Imaging Specialist',
                'qualification': 'MD, FASE, FSCMR',
                'experience_years': 14,
                'bio': 'Expert in advanced transesophageal echocardiography (TEE), 3D myocardial strain imaging, contrast cardiac MRI, and preventative cardiovascular risk stratification.',
                'available_days': 'Mon - Fri',
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
            self.stdout.write(f"Created Cardiologist: Dr. {doc.name}")

        # 3. Testimonials (Heart Patient Recovery Stories)
        testimonials_data = [
            {
                'patient_name': 'Eleanor Vance',
                'message': 'When I suffered sudden chest pressure at home, City Heart Hospital’s STEMI emergency team and Dr. Elena Rostova had me in the Cath Lab within 35 minutes. Their rapid angioplasty saved my heart muscle and my life.',
                'rating': 5,
                'is_approved': True,
            },
            {
                'patient_name': 'Robert Martinez',
                'message': 'Undergoing beating-heart bypass surgery was terrifying, but Dr. Marcus Vance and the CTVS surgical team gave me complete confidence. Today my heart is pumping stronger than it has in ten years.',
                'rating': 5,
                'is_approved': True,
            },
            {
                'patient_name': 'Sophie Lin & Family',
                'message': 'Dr. Sarah Jenkins and the pediatric cardiac team diagnosed and repaired our infant son’s ASD defect with such incredible kindness and precision. We will forever be grateful to City Heart Hospital.',
                'rating': 5,
                'is_approved': True,
            },
            {
                'patient_name': 'Thomas Sterling',
                'message': 'After years of frightening AFib episodes and palpitations, Dr. David Thorne performed a 3D catheter ablation. I am completely symptom-free and off medication. World-class heart care right here in Riverdale.',
                'rating': 5,
                'is_approved': True,
            },
        ]

        for t in testimonials_data:
            Testimonial.objects.create(
                patient_name=t['patient_name'],
                message=t['message'],
                rating=t['rating'],
                is_approved=t['is_approved']
            )
        self.stdout.write('Created Heart Recovery Testimonials.')

        # 4. Services (10 Dedicated Cardiac Services)
        services_data = [
            {
                'title': 'Primary Angioplasty (PAMI) & Stenting',
                'department': departments_dict['Interventional Cardiology & Cath Lab'],
                'icon': 'bi-heart-pulse-fill',
                'short_description': 'Immediate catheterization and drug-eluting stent implantation for acute myocardial infarction with rapid door-to-balloon protocol.'
            },
            {
                'title': 'Transcatheter Aortic Valve Replacement (TAVR / TAVI)',
                'department': departments_dict['Interventional Cardiology & Cath Lab'],
                'icon': 'bi-shield-check',
                'short_description': 'Minimally invasive percutaneous valve replacement for severe aortic stenosis without opening the chest.'
            },
            {
                'title': 'Minimally Invasive CABG (Beating-Heart Bypass)',
                'department': departments_dict['Cardiothoracic & Vascular Surgery (CTVS)'],
                'icon': 'bi-shield-plus',
                'short_description': 'Off-pump coronary artery bypass surgery performed through small incisions, promoting faster recovery and less blood loss.'
            },
            {
                'title': 'Heart Valve Repair & Aortic Reconstruction',
                'department': departments_dict['Cardiothoracic & Vascular Surgery (CTVS)'],
                'icon': 'bi-gear-wide-connected',
                'short_description': 'Specialized surgical repair and biological valve replacements for mitral, aortic, and tricuspid valve diseases.'
            },
            {
                'title': '3D Cardiac Mapping & Arrhythmia Catheter Ablation',
                'department': departments_dict['Cardiac Electrophysiology & Arrhythmia Center'],
                'icon': 'bi-activity',
                'short_description': 'Precision radiofrequency and cryoablation targeting atrial fibrillation, flutter, and ventricular tachycardias.'
            },
            {
                'title': 'Pacemaker, ICD & CRT-D Implantation',
                'department': departments_dict['Cardiac Electrophysiology & Arrhythmia Center'],
                'icon': 'bi-cpu-fill',
                'short_description': 'Implantation of modern leadless pacemakers and automated cardiac defibrillators for arrhythmia control and heart failure.'
            },
            {
                'title': 'Pediatric Interventional Defect Closure (ASD/VSD/PDA)',
                'department': departments_dict['Pediatric & Congenital Heart Center'],
                'icon': 'bi-emoji-smile-fill',
                'short_description': 'Non-surgical device closures for congenital structural heart defects in children and young adults.'
            },
            {
                'title': '3D Echocardiography & Transesophageal Echo (TEE)',
                'department': departments_dict['Non-Invasive Cardiology & Advanced Diagnostics'],
                'icon': 'bi-clipboard2-pulse-fill',
                'short_description': 'High-resolution ultrasound imaging of heart chambers, valves, and hemodynamics for precise cardiac evaluation.'
            },
            {
                'title': '24/7 Chest Pain Triage & Rapid STEMI Protocol',
                'department': departments_dict['24/7 Chest Pain & Acute STEMI Emergency Center'],
                'icon': 'bi-hospital-fill',
                'short_description': 'Zero-delay cardiac emergency assessment, point-of-care Troponin-I biomarkers, and immediate Cath Lab transfer.'
            },
            {
                'title': 'Mobile Cardiac ICU Ambulance & Telemetry Dispatch',
                'department': departments_dict['24/7 Chest Pain & Acute STEMI Emergency Center'],
                'icon': 'bi-truck',
                'short_description': 'Advanced life support ambulances equipped with 12-lead digital ECG transmission, defibrillators, and ventilator support.'
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
            self.stdout.write(f"Created Cardiac Service: {srv.title}")

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
                    draw.text((60, 260), "CITY HEART HOSPITAL", fill='#0F3D69')
                    draw.text((60, 285), g['title'], fill='#0F172A')
                    buf = io.BytesIO()
                    img.save(buf, format='JPEG', quality=90)
                    item = GalleryImage(title=g['title'], category='Hospital')
                    item.image.save(g['file_name'], ContentFile(buf.getvalue()), save=True)
                    self.stdout.write(f"Created Fallback Photo: {item.title}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with City Heart Hospital specialized cardiac data!'))

