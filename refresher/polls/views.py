from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Count

from .models import Choice, Question

# Create your views here.

class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    '''Return the last 5 published questions (excluding those yet to be published) only if they have choices.'''

    # return [question for question in Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5] if question.choice_set.all().count() > 0]
    # The above works because generic.ListView can work with lists (even though it usually works with a QuerySet object). However, it doesn't work in
    # generic.DetailView because DetailView expects a QS object. This makes me think that the 'correct' way to do it is the same way on both,
    # which is the qs.annotate() way, and not the list comprehension way I've done it now.

    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date').annotate(choice_count=Count('choice')).filter(choice_count__gt=0)[:5]


class DetailView(generic.DetailView):
  model = Question
  template_name = 'polls/detail.html'

  def get_queryset(self):
    # Using annotate() to return a QuerySet only containing Questions that have Choices

    # annotate() vs aggregate() - use annotate() when you want to perform computations on each
    # object in a QuerySet, use aggregate() when you want to perform computations on all objects in a QS put together.

    # https://stackoverflow.com/questions/22191879/how-do-i-peroform-django-model-validation-to-exclude
    # https://docs.djangoproject.com/en/4.0/topics/db/aggregation/

    return Question.objects.filter(pub_date__lte=timezone.now()).annotate(choice_count=Count('choice')).filter(choice_count__gt=0)


class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.html' 


def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {'question': question, 'error_message': 'You didn\'t select a choice.'})
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))