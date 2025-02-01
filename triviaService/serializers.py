from rest_framework import serializers
from .models import Trivia, Question, Answer, UserTrivia, UserAnswer

class triviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trivia
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'user']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'required': False ,'read_only': True}
        }
class questionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'trivia', 'question', 'difficulty', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'required': False ,'read_only': True}
        }
class answerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer', 'is_correct', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'is_correct': {'required': True, 'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'required': False ,'read_only': True}
        }
class userTriviaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTrivia
        fields = ['id', 'user', 'trivia', 'score', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'required': False ,'read_only': True}
        }
        
class userAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'user', 'answered']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
        }