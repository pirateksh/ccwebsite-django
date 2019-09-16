from django.urls import path
from .import views as quizapp_views 
urlpatterns = [
    
	path('quiz/',quizapp_views.quiz_view,name="take_quiz"),
	path('create-quiz/',quizapp_views.create_quiz,name="create_quiz"),
	path('create-quiz/questions/',quizapp_views.create_question,name="create_question")
]