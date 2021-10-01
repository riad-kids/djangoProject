from rest_framework import serializers
from pybo.models import Question, Answer, Comment


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'subject',
            'content',
            'create_date',
            'modify_date'
        ]
        read_only_fields = ('id', 'create_date', 'modify_date')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'content',
            'question_id',
            'create_date',
            'modify_date'
        ]
        read_only_fields = ('id', 'create_date', 'modify_date')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'question_id',
            'answer_id',
            'create_date',
            'modify_date'
        ]
        read_only_fields = ('id', 'create_date', 'modify_date')
