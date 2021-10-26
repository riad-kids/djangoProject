from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . views import QuestionView, AnswerView, CommentView

post_list = {
    'post': 'create',
    'get': 'list'
}
post_detail = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}

urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('question/', QuestionView.as_view(post_list), name='post_list'),
    path('question/<int:pk>/', QuestionView.as_view(post_detail), name='post_detail'),

    path('answer/', AnswerView.as_view({'get': 'list'}), name='post_list'),
    path('answer/<int:pk>/', AnswerView.as_view(post_detail), name='post_detail'),

    path('comment/', CommentView.as_view({'get': 'list'}), name='post_list'),
    path('comment/<int:pk>/', CommentView.as_view(post_detail), name='post_detail'),
])