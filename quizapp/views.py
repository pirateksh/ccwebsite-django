from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,reverse
from django.contrib import messages
import random
from django.http import JsonResponse
from .models import UserQuizResult,CurrentQuiz,Quiz,Question,Option,Answer,RandomQuizQuestion
from django.contrib.auth.models import User 
from .forms import QuizCreationForm,QuestionCreationForm,OptionCreationForm,AnswerCreationForm
from django.contrib.auth.decorators import login_required,user_passes_test
'''
check funtion for user_passes_test decorator:-
'''
def is_admin(user):#this function return True only if user is an admin 
	if user:
		# if user.groups.filter(name="Teacher").count():
		# 	return True
		if user.is_superuser:
			return True
		else:
			return False
	else:
		return False
def is_atmt(request,question_id):
	for entry in CurrentQuiz.objects.all().filter(user=request.user,question_id=int(question_id)):
		if entry.is_atm == True:
			return entry.id
	return False

def is_corrt(question_id,sel_ans):
	print(int(question_id))
	print(Answer.objects.all().filter(question_id=int(question_id)).first().id)
	print(type(Answer.objects.all().filter(question_id=int(question_id)).first().id))
	print(type(question_id))
	if int(question_id)==Answer.objects.all().filter(question_id=int(question_id)).first().id:
		return sel_ans==Answer.objects.all().filter(question_id=question_id).first().corr_answer
	# for answer_ in Answer.objects.all():
	# 	answers_.append(answer_.question)
	# print(answers_)
	# for entry in answers_:
	# 	print(entry)
	# 	print(entry.question)
	# 	return sel_ans==entry.corr_answer
	# print(correct_answer)
	# if str(correct_answer) == question:
	# 	print("Ting")
	# print(correct_answer)
	# print(type(str(correct_answer)))
	# print(type(question))
	# return correct_answer==sel_ans 
# Create your views here.
@login_required
def quiz_home(request,username):
	quizes = Quiz.objects.all()
	return render(request,'quizapp/quiz_portal_home.html',{'quizes':quizes})
@login_required
def share_quiz_perfo(request,username,pk):
	quiz_atmpt = UserQuizResult.objects.all().filter(user=request.user,quiz_id=pk).first()
	# print(quiz_atmpt.user)
	if quiz_atmpt:
		context = {
			'title' : quiz_atmpt.quiz,
			'score' : quiz_atmpt.score,
			'max_score' : quiz_atmpt.quiz.max_score
		}
		return render(request,"quizapp/share_quiz_perfo.html",context)
	else:
		return HttpResponse("Please Attempt this quiz fisrt then you will be Automatically Redirected to this page!")


