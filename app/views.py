from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count
from django.db import IntegrityError
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Answer, Tag, QuestionLike, AnswerLike, Profile
from .forms import UserRegistrationForm, UserLoginForm, UserSettingsForm, QuestionForm, AnswerForm
   

def index(request):
    page_num = int(request.GET.get('page', 1))
    
    # получаем все вопросы, отсортированные по дате, и предварительно загружаем теги
    questions = Question.objects.all().prefetch_related('tags') \
        .annotate(answer_count=Count('answers')).order_by('-created_at')
        
    # создаём пагинатор
    paginator = Paginator(questions, 5)
    page = paginator.page(page_num)
    
    # получаем 10 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:10]

    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:10]
    
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
    
    # получаем 10 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:10]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:10]

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
    
    # обработка формы
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            messages.add_message(request, messages.SUCCESS, 'Ответ успешно добавлен!', extra_tags='success')
            return redirect('question', question_id=question.id)# перенаправляем на страницу вопроса
        
        else:
            messages.add_message(request, messages.ERROR, 'Ошибка сохранения! Проверьте введенные данные!',
                                 extra_tags='danger')

    else:
        form = AnswerForm()
        
    
    # пагинация для ответов
    page_num = int(request.GET.get('page', 1))
    answers = Answer.objects.filter(question=question).order_by('-created_at')  # ответы для конкретного вопроса
    paginator = Paginator(answers, 5)
    page = paginator.page(page_num)
    
    # получаем 10 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:10]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:10]

    return render(
        request, 'question.html',
        context={
            'question': question,
            'page_obj': page,
            'answers': page.object_list,
            'tags': tags,
            'best_members': best_members,
            'form': form
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
    
    # получаем 10 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:10]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:10]
    
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
    # обработка формы
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            question.tags.set(form.cleaned_data['tags'])
            messages.add_message(request, messages.SUCCESS, 'Вопрос успешно добавлен!', extra_tags='success')
            return redirect('question', question_id=question.id)# перенаправляем на страницу вопроса
        
        else:
            messages.add_message(request, messages.ERROR, 'Ошибка сохранения! Проверьте введенные данные!',
                                 extra_tags='danger')

    else:
        form = QuestionForm()
        
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Вы должны войти, чтобы задать вопрос!',
                                 extra_tags='danger')
        return redirect('/')
    
    # получаем 10 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:10]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:10]
    return render(
        request, 'ask.html',
        context={
            'tags': tags,
            'best_members': best_members,
            'form': form
        }
    )
 
# функция для отдачи данных в Select2   
def tag_autocomplete(request):
    if 'term' in request.GET:
        qs = Tag.objects.filter(name__istartswith=request.GET.get('term'))
        tags = [{'id': tag.id, 'text': tag.name} for tag in qs]
        return JsonResponse({'results': tags})
    return JsonResponse({'results': []})
    
def login(request):
    # обработка формы
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Вы успешно вошли в систему!', extra_tags='success')
                return redirect('index')  # перенаправляем на главную страницу после входа
            else:
                messages.add_message(request, messages.ERROR, 'Неверное имя пользователя или пароль!',
                                 extra_tags='danger')
        else:
            messages.add_message(request, messages.ERROR, 'Ошибка заполнения формы! :(',
                                 extra_tags='danger')
    else:
        form = UserLoginForm()

    # получаем 10 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:10]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:10]
    
    return render(
        request, 'login.html',
        context={
            'tags': tags,
            'best_members': best_members,
            'form': form,
        }
    )
    
@login_required # только для авторизованных пользователей
def signup(request):
    # обработка формы
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = request.user # получаем текущего пользователя
                user.email = form.cleaned_data['email']
                user.username = form.cleaned_data['username']
                user.save()
                
                # Обработка загрузки аватара
                if form.cleaned_data['avatar']: # проверяем, есть ли файл
                    profile = user.profile  # получаем профиль пользователя
                    profile.avatar = form.cleaned_data['avatar']
                    profile.save()

                messages.add_message(request, messages.SUCCESS, 'Изменения успешно сохранены! :)', extra_tags='success')
                            
            except IntegrityError:
                messages.add_message(request, 
                                    messages.ERROR, 'Это имя пользователя уже занято. Пожалуйста, выберите другое. :(',
                                    extra_tags='danger')
        else:
            messages.add_message(request, 
                                messages.ERROR, 'Ошибка сохранения! проверьте заполнение формы :(',
                                extra_tags='danger')
    else:
        initial_data = {
            'email': request.user.email,
            'username': request.user.username,
        }
        form = UserSettingsForm(initial=initial_data)
    
    # получаем 10 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:10]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:10]
    return render(
        request, 'signup.html',
        context={
            'tags': tags,
            'best_members': best_members,
            'form': form
        }
    )

def register(request):   
    # отправка формы
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)  
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # после создания пользователя происходит вход
            messages.add_message(request, messages.SUCCESS, 'Регистрация прошла успешно :)', extra_tags='success')
            return redirect('index')  # если регистрация прошла успешно переходим на главную страницу
        else:
            messages.add_message(request, messages.ERROR, 'Ошибка регистрации! проверьте заполнение формы :(',
                                 extra_tags='danger')
    else:
        form = UserRegistrationForm() # создаем форму для GET-запроса
        
    # получаем 15 самых популярных тегов по количеству связанных с ними вопросов
    tags = Tag.objects.annotate(question_count=Count('questions')).order_by('-question_count')[:15]
    
    # берем лучших пользователей
    best_members = Profile.objects.order_by('-rating')[:10]
    return render(
        request, 'register.html',
        context={
            'tags': tags,
            'best_members': best_members,
            'form': form
        }
    )

