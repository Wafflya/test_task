from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import exceptions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser
from django.core.exceptions import ObjectDoesNotExist

from _datetime import date
from .models import Poll, Question, Participant, Answer, Option
from .serializers import PollSerializer, PollEditSerializer, PollCreateSerializer, QuestionCreateSerializer, \
    QuestionSerializer, QuestionEditSerializer, PollDetailSerializer, AnsweredPollDetailSerializer


def is_poll_active(poll):
    current_date = date.today()
    if poll.start_date > current_date or poll.end_date < current_date:
        return False
    else:
        return True


class AdminAPIView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]


class ActivePollsListView(APIView):

    def get(self, request):
        current_date = date.today()
        polls = Poll.objects.filter(start_date__lte=current_date, end_date__gte=current_date)
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)


class CreatePoll(AdminAPIView):

    def post(self, request):
        poll = PollCreateSerializer(data=request.data)
        if poll.is_valid():
            poll.create(validated_data=request.data)
            return Response(status=201)
        else:
            raise exceptions.ValidationError('Ошибка ввода данных')


class EditPoll(AdminAPIView):

    def get(self, request, pk):
        poll = get_object_or_404(Poll, id=pk)
        serializer = PollSerializer(poll)
        return Response(serializer.data)

    def put(self, request, pk):
        poll = get_object_or_404(Poll, id=pk)
        serializer = PollEditSerializer(data=request.data)
        if serializer.is_valid():
            PollEditSerializer.update(self, instance=poll, validated_data=request.data)
            return Response(serializer.data)
        else:
            raise exceptions.ValidationError('Ошибка ввода данных')


class DeletePoll(AdminAPIView):
    def delete(self, request, pk):
        poll = get_object_or_404(Poll, id=pk)
        dd = poll.id
        poll.delete()
        return Response('Poll with id {} deleted'.format(dd))