@login_required
def quiz_view(request,username,pk):
	if request.method=="GET" and request.GET.get('question_id') and request.GET.get('quiz'): # to handle Reset Button in each question
		question_id = request.GET.get('question_id')
		quiz = request.GET.get('quiz')
		# print(request.GET)
		question_=Question.objects.all().filter(id=question_id).first()#Question Object
		if is_atmt(request,question_id): # as is_atmt returns the id of the row(entry) of the attempt in CurrentQuiz Table
			# print("Attempted One")
			entry_id = is_atmt(request,question_id)
			CurrentQuiz.objects.get(id=entry_id).delete()
			data = {
					'SS':"Choice Reset Done!"
			}
			response = JsonResponse(data)
			return response


	if request.method=='POST': # To handle Submit Button in each question
		question_id = request.POST['question_id']
		sel_ans = request.POST['sel_ans']
		quiz = request.POST['quiz']
		# print(request.POST)
		question=Question.objects.all().filter(id=question_id).first().question
		quiz_ = Quiz.objects.all().filter(title=quiz).first() #Quiz Object
		question_=Question.objects.all().filter(id=question_id).first()#Question Object
		contrib = 0
		if is_atmt(request,question_id):
			# print("Attempted One")
			entry_id = is_atmt(request,question_id)
			if is_corrt(question_id,sel_ans):
				contrib = (quiz_.max_score)/(quiz_.no_of_ques)
			else:
				contrib = 0 - neg_marks
			entry = CurrentQuiz.objects.get(id=entry_id)
			entry.sel_ans = sel_ans
			entry.contrib=contrib
			entry.save()
		else:
			#Definitely Add new row
			# check is_atm for that question
			# print("None Attempted One") 
			if is_corrt(question_id,sel_ans):
				# print("Hello")
				contrib = (quiz_.max_score)/(quiz_.no_of_ques)
			else:
				# print("World")
				contrib = 0 - quiz_.neg_marks
			print(contrib)
			entry = CurrentQuiz.objects.create(
						user = request.user,
						contrib = contrib,
						quiz = quiz_,
						question = question_,
						sel_ans = sel_ans,
						is_atm = True,
					)
			entry.save()	
		data={ 'SS' :"Successfully Submitted."}
		'''SS:'''
		return JsonResponse(data)

	else:
		quiz = Quiz.objects.all().filter(id=pk).first()
		rows = UserQuizResult.objects.all().filter(quiz=quiz)
		for row in rows:
			if request.user==row.user:
				# messages.info(request, f"Sorry, You have Alredy Attempted this Quiz.");
				# return HttpResponseRedirect(reverse('quiz_home', kwargs={'username': request.user.username}));
				return HttpResponse("Sorry, You have Alredy Attempted this Quiz.")
		questions = Question.objects.all().filter(quiz=quiz) #return Query Set i.e. <QuerySet [<Question: Question object (1)>, <Question: Question object (2)>]>
		quiz_ques = RandomQuizQuestion.objects.all().filter(user=request.user).first()
		if not quiz_ques:
			questions_ = []
			for question_ in questions:
				questions_.append(question_)
			random.shuffle(questions_)
			for q in questions_: 
				RandomQuizQuestion.objects.create(
					user = request.user,
					quiz_ques_id  = q
				)
		random_questions = RandomQuizQuestion.objects.all().filter(user=request.user)
		options = Option.objects.all().filter(quiz=quiz) 
		# options_ = []
		# for que in random_questions:
		# 	for option_ in options:
		# 		if option_.question == que.quiz_ques_id:
		# 			options_.append(option_)
					# print(option_.question)
		# print(answers)
		# for random_question in random_questions:
			# print(random_question.quiz_ques_id)
		return render(request,'quizapp/take_quiz.html',{'quiz':quiz,'questions':random_questions,'options':options})
		'''
		Finally random_questions have are rows in which quiz_ques_id is a question and these questions are random. 
		options_ have option_ where option_.question are in sync with random questions
		'''


		'''
		Try of Random using Sessions.
		'''
		# if request.session.get('quiz_running') in request.session:
		# 	return render(request,'quizapp/take_quiz.html',{'quiz':quiz,'questions':request.session['quiz_running'],'options':options})
		# else:
		# 	questions_ = []
		# 	for question_ in questions:
		# 		questions_.append(question_)
		# 	random.shuffle(questions_)
		# 	# print(questions)
		# 	options = Option.objects.all().filter(quiz=quiz) 
			# answers = Answer.objects.all().filter(quiz=quiz)
			# for question in questions:
				# print(question.option1)
			# print(answers)
			# request.session['quiz_running'] = questions_
			# return render(request,'quizapp/take_quiz.html',{'quiz':quiz,'questions':request.session['quiz_running'],'options':options})


@login_required
def submitquizview(request,pk):
	# user,quiz,score created permanently for current user
	if request.method=="GET":
		# print(request.GET)
		user = request.user
		quiz = Quiz.objects.all().filter(id=pk).first()
		attempts = CurrentQuiz.objects.all().filter(user=user)
		summation = 0
		for attempt in attempts:
			summation += attempt.contrib
		entry = UserQuizResult.objects.create(
					user = user,
					quiz = quiz,
					score = summation,
					is_atm = True
				)
		entry.save()
		CurrentQuiz.objects.all().filter(user=request.user).delete()
		RandomQuizQuestion.objects.all().filter(user=request.user).delete()
		share_url = "/" + str(user.username) + "/quiz/" + str(pk) + "/share/"
		# profle_url = "/profile/" + str(request.user) + "/"
		# print(profle_url)
		data={ 'SS' :"Successfully Submitted the quiz.",
			   'hit': share_url }
		response = JsonResponse(data)
		# path = "/quiz/" + str(quiz.id)
		# print(path)
		# print(response.set_cookie('minutes',1, max_age=10*86400, path=path))
		# response.set_cookie('seconds',1, max_age=10*86400, path=path)
		# print("Cookie Set")
		return response
		# return HttpResponse("Your scored " + entry.score + " out of " + quiz.max_score)
	else:
		return HttpResponse("Badass Url!")

