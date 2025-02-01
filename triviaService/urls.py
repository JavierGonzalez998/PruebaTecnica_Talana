from django.urls import path
from .views import AdminTriviaView,AdminTriviaQuestions, AdminQuestionAnswers, AdminUserTrivia, UserTriviaView, UserQuestionAnswerView, UserLeaderBoardView

# api/v1/game/
urlpatterns = [
    # Rutas Administrador
    path('admin/trivia/', AdminTriviaView.as_view(), name='adminTrivia'), # ✅
    path('admin/trivia/<int:id>/', AdminTriviaView.as_view(), name='adminTrivia'), #✅
    path("admin/trivia/<int:id>/question/", AdminTriviaQuestions.as_view(), name='adminTriviaQuestions'),#✅
     path("admin/trivia/<int:id>/question/<int:idQuestion>", AdminTriviaQuestions.as_view(), name='adminTriviaQuestions'), #✅
    path('admin/trivia/question/<int:id>/',AdminQuestionAnswers.as_view(), name='adminQuestionAnswers'),  #✅
    path('admin/trivia/question/<int:id>/<int:idAnswer>',AdminQuestionAnswers.as_view(), name='adminQuestionAnswers'),
    path('admin/trivia/user/', AdminUserTrivia.as_view(), name="adminUserTrivia"), #✅
    path('admin/trivia/user/<int:id>/', AdminUserTrivia.as_view(), name="adminUserTrivia"), #✅
    # Rutas Usuario
    path('trivia/', UserTriviaView.as_view(), name='userTrivia'), #✅
    path('trivia/<int:id>/', UserQuestionAnswerView.as_view(), name="userQuestionAnswer"),
    path('leaderboard/', UserLeaderBoardView.as_view(), name="userLeaderBoard"),  #✅
    path('leaderboard/<int:id>/', UserLeaderBoardView.as_view(), name="userLeaderBoardWithId") #✅
]