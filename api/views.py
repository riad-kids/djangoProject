from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from pybo.models import Question, Answer, Comment
from . serializers import QuestionSerializer, AnswerSerializer, CommentSerializer


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, create_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modify_date=timezone.now())


class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, create_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modify_date=timezone.now())


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, create_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modify_date=timezone.now())
