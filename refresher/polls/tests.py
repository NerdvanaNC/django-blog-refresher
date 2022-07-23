import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


def create_question(question_text, num_days):
  '''Shortcut function to quickly create dummy questions for tests.
  question_text is the title of the question, and num_days is an int value for how
  many days in the past/future the question's pub_date is. Use negative values for past dates.'''
  time = timezone.now() + datetime.timedelta(days=num_days)
  return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):

  def test_no_questions(self):
    '''In the case of no questions, an appropriate message is displayed.'''
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    # The error message might be any string, but will definitely say "no polls"
    self.assertContains(response, 'No polls')
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_past_questions(self):
    '''Only questions already published exist, so should be shown.'''
    question = create_question('Past Question', -3)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_question_list'], [question])

  def test_future_questions(self):
    '''Only questions with a future pub_date exist, and should not be shown.'''
    question = create_question('Future Question', 7)
    response = self.client.get(reverse('polls:index'))
    self.assertContains(response, 'No polls')
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_past_and_future_questions(self):
    '''A mixed set of questions already published and with their pub_date in the future exist.
    Only the ones with their pub_date in the past should be shown.'''
    past_question = create_question('Past Question', -3)
    future_question = create_question('Future Question', 3)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

  def test_two_past_questions(self):
    '''Multiple questions with their pub_date in the past exist, they should all be shown.'''
    past_question_1 = create_question('Past Question 1', -10)
    past_question_2 = create_question('Past Question 2', -7)
    response = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(response.context['latest_question_list'], [past_question_2, past_question_1]) # the order of questions is important