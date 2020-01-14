from django.test import TestCase

# Create your tests here.
from core.models import Lesson


class LessonTests(TestCase):
    def test_read_hot_lessons(self):
        """
        load hot lesson, according to their hits
        in the ascending order
        :return:
        """
        lesson = Lesson.objects.create()