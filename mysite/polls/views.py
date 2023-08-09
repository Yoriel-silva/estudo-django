from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import question
# Create your views here.

def index(request):
    latest_question_list = question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def results(request, question_id):
    questions = question(pk=question_id) 
    return render(request, 'polls/results.html', {'questions': questions})

def vote (request, question_id):
    questions = get_object_or_404(question, pk=question_id)
    try:
        selected_choice = questions.choice_set.get(pk=request.POST['choice'])
    except KeyError:
        return render(request, 'polls/vote.html', {
            'question': questions,
            'error_message': 'you didn`t select a choice.',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))