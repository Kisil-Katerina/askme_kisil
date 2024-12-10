from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from django.contrib.auth.models import User
from faker import Faker
import random
from django.db import transaction
from django.db import IntegrityError

fake = Faker('ru_RU')

# значения для генерации данных
NUM_USERS = 100
NUM_QUESTIONS = 100
NUM_ANSWERS = 1000
NUM_TAGS = 1000
NUM_LIKES = 2000


books     = ['Трудно быть Богом', 'Мастер и Маргарита', 'Мы', 'Война и мир', 'Преступление и наказание',
            'Улитка на склоне', 'Пикник на обочине', 'Поэма без героя', 'Овод', 'Солярис', 'Идиот',
            'Воскресение', 'Соло на ундервуде', 'Доктор Живаго', 'Поэма конца', 'Поверх барьеров', 
            'Сестра моя жизнь', 'Территория', 'Кысь', 'Мой Пушкин', 'Властелин колец', 'Сто лет одиночества', 
            'Убить пересмешника', 'Гордость и предубеждение', 'Мастер и Маргарита', 'Время жить и время умирать']

genres = ["фэнтези", "фантастика", "детектив", "роман", "мистика", "психология", "символизм",
            "научная фантастика", "научная литература", "биография", "ужасы", "триллер", "реализм",
            "исторический роман", "приключения", "поэзия", "сказка", "классицизм", "драма", "романтизм",
            "современная литература", "мемуары", "пьеса", "юмор", "постмодернизм", "проза", "абсурд"
             ]
                
authors =  ['Лев Толстой', 'Федор Достоевский', 'Михаил Булгаков', 'Айзек Азимов', 'Борис Пастернак',
            'Марина Цветаева', 'Анна Ахматова', 'Осип Мандельштам', 'Юнна Мориц', 'Мария Петровых',
            'Рената Муха', 'Аркадий и Борим Стругацкие', 'А. С. Пушкин', 'Сергей Довлатов', 'М. Ю. Лермонтов',
            'Михаил Пришвин', 'Олег Куваев', 'Даниил Хармс', 'Борис Чичибабин', 'Юрий Домбровский']

