from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from app.models import QuestionLike, AnswerLike, Question, Answer, Profile


# сигнал для обновления рейтинга вопроса
@receiver(post_save, sender=QuestionLike)
def update_question_rating(sender, instance, created, **kwargs):
    if created:
        # обновляем рейтинг вопроса
        instance.question.update_rating()

        # обновляем рейтинг пользователя
        instance.question.author.profile.update_rating()


# сигнал для обновления рейтинга ответа
@receiver(post_save, sender=AnswerLike)
def update_answer_rating(sender, instance, created, **kwargs):
    if created:
        # обновляем рейтинг ответа
        instance.answer.update_rating()

        # обновляем рейтинг пользователя
        instance.answer.author.profile.update_rating()

