from django.shortcuts import render
from django.http import Http404,HttpResponse
from django.contrib.auth.decorators import login_required
from . models import *

@login_required(login_url='/login/')
def poll_list(request):
    context              = { }
    questions            = Question.objects.all()
    context['title']     = 'polls'
    context['questions'] = questions
    template_name        = 'polls/poll_list.html'
    return render(request,template_name,context)

@login_required(login_url='/login/')
def poll_details(request, id=None):
    context = {}
    try:
        question = Question.objects.get(id=id)
    except:
        raise Http404

    context['question'] = question
    template_name       = 'polls/poll_details.html'
    return render(request,template_name,context)
    
@login_required(login_url='/login/')
def single_poll(request,id=None):
    context = { }
    if request.method == 'GET':
        try:
            question = Question.objects.get(id=id)
        except:
            raise Http404
        context['question'] = question
        template_name       = 'polls/single_poll.html'
        return render(request,template_name,context)
    if request.method == 'POST':
        user_id = 1
        data = request.POST
        save_choice = Answer.objects.create(user_id=user_id, choice_id=data['choice'])
        if save_choice:
            return HttpResponse("Your choice is selected.")
        else:
            return HttpResponse("Your choice is not select. ")