class AllQuestions(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class CreateQuestion(AdminAPIView):

    def post(self, request):
        question = QuestionCreateSerializer(data=request.data)
        if question.is_valid():
            print(question)
            question.create(validated_data=request.data)
            return Response(status=201)
        else:
            raise exceptions.ValidationError('Ошибка ввода данных')


class UpdateQuestion(AdminAPIView):
    def get(self, request, pk):
        question = get_object_or_404(Question, id=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        ques = get_object_or_404(Question, id=pk)
        serializer = QuestionEditSerializer(data=request.data)
        if serializer.is_valid():
            QuestionEditSerializer.update(self, instance=ques, validated_data=request.data)
            return Response(serializer.data)
        else:
            raise exceptions.ValidationError('Ошибка ввода данных')

    def delete(self, request, pk):
        ques = get_object_or_404(Question, id=pk)
        dd = ques.text
        ques.delete()
        return Response('Вопрос {} успешно удалён'.format(dd))


class PollDetail(APIView):
    def get(self, request, pk):
        poll = get_object_or_404(Poll, id=pk)
        if not is_poll_active(poll):
            return Response('Этот опрос неактивен', status=403)
        serializer = PollDetailSerializer(poll)
        return Response(serializer.data)

    def post(self, request, pk):
        poll = get_object_or_404(Poll, id=pk)
        if not is_poll_active(poll):
            return Response('Этот опрос неактивен', status=405)

        if request.user.is_authenticated:
            try:
                p = Participant.objects.get(respondent_user=request.user, completed_poll=poll)
                p.delete()
                p = Participant.objects.create(respondent_user=request.user, completed_poll=poll)
            except ObjectDoesNotExist:
                p = Participant.objects.create(respondent_user=request.user, completed_poll=poll)
        else:
            if 'anon_user_id' not in request.data:
                return Response('Не указан айди анонимного пользователя')
            else:
                try:
                    us_id = int(request.data['anon_user_id'])
                    p = Participant.objects.get(respondent_id=us_id, completed_poll=poll)
                    p.delete()
                    p = Participant.objects.create(respondent_id=us_id, completed_poll=poll)

                except ValueError:
                    return Response('Не верный формат айди')
                except ObjectDoesNotExist:
                    p = Participant.objects.create(respondent_id=us_id, completed_poll=poll)

        for i in request.data:
            try:
                if i == 'anon_user_id':
                    continue
                q = Question.objects.get(id=int(i))
            except ValueError:
                raise exceptions.ValidationError('Не числовое значение в графе вопрос')
            except ObjectDoesNotExist:
                raise exceptions.ValidationError('Ссылка на вопрос указывает на несуществующий вопрос')
            if q not in poll.questions_in_poll.all():
                raise exceptions.ValidationError('Ссылка на вопрос указывает на вопрос с другого опроса')

            if len(str(request.data[i])) == 0:
                raise exceptions.ValidationError('Вы не ответили на один из вопросов')

            if q.type == "OP":
                try:
                    val = Option.objects.get(id=int(request.data[i]))
                except ValueError:
                    raise exceptions.ValidationError("Не числовое значение в варианте ответа")
                except ObjectDoesNotExist:
                    raise exceptions.ValidationError("Не существует выбранного варианта вообще")

                if val in q.options.all():
                    Answer.objects.create(polled=p, question=q,
                                          reply=val)
                else:
                    raise exceptions.ValidationError("Нет такого варианта в вопросе")
            if q.type == "TX":
                Answer.objects.create(polled=p, question=q, reply=request.data[i])
            if q.type == "MP":
                str_ans = []
                try:
                    chooses = set(int(i) for i in str(request.data[i]).split(','))
                except ValueError:
                    raise exceptions.ValidationError("Неверный формат ответа на вопрос типа MP")

                for j in chooses:
                    try:
                        val = Option.objects.get(id=int(j))
                    except ValueError:
                        raise exceptions.ValidationError("Не числовое значение в варианте ответа")
                    except ObjectDoesNotExist:
                        raise exceptions.ValidationError("Не существует выбранного варианта вообще")

                    if val not in q.options.all():
                        raise exceptions.ValidationError("Нет такого варианта в заданном вопросе")
                    else:
                        str_ans.append(get_object_or_404(Option, id=int(j)).text)
                Answer.objects.create(polled=p, question=q, reply=', '.join(str_ans))

        return Response(status=200)


class MyAnswers(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('polls:anon_ans', pk=0)
        else:
            auth_user = Participant.objects.filter(respondent_user=request.user)

            result2 = []
            for i in auth_user:
                result = AnsweredPollDetailSerializer(i.completed_poll).data
                result['questions_in_poll'] = []
                ans_dict = {}
                for n, j in enumerate(i.completed_poll.questions_in_poll.all()):
                    anss = str(n + 1) + '. ' + str(j.text)
                    try:
                        a = Answer.objects.get(question=j, polled=i).reply
                        ans_dict[anss] = a
                    except ObjectDoesNotExist:
                        ans_dict[anss] = "Не ответил"
                result['questions_in_poll'] = [ans_dict]
                result2.append(result)

        return Response(result2)


class MyAnonAnswers(APIView):
    def get(self, request, pk):
        if pk == 0:
            return Response("Не указан id пользователя в url", status=400)
        anon_user = Participant.objects.filter(respondent_id=pk)

        result2 = []

        for i in anon_user:
            result = AnsweredPollDetailSerializer(i.completed_poll).data
            result['questions_in_poll'] = []
            ans_dict = {}
            for n, j in enumerate(i.completed_poll.questions_in_poll.all()):
                anss = str(n + 1) + '. ' + str(j.text)
                try:
                    a = Answer.objects.get(question=j, polled=i).reply
                    ans_dict[anss] = a
                except ObjectDoesNotExist:
                    ans_dict[anss] = "Не ответил"
            result['questions_in_poll'] = [ans_dict]
            result2.append(result)
        return Response(result2)
