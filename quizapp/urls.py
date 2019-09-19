from django.urls import path
from .import views as quizapp_views 
urlpatterns = [   
	path('<str:username>/quiz_home/',quizapp_views.quiz_home,name="quiz_home"), 
	path('<str:username>/quiz/<int:pk>/',quizapp_views.quiz_view,name="take_quiz"),
	path('<str:username>/quiz/<int:pk>/share/',quizapp_views.share_quiz_perfo,name="share_quiz_perfo"),
	path('quiz/submit_quiz/<int:pk>/',quizapp_views.submitquizview,name="submit_quiz"),
	path('create-quiz/',quizapp_views.create_quiz,name="create_quiz"),
	path('create-quiz/questions/',quizapp_views.create_questions,name="create_questions"),
	# path('take_quiz/',quizapp_views.take_quiz_view,name="take_quiz_vish"),
	path('create_quiz/questions/<int:pk>/',quizapp_views.ques_detail_view,name="ques_detail"),
]