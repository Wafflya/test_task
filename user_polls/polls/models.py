from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Poll(models.Model):
    title = models.CharField('Название', max_length=100)
    start_date = models.DateField('Дата старта', null=False, blank=False)
    end_date = models.DateField('Дата окончания', null=False, blank=False)
    description = models.TextField('Описание')

    def __str__(self):
        return 'Опрос {}'.format(self.title)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    QUES_TYPES = [
        ('TX', 'Ответ текстом'),
        ('OP', 'Ответ с выбором одного варианта'),
        ('MP', 'Ответ с выбором нескольких вариантов')
    ]
    poll = models.ForeignKey(Poll, verbose_name='В каком опросе', on_delete=models.CASCADE,
                             related_name='questions_in_poll')
    text = models.TextField('Текст вопроса', null=False, blank=False, )
    type = models.CharField('Тип вопроса', max_length=2, choices=QUES_TYPES)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


# Варианты ответа для вопросов с выбором
class Option(models.Model):
    question = models.ForeignKey(Question, verbose_name='Вопрос в котором', related_name='options',
                                 on_delete=models.CASCADE)
    text = models.TextField('Текст варианта')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'


# Пройденный опрос(участник)
class Participant(models.Model):
    respondent_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    respondent_id = models.PositiveIntegerField('ID пользователя', blank=True, null=True)
    completed_poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        if self.respondent_user:
            return "Участник {} в {}".format(self.respondent_user, self.completed_poll)
        if self.respondent_id:
            return "Аноним {}id в {}".format(self.respondent_id, self.completed_poll)

    class Meta:
        verbose_name = 'Респондент'
        verbose_name_plural = 'Респонденты'


#
class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name='На какой вопрос', on_delete=models.CASCADE, related_name='answers')
    polled = models.ForeignKey(Participant, verbose_name='Кем даны', on_delete=models.CASCADE)
    reply = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return '{} на {}'.format(self.polled, self.question)