@login_required
@user_passes_test(is_admin,login_url="Index") #i.e. when is_admin is Fasle then goes to Index
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
			return redirect("create_questions")
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


@login_required
@user_passes_test(is_admin,login_url="Index") #i.e. when is_admin is Fasle then goes to Index
def create_questions(request):
	if request.method == 'POST':
		# print(request.POST)
		quiz = Quiz.objects.all().last()
		que_obj = Question.objects.create(
			quiz = quiz,
			question = request.POST['question']
		)
		opt_obj = Option.objects.create(
			quiz = quiz,
			question = Question.objects.all().last(),
			option1 = request.POST['option1'],
			option2 = request.POST['option2'],
			option3 = request.POST['option3'],
			option4 = request.POST['option4']
		)
		ans_obj = Answer.objects.create(
			quiz = quiz,
			question = Question.objects.all().last(),
			corr_answer = request.POST.get('corr_answer',False),#to handle multivalue dictionary error
			extra_info = request.POST['extra_info']	
		)
		# TO send back whatever we have created using JsonResponse
		# question = {'question':que_obj.question}
		data={
			'question' : que_obj.question,
			'que_cnt' : Question.objects.all().filter(quiz=quiz).count(),
			'ques_id' :  Question.objects.all().last().id
		}
		# return redirect(request.path_info)
		return JsonResponse(data)

	else:
		form_que = QuestionCreationForm()
		form_opt = OptionCreationForm()
		form_ans = AnswerCreationForm()
		quiz = Quiz.objects.all().last()
		questions = Question.objects.all().filter(quiz = quiz) # using quiz = quiz.title gives inavlid literal error.
		que_cnt = questions.count()
		return render(request,"quizapp/create_questions.html",{'quiz':quiz,'questions':questions,'form_que':form_que,
															'form_opt':form_opt,'form_ans':form_ans,'que_cnt':que_cnt})
''' THIS CODE WORKS PERFECTLY FINE BUT FOR AJAXIFYING Create Questions we don't use it.
	# if request.method == 'POST':
	# 	form_que = QuestionCreationForm(request.POST)
	# 	curr_quiz = Quiz.objects.all().last()
	# 	form_que.instance.quiz = curr_quiz
	# 	if form_que.is_valid():
	# 		form_que.save()
	# 	form_opt = OptionCreationForm(request.POST)
	# 	form_ans = AnswerCreationForm(request.POST)
	# 	form_opt.instance.quiz = curr_quiz
	# 	form_ans.instance.quiz = curr_quiz
	# 	curr_que = Question.objects.all().last()
	# 	form_opt.instance.question = curr_que 
	# 	form_ans.instance.question = curr_que 
	# 	print(request.POST)
	# 	form_ans.instance.corr_answer = request.POST['correct_one']
	# 	if form_opt.is_valid() and form_ans.is_valid():
	# 		form_opt.save()
	# 		form_ans.save()
	# 		return HttpResponse("Question Addded Successfully")
	# 	else:
	# 		if form_ans.errors:
	# 			for field in form_ans:
	# 				for error in field.errors:
	# 					print(error)
	# 		return HttpResponse("Question NOT Addded Successfully")
'''
def ques_detail_view(request,pk):
	if request.method == 'POST':
		question = Question.objects.all().filter(id=pk)
		question_res = serializers.serialize('json', question)
		options = Option.objects.all().filter(question=question.first())
		options_res = serializers.serialize('json', options)
		answer = Answer.objects.all().filter(question=question.first())
		answer_res = serializers.serialize('json', answer)
		data={
			'question' : question_res,
			'options' : options_res,
			'answer' : answer_res
		}

		# return HttpResponse(options_res, content_type="text/json-comment-filtered")
		'''
		e.g. [{"model": "quizapp.question", "pk": 115, "fields": {"quiz": 18, "question": "Question from Quiz 4"}}]
		'''
		return JsonResponse(data)
		# print(question)
		# options  = Option.objects.all().filter(question=)
		# return HttpResponse("Hola")