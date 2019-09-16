from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Quiz(models.Model):
	title = models.CharField(max_length=100)
	no_of_ques = models.PositiveIntegerField(default=0)
	max_score = models.PositiveIntegerField(default=0)
	time_lim = models.PositiveIntegerField(help_text="Time Limit should be in MINUTES.")
	instructions = models.TextField()
	author  = models.ForeignKey(User,on_delete=models.DO_NOTHING)
	date_created = models.DateTimeField(default = timezone.now)
	def __str__(self):
		return "{}".format(self.title)
	class Meta:
		ordering = ['id']
class UserQuizResult(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="quiz_title")
	score = models.PositiveIntegerField()

class Question(models.Model):
	quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
	question = models.TextField()
	def __str__(self):
		return "{}".format(self.question)
	class Meta:
		ordering = ['id']
class Option(models.Model):
	quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
	question = models.ForeignKey(Question,on_delete=models.CASCADE)
	option1 = models.TextField()
	option2 = models.TextField()
	option3 = models.TextField(null=True,blank=True)
	option4 = models.TextField(null=True,blank=True)
	def __str__(self):
		return "{}{}{}{}".format(self.option1,self.option2,self.option3,self.option4)
	class Meta:
		ordering = ['id']
class Answer(models.Model):
	'''
		Here We have used a convention that if a question is True False Type then
		we will have option 1 set to True and option 2 set to False.
	'''
	quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
	question = models.ForeignKey(Question,on_delete=models.CASCADE)

	Ans_Choices=(('1','option1'),('2','option2'),('3','option3'),('4','option4'))
	# def Ans_Choices(que):
		# here que is quizapp.Answer.question
		# return (('1',que.objects.all()),('2','option2'),('3','option3'),('4','option4'))
	# curr_question = Question.objects.get(id=id)
	# print(que)
	# def Ans_Choices():
		# obj = Option.objects.last()
	# 	curr_question = objs
	# 	# for obj in questions:
	# 	print(obj)
		# return(('1',getattr(obj,'option1')),('1',getattr(obj,'option2')),('1',getattr(obj,'option3')),('1',getattr(obj,'option4')))




		# return (('1','option1'),('2','option2'),('3','option3'),('4','option4'))
		# question = questions.filter(id = id)
		# for question in questions:
		# 	if(que == question.question):
			# return (('1',question.option1),('2',question.option2),('3',question.option3),('4',question.option4))
	corr_answer = models.CharField(max_length=1,choices=Ans_Choices)
	extra_info = models.TextField(null=True,blank=True)
	def __str__(self):
		return "{}".format(self.question)
	class Meta:
		ordering = ['id']