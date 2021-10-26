from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'pybo'

urlpatterns = [
    # base
    # path('', views.index, name='index'),
    # path('<int:question_id>/', views.detail, name='detail'),
    path('', views.IndexListView.as_view(), name='index'),
    path('<int:question_id>/', views.QuestionDetailView.as_view(), name='detail'),

    # question
    # path('question/create/', views.question_create, name='question_create'),
    # path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    # path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('question/create/',
         login_required(views.QuestionCreateView.as_view()), name='question_create'),
    path('question/modify/<int:question_id>/',
         login_required(views.QuestionUpdateView.as_view()), name='question_modify'),
    path('question/delete/<int:question_id>/', views.QuestionDeleteView.as_view(), name='question_delete'),

    # answer
    # path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    # path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    # path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('answer/create/<int:question_id>/', login_required(views.AnswerCreateView.as_view()), name='answer_create'),
    path('answer/modify/<int:answer_id>/', login_required(views.AnswerUpdateView.as_view()), name='answer_modify'),
    path('answer/delete/<int:answer_id>/', login_required(views.AnswerDeleteView.as_view()), name='answer_delete'),


    # comment question
    # path('comment/create/question/<int:question_id>/', views.comment_create_question, name='comment_create_question'),
    # path('comment/modify/question/<int:comment_id>/', views.comment_modify_question, name='comment_modify_question'),
    # path('comment/delete/question/<int:comment_id>/', views.comment_delete_question, name='comment_delete_question'),
    path('comment/create/question/<int:question_id>/',
         login_required(views.CommentQuestionCreateView.as_view()), name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/',
         login_required(views.CommentQuestionUpdateView.as_view()), name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/',
         login_required(views.CommentQuestionDeleteView.as_view()), name='comment_delete_question'),

    # comment answer
    # path('comment/create/answer/<int:answer_id>/', views.comment_create_answer, name='comment_create_answer'),
    # path('comment/modify/answer/<int:comment_id>/', views.comment_modify_answer, name='comment_modify_answer'),
    # path('comment/delete/answer/<int:comment_id>/', views.comment_delete_answer, name='comment_delete_answer'),
    path('comment/create/answer/<int:answer_id>/',
         login_required(views.CommentAnswerCreateView.as_view()), name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/',
         login_required(views.CommentAnswerUpdateView.as_view()), name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/',
         login_required(views.CommentAnswerDeleteView.as_view()), name='comment_delete_answer'),

    # vote
    # path('vote/question/<int:question_id>/', views.vote_question, name='vote_question'),
    # path('vote/answer/<int:answer_id>/', views.vote_answer, name='vote_answer'),
    path('vote/question/<int:question_id>/', login_required(views.VoteQuestionView.as_view()), name='vote_question'),
    path('vote/answer/<int:answer_id>/', login_required(views.VoteAnswerView.as_view()), name='vote_answer'),
]