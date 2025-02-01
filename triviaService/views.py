from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import triviaSerializer, questionSerializer, answerSerializer, userTriviaSerializer, userAnswerSerializer
from .models import Trivia, Question, Answer, UserTrivia, UserAnswer, Difficulty
from rest_framework.permissions import IsAuthenticated, AllowAny
from userService.utils import get_user_id_from_request, validate_admin, validate_user
from django.db import transaction
from userService.models import User
import random
# Panel Administrador

# Crear la vista AdminTriviaView que permita listar, crear trivia y actualizar las trivias
class AdminTriviaView(APIView):
    # listar todas las trivias
    def get(self, request):
        # Valida que el usuario sea un administrador
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin  
        # Obtiene todas las trivias 
        trivia = Trivia.objects.all()
        serializer = triviaSerializer(trivia, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Crea una trivia
    # Body: name: string, description: string
    def post(self, request):
        # Valida que el usuario sea un administrador
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        # Crea la trivia
        body = request.data
        body["user"] = admin.id
        serializer = triviaSerializer(data=body)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualiza una trivia
    # QueryParam: id: number, Id de la trivia
    # Body: name: string, description: string
    def put(self, request, id):
        # Valida que el usuario sea un administrador
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        # Obtiene la trivia
        trivia = Trivia.objects.filter(pk=id).first()
        if not trivia:
            return Response({'error': 'trivia not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualiza la trivia
        body = request.data
        body["user"] = admin.id
        serializer = triviaSerializer(trivia, data=body)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Elimina una trivia
    # QueryParam: id: number, Id de la trivia   
    def delete(self, request, id):
        # Valida que el usuario sea un administrador
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        trivia = Trivia.objects.filter(pk=id).first()
        if not trivia:
            return Response({"message": "No se encuentra la Trivia a eliminar"}, status=status.HTTP_404_NOT_FOUND)

        trivia.delete()
        return Response({"message": "Trivia Eliminada!"}, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'GET' or self.request.method == 'PUT' or self.request.method == "DELETE":
            return [IsAuthenticated()]
        return super().get_permissions()

# Crear la vista AdminTriviaQuestions que permita listar, crear y actualizar las preguntas de una trivia
class AdminTriviaQuestions(APIView):
    # Listar las preguntas de una trivia
    # QueryParam: id: number, Id de la trivia
    def get(self, request, id):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 

        trivia = Trivia.objects.filter(pk=id).first()
        if not trivia:
            return Response({'error': 'trivia not found'}, status=status.HTTP_404_NOT_FOUND)
        questions = Question.objects.filter(trivia=trivia)
        serializer = questionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Crear una pregunta de una trivia
    # QueryParam: id: number, Id de la trivia
    # Body: question: string, difficulty: number
    def post(self, request, id):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        
        trivia = Trivia.objects.filter(pk=id).first()
        if not trivia:
            return Response({'error': 'trivia not found'}, status=status.HTTP_404_NOT_FOUND)
        
        body = request.data
        body['trivia'] = trivia.id
        serializer = questionSerializer(data=body)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar una pregunta de una trivia
    # QueryParam: id: number, Id de la trivia
    # Body: id: number, question: string, difficulty: number
    def put(self, request, id):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin
        
        trivia = Trivia.objects.filter(pk=id).first()
        if not trivia:
            return Response({'error': 'trivia not found'}, status=status.HTTP_404_NOT_FOUND)
        
        body = request.data
        idQuestion = body["id"] 
        question = Question.objects.filter(pk=idQuestion).first()
        if not question:
            return Response({'error': 'question not found'}, status=status.HTTP_404_NOT_FOUND)
        
        body['trivia'] = trivia.id
        serializer = questionSerializer(question, data=body)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # Eliminar una pregunta de una trivia
    # QueryParam: id: number, Id de la trivia    
    def delete(self, request, id, idQuestion):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin
        question = Question.objects.filter(pk=idQuestion).first()
        if not question:
            return Response({"message": "No se encuentra la pregunta a eliminar"}, status=status.HTTP_404_NOT_FOUND)
        question.delete()
        return Response({"message": "Pregunta Eliminada!"}, status=status.HTTP_200_OK)


    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'GET' or self.request.method == 'PUT' or self.request.method == "DELETE":
            return [IsAuthenticated()]
        return super().get_permissions()

# Crear la vista AdminQuestionAnswers que permita listar, crear y actualizar las respuestas de una pregunta
class AdminQuestionAnswers(APIView):
    # Listar las respuestas de una pregunta
    # QueryParam: id: number, Id de la pregunta
    def get(self, request, id):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        
        question = Question.objects.filter(pk=id).first()
        if not question:
            return Response({'error': 'question not found'}, status=status.HTTP_404_NOT_FOUND)
        answers = Answer.objects.filter(question=question)
        serializer = answerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Crear una respuesta de una pregunta
    # QueryParam: id: number, Id de la pregunta
    # Body: answer: string, is_correct: number
    def post(self, request, id):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        
        question = Question.objects.filter(pk=id).first()
        if not question:
            return Response({'error': 'question not found'}, status=status.HTTP_404_NOT_FOUND)
        
        body = request.data
        body['question'] = question.id

        # Serializar la nueva respuesta
        serializer = answerSerializer(data=body)

        if serializer.is_valid():
            with transaction.atomic(): 
                # Si la nueva respuesta es correcta, poner las otras en 0
                if body.get("is_correct", 0) == 1:
                    Answer.objects.filter(question=question).update(is_correct=0)

                serializer.save()  # Guardar la nueva respuesta

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar una respuesta de una pregunta
    # QueryParam: id: number, Id de la pregunta
    # Body: id: number, answer: string, is_correct: number
    def put(self, request, id):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        question = Question.objects.filter(pk=id).first()
        if not question:
            return Response({'error': 'question not found'}, status=status.HTTP_404_NOT_FOUND)
        
        answers = Answer.objects.filter(question=question).all()
        if not answers:
            return Response({'error': 'answer not found'}, status=status.HTTP_404_NOT_FOUND)
        
        body = request.data
        response = answers
        response = answerSerializer(response, many=True).data
        for answer in response:
            answer["is_correct"] = 0
        for answer in response:
            if answer["id"] == body["id"]:
                answer["answer"] = body["answer"]
                answer["is_correct"] = 1
                break

        if not any(item["is_correct"] == 1 for item in response):
            return Response({"message": "Debe haber al menos 1 elemento con respuesta correcta"})

        for i in response:
            answ = Answer.objects.filter(pk=i["id"]).first()
            serializer = answerSerializer(answ, data=i)
            if serializer.is_valid():
                serializer.save()
        return Response(response, status=status.HTTP_200_OK)
    
    def delete(self, request, id, idAnswer):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        
        answer = Answer.objects.filter(pk=idAnswer).first()
        if not answer:
            return Response({'message': 'No se encontró la respuesta'}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si la respuesta es la correcta
        if answer.is_correct:
            return Response({'message': 'No se puede eliminar la respuesta correcta'}, status=status.HTTP_400_BAD_REQUEST)

        # Si no es la correcta, eliminarla
        answer.delete()
        return Response({'message': 'Respuesta eliminada correctamente!'}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'GET' or self.request.method == 'PUT':
            return [IsAuthenticated()]
        return super().get_permissions()
    
# Crear la vista AdminQuestionAnswers que permita obtener y listar los usuarios que participarán en las trivias
class AdminUserTrivia(APIView):
    def get(self, request):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        userTrivia = UserTrivia.objects.all()
        serializer = userTriviaSerializer(userTrivia, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # QueryParam: id: number, Id de usuario
    # Body: trivia: number
    def post(self, request, id):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin 
        user = User.objects.filter(pk=id).first()
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        trivia = Trivia.objects.filter(pk=request.data["trivia"]).first()
        if not trivia:
            return Response({'error': 'trivia not found'}, status=status.HTTP_404_NOT_FOUND)
        data={}
        data["user"] = user.id
        data["trivia"] = trivia.id
        data["score"] = 0
        serializer = userTriviaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado en la trivia'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        admin = validate_admin(request)
        if isinstance(admin, Response):
            return admin
        
        user = User.objects.filter(pk=id).first()
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        userTrivia = UserTrivia.objects.filter(user=user).first()
        if not userTrivia:
            return Response({"message": "No se encontró al usuario registrado en la trivia"}, status=status.HTTP_404_NOT_FOUND)
        userTrivia.delete()
        return Response({"message": "Usuario eliminado de la trivia correctamente!"}, status=status.HTTP_200_OK)
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'GET' or self.request.method == 'PUT':
            return [IsAuthenticated()]
        return super().get_permissions()
# Panel de Usuario
class UserTriviaView(APIView):
    # Listar las trivias que el administrador asignó al usuario
    def get(self, request):
        user = validate_user(request)
        if isinstance(user, Response):
            return user
        data = []
        userTrivia = UserTrivia.objects.filter(user=user)
        for user in userTrivia:
            trivia = user.trivia  # Obtener la trivia asociada
            # Contar cuántas preguntas de esta trivia han sido respondidas por el usuario
            answered_count = UserAnswer.objects.filter(user_id=user.id, question__trivia=trivia).count()
            total_questions = Question.objects.filter(trivia=trivia).count()
            # Serializar la trivia y agregar el número de preguntas respondidas
            trivia_data = triviaSerializer(trivia).data
            trivia_data['answered_questions'] = answered_count
            trivia_data['total_questions'] = total_questions

            data.append(trivia_data)
        return Response({'trivias': data}, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'GET' or self.request.method == 'PUT':
            return [IsAuthenticated()]
        return super().get_permissions()

class UserQuestionAnswerView(APIView):
    # Muestra la pregunta de la trivia con su respuesta
    # QueryParam: id: number, Id de la trivia
    def get(self, request, id):
        # Obtiene y valida el usuario
        user = validate_user(request)
        if isinstance(user, Response):
            return user
        # Obtiene la trivia por el Query Params
        trivia = Trivia.objects.filter(pk=id).first()
        if not trivia:
            return Response({'error': 'trivia not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Se obtiene el usuario registrado
        userTrivia = UserTrivia.objects.filter(trivia=trivia, user=user).first()
        if not userTrivia:
            return Response({'message': 'No se encuentra registrado en la trivia. Por favor, comuníquese con el administrador para que sea agregado/a'}, status=status.HTTP_404_NOT_FOUND)
        
        # Se obtienen las preguntas que no ha respondido el usuario
        userQuestion = Question.objects.filter(trivia=trivia).exclude(id__in=UserAnswer.objects.filter(user=user).values_list("question_id", flat=True)).all()
        if not userQuestion:
            return Response({'message': 'No quedan preguntas por responder, revisa el tablero para ver tu resultado!'}, status=status.HTTP_200_OK)
        
        # Se selecciona solo 1 de las preguntas de forma aleatoria
        userQuestion = questionSerializer(userQuestion, many=True).data
        userQuestion = userQuestion[random.randint(0, len(userQuestion)-1)]

        #Se obtienen las respuestas y se arma los datos para responder
        answer = Answer.objects.filter(question=userQuestion["id"]).all()
        data = {}
        answers = []
        data["id_question"] = userQuestion["id"]
        data["question"] = userQuestion["question"]
        for i in answer:
            answers.append({"id": i.id, "answer": i.answer})
        data["answers"] = answers
        return Response(data, status=status.HTTP_200_OK)
    
    # Responde la pregunta y registra el puntaje
    # QueryParam: id: number, Id de la trivia
    # Body: question: number, answer: number
    def post(self, request, id):
        # Obtiene y valida el usuario
        user = validate_user(request)
        if isinstance(user, Response):
            return user
        
        # Obtiene la trivia
        trivia = Trivia.objects.filter(pk=id).first()
        if not trivia:
            return Response({'error': 'trivia not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Obtiene el usuario registrado en la trivia
        userTrivia = UserTrivia.objects.filter(trivia=trivia, user=user).first()
        if not userTrivia:
            return Response({'message': 'No se encuentra registrado en la trivia. Por favor, comuníquese con el administrador para que sea agregado/a'}, status=status.HTTP_404_NOT_FOUND)
        
        # Obtiene la pregunta y la respuesta
        body = request.data
        idQuestion = body["question"]
        answer = body['answer']
        question = Question.objects.filter(pk=idQuestion, trivia=userTrivia.trivia).first()
        if not question:
            return Response({'message': 'No se encontró la pregunta, revise nuevamente'}, status=status.HTTP_404_NOT_FOUND)
        answer = Answer.objects.filter(pk=answer, question=question).first()
        if not answer:
            return Response({'message': 'No se encontró la respuesta, revise nuevamente'}, status=status.HTTP_404_NOT_FOUND)
        
        # Se registra al usuario que respondió
        userAnswer = UserAnswer.objects.filter(user=user, question=question).first()
        if not userAnswer:
            userAnswer = UserAnswer()
            userAnswer.user = user
            userAnswer.question = question
            userAnswer.answered = 1
            userAnswer.save()
    
        # Registra el puntaje
        if answer.is_correct == 1 and userTrivia:
            userTrivia.score += question.difficulty.id
            userTrivia.save()
        return Response({'message': 'Respuesta guardada'}, status=status.HTTP_200_OK)
        
        
    
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'GET' or self.request.method == 'PUT':
            return [IsAuthenticated()]
        return super().get_permissions()

class UserLeaderBoardView(APIView):
    def get(self, request, id=None):
        trivia = Trivia.objects.filter(pk=id).first() if id is not None else Trivia.objects.all()
        if not trivia:
            return Response({'message': 'No se encuentran trivias registradas, comuníquese con su administrador para solicitar el ingreso de trivias'}, status=status.HTTP_404_NOT_FOUND)
        if isinstance(trivia, Trivia):
            userTrivia = UserTrivia.objects.filter(trivia=trivia).order_by('-score').all()
            serializer = userTriviaSerializer(userTrivia, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        response = []
        for t in trivia:
            print(t)
            userTrivia = UserTrivia.objects.filter(trivia=t).order_by('-score')
            serializer = userTriviaSerializer(userTrivia, many=True)
            data= serializer.data
            response.append({
                "trivia": t.name,
                "users": data
            })
        return Response(response, status=status.HTTP_200_OK)
    
    def get_permissions(self):    
        if self.request.method == 'GET':
            return [AllowAny()]
        return super().get_permissions()


