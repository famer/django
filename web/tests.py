from django.db.models import Max
from django.test import Client, TestCase
from .models import Job, Tag, City

# Create your tests here.
class JobTestCase(TestCase):

    def setUp(self):

        # Create cities
        remote = City.objects.create(title="Удаленка")
        nn = City.objects.create(title="Нижний Новгород")
        moscow = City.objects.create(title="Москва")
        spb = City.objects.create(title="Санкт-Петербург")

        # Create tags
        express_tag = Tag.objects.create(title="Express.js")
        node_tag = Tag.objects.create(title="Node.js")
        
        swift_tag = Tag.objects.create(title="Swift")

        python_tag = Tag.objects.create(title="Python")
        django_tag = Tag.objects.create(title="Django")
        
        # Create jobs
        # Valid job
        nodejs_job = Job.objects.create(title="Node.js developer",\
                        company="OOO LTD",\
                        description="Develop some greate Node.js application",\
                        city=spb, contacts="Email: dj.famer@gmail.com, tg: famer",\
                        net_salary_from=50000,\
                        net_salary_to=12000,\
                        moderated=True)
                        
        nodejs_job.tags.add(express_tag)
        nodejs_job.tags.add(node_tag)

        # Invalid job, no description
        swift_job = Job.objects.create(title="Swift developer",\
                    city=moscow,\
                    contacts="Email: dj.famer@gmail.com, tg: famer",\
                    net_salary_from=70000,\
                    net_salary_to=140000,\
                    moderated=True)

        swift_job.tags.add(swift_tag)

        # Not moderated
        django_job = Job.objects.create(title="Django developer",\
                    company="OOO LTD",\
                    description="Develop some greate django application",\
                    city=nn,\
                    contacts="Email: dj.famer@gmail.com, tg: famer",\
                    net_salary_from=60000, net_salary_to=120000)

        django_job.tags.add(python_tag)
        django_job.tags.add(django_tag)

    def test_tag_jobs_count(self):
        express = Tag.objects.get(title="Express.js")
        self.assertEqual(express.jobs.count(), 1)

    def test_city_jobs_count(self):
        nn = City.objects.get(title="Нижний Новгород")
        self.assertEqual(nn.jobs.count(), 1)

    def test_is_valid_job(self):
        nn = City.objects.get(title="Нижний Новгород")
        j = Job.objects.get(title="Django developer",\
                    company="OOO LTD",\
                    description="Develop some greate django application",\
                    city=nn, contacts="Email: dj.famer@gmail.com, tg: famer",\
                    net_salary_from=60000, net_salary_to=120000)
        self.assertTrue(j.is_valid_job())

    def test_is_invalid_salary(self):
        spb = City.objects.get(title="Санкт-Петербург")
        j = Job.objects.get(title="Node.js developer",\
                    company="OOO LTD",\
                    description="Develop some greate Node.js application",\
                    city=spb,\
                    contacts="Email: dj.famer@gmail.com, tg: famer",\
                    net_salary_from=50000, net_salary_to=12000)
        self.assertFalse(j.is_valid_job())

    def test_is_invalid_description(self):
        moscow = City.objects.get(title="Москва")
        j = Job.objects.get(title="Swift developer",\
                    city=moscow,\
                    contacts="Email: dj.famer@gmail.com, tg: famer",\
                    net_salary_from=70000, net_salary_to=140000)
        self.assertFalse(j.is_valid_job())

    def test_index(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['jobs'].count(), 2)

    def test_search(self):
        c = Client()
        response = c.get('/jobs/?q=node')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['jobs'].count(), 1)

    def test_search_onmoderated(self):
        c = Client()
        response = c.get('/jobs/?q=django')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['jobs'].count(), 0)

    def test_valid_job_page(self):
        city = City.objects.get(title="Санкт-Петербург")
        j = Job.objects.get(title="Node.js developer", company="OOO LTD", description="Develop some greate Node.js application", city=city, contacts="Email: dj.famer@gmail.com, tg: famer", net_salary_from=50000, net_salary_to=12000, moderated=True)

        c = Client()
        response = c.get(f"/jobs/{j.id}")
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_job_page(self):
        max_id = Job.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/jobs/{max_id + 1}")
        self.assertEqual(response.status_code, 404)