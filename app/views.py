from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Question, Answer, Tag, QuestionLike, AnswerLike, Profile
import copy
   

def index(request):
    page_num = int(request.GET.get('page', 1))
    
    # получаем все вопросы, отсортированные по дате, и предварительно загружаем теги
    questions = Question.objects.all().prefetch_related('tags') \
        .annotate(answer_count=Count('answers'))  
    
    # создаём пагинатор
    paginator = Paginator(questions, 5)
    page = paginator.page(page_num)
    
    # получаем 15 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:15]

    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:5]
    
    return render(
        request, 'index.html',
        context={
            'questions': page.object_list,
            'page_obj': page,
            'tags': tags,
            'best_members': best_members
        }
    )

def hot(request):
    page_num = int(request.GET.get('page', 1))
    
    # используем метод get_best_questions для получения вопросов, отсортированных по лайкам
    hot_questions = Question.objects.get_best_questions() \
        .annotate(answer_count=Count('answers'))  
    
    # пагинация
    paginator = Paginator(hot_questions, 5)
    page = paginator.page(page_num)
    
    # получаем 15 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:15]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:5]

    return render(
        request, 'hot.html',
        context={
            'questions': page.object_list,
            'page_obj': page,
            'tags': tags,
            'best_members': best_members
        }
    )

def question(request, question_id):
    question = get_object_or_404(Question.objects.annotate(answer_count=Count('answers')), id=question_id)
    
    # пагинация для ответов
    page_num = int(request.GET.get('page', 1))
    answers = Answer.objects.filter(question=question).order_by('-created_at')  # ответы для конкретного вопроса
    paginator = Paginator(answers, 5)
    page = paginator.page(page_num)
    
    # получаем 15 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:15]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:5]

    return render(
        request, 'question.html',
        context={
            'question': question,
            'page_obj': page,
            'answers': page.object_list,
            'tags': tags,
            'best_members': best_members
        }
    )

def tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    
    # все вопросы с этим тегом
    questions = Question.objects.filter(tags=tag)\
        .annotate(answer_count=Count('answers'))  
    
    # пагинация
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(questions, 5)
    page = paginator.page(page_num)
    
    # получаем 15 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:15]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:5]
    
    return render(
        request, 'tag.html',
        context={
            'questions': page.object_list,
            'page_obj': page,
            'tag': tag,
            'tags': tags,
            'best_members': best_members
        }
    )

def ask(request):
    # получаем 15 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:15]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:5]
    return render(
        request, 'ask.html',
        context={
            'tags': tags,
            'best_members': best_members
        }
    )

def login(request):
    # получаем 15 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:15]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:5]
    return render(
        request, 'login.html',
        context={
            'tags': tags,
            'best_members': best_members
        }
    )

def signup(request):
    # получаем 15 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:15]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:5]
    return render(
        request, 'signup.html',
        context={
            'tags': tags,
            'best_members': best_members
        }
    )

def register(request):
    # получаем 15 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:15]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:5]
    return render(
        request, 'register.html',
        context={
            'tags': tags,
            'best_members': best_members
        }
    )

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)