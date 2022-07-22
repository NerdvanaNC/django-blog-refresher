import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

  def test_was_published_recently_with_future_question(self):
    '''was_published_recently() should return False for questions
    published with a future date'''
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date = time)
    self.assertIs(future_question.was_published_recently(), False)

  def test_was_published_recently_with_recent_question(self):
    '''was_published_recently() should return True for questions
    published a day before'''
    recently = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=recently)
    self.assertIs(recent_question.was_published_recently(), True)

  def test_was_published_recently_with_old_question(self):
    '''was_published_recently() should return False for questions
    published more than a day in the past'''
    two_days_ago = timezone.now() - datetime.timedelta(days=2)
    old_question = Question(pub_date=two_days_ago)
    self.assertIs(old_question.was_published_recently(), False)