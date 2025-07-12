from django.test import TestCase
from .models import Teacher

# Create your tests here.

class TeacherModelTest(TestCase):
    def test_str(self):
        teacher = Teacher(name='Test', subject='Math')
        self.assertEqual(str(teacher), 'Test')
