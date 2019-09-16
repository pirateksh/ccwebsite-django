from django.contrib import admin
from django.contrib.auth.models import User
from .models import Quiz,Question,Option,Answer,UserQuizResult
# Register your models here.

class UserQuizResultAdmin(admin.ModelAdmin):
	model = UserQuizResult
	list_display = ['id','user','quiz_title','score','max_score']

	def user(self,instance):
		return instance.user.username
	def quiz_title(self,instance):
#instance is the instance of Quiz(current) class
		return instance.quiz.title
	def max_score(self,instance):
		return instance.quiz.max_score

class QuizAdmin(admin.ModelAdmin):
	model = Quiz
	list_display = ['id','title','no_of_ques','time_lim','instructions','author_name','date_created']
	def author_name(self,instance):
		#instance is the instance of Quiz(current) class
		return instance.author.username

class QuestionAdmin(admin.ModelAdmin):
	model = Question
	list_display = ['id','quiz_title','question']
	def quiz_title(self,instance):
		#instance is the instance of Question(current) class
		return instance.quiz.title
class OptionAdmin(admin.ModelAdmin):
	model = Option
	list_display = ['id','quiz_title','question','option1','option2','option3','option4']
	def quiz_title(self,instance):
		#instance is the instance of Question(current) class
		return instance.quiz.title
class AnswerAdmin(admin.ModelAdmin):
	model = Answer
	list_display = ['id','quiz_title','question_name','corr_answer','extra_info']
	def quiz_title(self,instance):
		#instance is the instance of Question(current) class
		return instance.quiz.title
	def question_name(self,instance):
		#instance is the instance of Question(current) class
		return instance.question.question
	

admin.site.register(UserQuizResult,UserQuizResultAdmin)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Option,OptionAdmin)
admin.site.register(Answer,AnswerAdmin)
'''
Below Code Works when any one of the fields is a foreign key
	def get_name(self,obj):
		return obj.Hostels.Type
	get_name.short_description = 'Type'#Renames column head
'''