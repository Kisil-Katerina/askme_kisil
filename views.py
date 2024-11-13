from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import copy
   
QUESTIONS = [
  {
    'title': f'Title {i}',
    'id': i,
    'text': f'This is text for question № {i}! This is text for question № {i}! This is text for question № {i}!This is text for question № {i}!'
  } for i in range(80)
]

ANSWERS = [
  {
    'id': i,
    'text': f'This is text for answer № {i}! This is text for answer № {i}! This is text for answer № {i}! This is text for answer № {i}!'
  } for i in range(40)
]

TAGS = [
  {
    'id': i,
    'text': f'tag {i}'
  } for i in range(9)
]


def index(request):
  page_num = int(request.GET.get('page', 1))
  paginator = Paginator(QUESTIONS, 20)
  page = paginator.page(page_num)

  return render(
      request, 'index.html', 
       context={
        'questions': page.object_list,
        'page_obj': page,
        'tags': TAGS }  
  )

def hot(request):
  hot_questions = copy.deepcopy(QUESTIONS)
  hot_questions.reverse()

  page_num = int(request.GET.get('page', 1))
  paginator = Paginator(hot_questions, 20)
  page = paginator.page(page_num)

  return render(
      request, 'hot.html', 
      context={
        'questions': page.object_list,
        'page_obj': page,
        'tags': TAGS }
  )    

def question(request, question_id):
  question = QUESTIONS[question_id]

  page_num = int(request.GET.get('page', 1))
  paginator = Paginator(ANSWERS, 20)
  page = paginator.page(page_num)

  return render(
    request, 'question.html',
    context={
        'questions': question,
        'page_obj': page,
        'answers': page.object_list,  
        'tags': TAGS } 
  )

def ask(request):
  return render(
    request, 'ask.html',
    context={ 
        'tags': TAGS } 
  )

def login(request):
  return render(
    request, 'login.html',
    context={ 
        'tags': TAGS } 
  )

def signup(request):
  return render(
    request, 'signup.html',
    context={ 
        'tags': TAGS } 
  )

def register(request):
  return render(
    request, 'register.html',
    context={ 
        'tags': TAGS } 
  )

def tag(request, tag_id):
  tag = TAGS[tag_id]
  return render(
    request, 'tag.html',
    context={
        'questions': QUESTIONS,
        'tag': tag,
        'tags': TAGS } 
  )

