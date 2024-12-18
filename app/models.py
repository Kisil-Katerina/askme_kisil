from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# менеджер
class QuestionManager(models.Manager):

    # Возвращает вопросы, отсортированные по количеству лайков (в порядке убывания).
    def get_best_questions(self):

        return self.annotate(likes_count=Count('likes')).order_by('-likes_count')

    # Возвращает вопросы, отсортированные по дате создания.
    def get_newest_questions(self):
        
        return self.order_by('-created_at')


# профиль пользователя
class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default="default-avatar.png", upload_to="avatar/%Y/%m/%d")
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        # все вопросы пользователя, считаем количество лайков для этих вопросов
        questions_likes = QuestionLike.objects.filter(question__author=self.user).count()

        # все ответы пользователя, считаем количество лайков для этих ответов
        answers_likes = AnswerLike.objects.filter(answer__author=self.user).count()

        # суммируем количество лайков на вопросах и ответах
        self.rating = questions_likes + answers_likes
        self.save()    

# тег
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# вопрос
class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='questions')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def update_rating(self):
        # обновляем рейтинг вопроса, основываясь на лайках
        self.rating = self.likes.count()
        self.save()
    
    def answer_count(self):
        return self.answers.count()


    def like(self, user):
        QuestionLike.objects.create(user=user, question=self)
        self.rating = self.likes.count()
        self.save()

    def unlike(self, user):
        try:
           like = QuestionLike.objects.get(user=user, question=self)
           like.delete()
           self.rating = self.likes.count()
           self.save()
        except QuestionLike.DoesNotExist:
             pass
         
    # менеджер
    objects = QuestionManager()
         
# ответ
class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Answer to: {self.question.title}"

    def update_rating(self):
        # обновляем рейтинг ответа, основываясь на лайках
        self.rating = self.likes.count()
        self.save()
        
    def like(self, user):
        AnswerLike.objects.create(user=user, answer=self)
        self.rating = self.likes.count()
        self.save()

    def unlike(self, user):
        try:
           like = AnswerLike.objects.get(user=user, answer=self)
           like.delete()
           self.rating = self.likes.count()
           self.save()
        except AnswerLike.DoesNotExist:
            pass

# лайк для вопроса
class QuestionLike(models.Model):
    user = models.ForeignKey(User, related_name='question_likes', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')  # ограничение на уникальность
        

# лайк для ответа
class AnswerLike(models.Model):
    user = models.ForeignKey(User, related_name='answer_likes', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'answer')   # ограничение на уникальность

        