def logout(request):
    auth_logout(request)
    next_url = request.GET.get('next', '/')  
    if next_url and reverse('signup') in next_url:
      return redirect('/')
    return redirect(next_url)

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

@login_required
def like_question(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)
        user = request.user
        if QuestionLike.objects.filter(user=user, question=question).exists():
            question.unlike(user)
            liked = False
        else:
            question.like(user)
            liked = True

        likes = question.likes.count()
        return JsonResponse({'likes': likes, 'liked': liked})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def get_like_status(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    user = request.user
    liked =  QuestionLike.objects.filter(user=user, question=question).exists()
    return JsonResponse({'liked': liked})


@login_required
def like_answer(request, answer_id):
    if request.method == 'POST':
        answer = get_object_or_404(Answer, id=answer_id)
        user = request.user
        if AnswerLike.objects.filter(user=user, answer=answer).exists():
             answer.unlike(user)
             liked = False
        else:
            answer.like(user)
            liked = True

        likes = answer.likes.count()
        return JsonResponse({'likes': likes, 'liked': liked})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def get_answer_like_status(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user
    liked = AnswerLike.objects.filter(user=user, answer=answer).exists()
    return JsonResponse({'liked': liked})
    question = get_object_or_404(Question, id=question_id)
    user = request.user
    liked =  QuestionLike.objects.filter(user=user, question=question).exists()
    return JsonResponse({'liked': liked})

# @login_required
# def set_correct_answer(request, question_id):
    if request.method == 'POST':
       try:
            question = get_object_or_404(Question, id=question_id)
            if request.user != question.author:
                return JsonResponse({'status': 'error', 'message': 'Только автор может выбирать правильный ответ.'}, status=403)

            data = json.loads(request.body)
            answer_id = data.get('answer_id')
            is_correct = data.get('is_correct')

            answer = get_object_or_404(Answer, id=answer_id)
            if answer.question != question:
                 return JsonResponse({'status': 'error', 'message': 'Этот ответ не относится к этому вопросу.'}, status=400)

            answer.is_correct = is_correct
            answer.save()

            return JsonResponse({'status': 'success', 'message': 'Правильный ответ обновлен.'})

       except Exception as e:
          return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)