class Command(BaseCommand):

    def create_users(self):
        self.stdout.write("Создание пользователей...")

        users = []
        for _ in range(NUM_USERS):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            user = User(username=username, email=email)
            user.set_password(password)
            users.append(user)

        try:
            # используем atomic для обеспечения целостности транзакции
            with transaction.atomic():
                User.objects.bulk_create(users)
        except IntegrityError:
            self.stdout.write(self.style.WARNING('Ошибка уникальности при добавлении пользователей'))

        self.stdout.write(self.style.SUCCESS('Пользователи созданы'))

    def create_profiles(self):
        self.stdout.write("Создание профилей...")

        profiles = []
        for user in User.objects.all():
            profile = Profile(user=user, avatar=fake.image_url(), rating=0)
            profiles.append(profile)

        try:
            # используем atomic для создания профилей в отдельной транзакции
            with transaction.atomic():
                Profile.objects.bulk_create(profiles)
        except IntegrityError:
            self.stdout.write(self.style.WARNING('Ошибка уникальности при добавлении профилей'))

        self.stdout.write(self.style.SUCCESS('Профили созданы'))

    def create_tags(self):
        self.stdout.write("Создание тегов...")

        tags = set(genres)  # Начнём с фиксированных жанров
    
        for _ in range(NUM_TAGS - len(tags)):
            # Составляем случайные теги с использованием словарных шаблонов
            tag_new = fake.word()
            tag_old = random.choice(list(tags))
        
            # Составляем новый тег, состоящий из двух слов (максимум)
            tag = f"{tag_old} {tag_new}".strip()
        
            # Разделяем тег на слова и проверяем количество слов
            tag_words = tag.split()
        
            # Если тег состоит из более чем 2 слов, генерируем новый тег
            if len(tag_words) > 2:
                continue  # Пропускаем этот тег, если он состоит из более чем 2 слов

            # Проверка длины тега перед добавлением
            if len(tag) <= 100:
                tags.add(tag)  # Гарантируем уникальность с использованием set
            else:
                # Если длина превышает 100 символов, пропускаем этот тег
                continue

        tag_objects = [Tag(name=tag_name) for tag_name in tags]

        try:
            with transaction.atomic():
                Tag.objects.bulk_create(tag_objects)
        except IntegrityError:
            self.stdout.write(self.style.WARNING('Ошибка уникальности при добавлении тегов'))

        self.stdout.write(self.style.SUCCESS('Теги созданы'))

    def create_questions(self):
        self.stdout.write("Создание вопросов...")

        question_templates = [
            "Какую книгу из жанра {genre} вы бы порекомендовали?",
            "Какой персонаж из книги {book} вам больше всего нравится и почему?",
            "Что вам больше всего понравилось в книге {book}?",
            "Недавно прочел книгу {book}, что вы о ней думаете?",
            "Какая книга в жанре {genre} ваша любимая?",
            "Какие книги в жанре {genre} вам нравятся больше всего?",
            "Решил почитать книги в жанре {genre}, посоветуйте, с чего начать?",
            "Что вы думаете о стиле {author}?",
            "Какая книга {author} ваша любимая?",
            "Очень люблю книги {author}, а вы?"
        ]

        questions = []
        tags = list(Tag.objects.all())  # получаем все теги
        tags_count = len(tags)  # определяем количество тегов

        for _ in range(NUM_QUESTIONS):
            # случайным образом выбираем жанр, книгу и автора
            genre = random.choice(genres)
            book = random.choice(books)
            author = random.choice(authors)

            # выбираем случайный шаблон вопроса
            template = random.choice(question_templates)

            # заменяем пропуски на реальные данные
            if '{genre}' in template:
                template = template.format(genre=genre)
            elif '{book}' in template:
                template = template.format(book=book)
            elif '{author}' in template:
               template = template.format(author=author)

            # случайный автор вопроса
            author_user = random.choice(User.objects.all())

            # выбираем случайное количество тегов от 1 до 13
            num_tags = random.randint(1, 13)

            # выбираем случайные теги для вопроса
            selected_tags = random.sample(tags, min(tags_count, num_tags))

            # создаем вопрос
            content = fake.text(max_nb_chars=500)
            question = Question(title=template, content=content, author=author_user)
            questions.append(question)  # добавляем вопрос в список

            # сохраняем вопрос в базе данных, чтобы он получил id
            question.save()
        
            # присваиваем теги каждому вопросу сразу после его создания
            question.tags.set(selected_tags)
            
        self.stdout.write(self.style.SUCCESS('Вопросы созданы'))

    def create_answers(self):
        self.stdout.write("Создание ответов...")

        answers = []
        for _ in range(NUM_ANSWERS):
            content = fake.text(max_nb_chars=500)
            author = random.choice(User.objects.all())
            question = random.choice(Question.objects.all())
            is_correct = random.choice([True, False]) 
            answer = Answer(content=content, author=author, question=question, is_correct=is_correct)
            answers.append(answer)

        try:
            with transaction.atomic():
                Answer.objects.bulk_create(answers)
        except IntegrityError:
            self.stdout.write(self.style.WARNING('Ошибка при добавлении ответов'))

        self.stdout.write(self.style.SUCCESS('Ответы созданы'))

    def create_likes(self):
        self.stdout.write("Создание лайков...")

        try:
            for _ in range(NUM_LIKES):
                user = random.choice(User.objects.all())
                question = random.choice(Question.objects.all())
                QuestionLike.objects.get_or_create(user=user, question=question)

                user = random.choice(User.objects.all())
                answer = random.choice(Answer.objects.all())
                AnswerLike.objects.get_or_create(user=user, answer=answer)
        except IntegrityError:
            self.stdout.write(self.style.WARNING('Ошибка при добавлении лайков'))

        self.stdout.write(self.style.SUCCESS('Лайки созданы'))

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.create_users()
            self.create_profiles()

        with transaction.atomic():
            self.create_tags()

        with transaction.atomic():
            self.create_questions()

        with transaction.atomic():
            self.create_answers()

        with transaction.atomic():
            self.create_likes()

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена фейковыми данными!'))



