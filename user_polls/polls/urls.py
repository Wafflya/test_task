from django.urls import path

from .views import ActivePollsListView, CreatePoll, EditPoll, DeletePoll, CreateQuestion, AllQuestions, UpdateQuestion, \
    PollDetail, MyAnswers, MyAnonAnswers

app_name = 'polls'

urlpatterns = [
    path('active_polls/', ActivePollsListView.as_view(), name='active_polls'),
    path('create_poll/', CreatePoll.as_view()),
    path('edit_poll/<int:pk>', EditPoll.as_view()),
    path('delete_poll/<int:pk>', DeletePoll.as_view()),

    path('all_questions/', AllQuestions.as_view()),
    path('create_question/', CreateQuestion.as_view()),
    path('edit_question/<int:pk>', UpdateQuestion.as_view()),

    path('poll_detail/<int:pk>', PollDetail.as_view()),
    path('my_answers/', MyAnswers.as_view()),
    path('anonym_answers/<int:pk>', MyAnonAnswers.as_view(), name='anon_ans'),

]
