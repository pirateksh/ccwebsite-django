from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Quiz,Question,Option,Answer
from django.contrib.auth.models import User 
from .forms import QuizCreationForm,QuestionCreationForm,OptionCreationForm,AnswerCreationForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def quiz_view(request):
	quiz1 = Quiz.objects.all().first()
	questions = Question.objects.all() #return Query Set i.e. <QuerySet [<Question: Question object (1)>, <Question: Question object (2)>]>
	options = Option.objects.all() 
	answers = Answer.objects.all()
	# for question in questions:
		# print(question.option1)
	print(answers)
	return render(request,'quizapp/quiz.html',{'quiz1':quiz1,'questions':questions,'options':options,'answers':answers})
@login_required
def create_quiz(request):
	if request.method == 'POST':
		form = QuizCreationForm(request.POST)
		form.instance.instructions = request.POST.get('instr') #i.e. get('name_attribute')
		form.instance.author = request.user
		'''
		Above statement will throw following error:
			Cannot assign "'Ankit@mnnit.com'": "Quiz.author" must be a "User" instance.
		when
		'''
		if form.is_valid():
			form.save()
			# messages.success(request,f'Commeted Successfully!')
		# redirect(request.path_info)
			return HttpResponse("Form Saved")
		else:
			if form.errors:
				for field in form:
					for error in field.errors:
						print(error)
			return HttpResponse("Something Bad Just Happend")
		

	else:
		form = QuizCreationForm()
		context = {
			'form':form
		}
		return render(request,"quizapp/create_quiz.html",context)


def create_question(request):
	if request.method == 'POST':
		form_que = QuestionCreationForm(request.POST)
		form_que.instance.quiz = Quiz.objects.all().last()
		if form_que.is_valid():
			form_que.save()
		form_opt = OptionCreationForm(request.POST)
		form_ans = AnswerCreationForm(request.POST)
		form_opt.instance.quiz = Quiz.objects.all().last()
		form_ans.instance.quiz = Quiz.objects.all().last()
		form_opt.instance.question = Question.objects.all().last()
		form_ans.instance.question = Question.objects.all().last()
		if form_opt.is_valid():
			form_opt.save()
		if form_ans.is_valid():
			form_ans.save()
		return HttpResponse("Question Addded Successfully")