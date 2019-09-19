from django import forms
from .models import Quiz,Question,Option,Answer

class QuizCreationForm(forms.ModelForm):
	class Meta:
		model = Quiz
		fields = ['title','no_of_ques','time_lim','max_score','neg_marks']
		# Experiment: Using Html tag TextArea itself for istructions
		# IMP: fields should not contain author as it will be updated in Views itself
	# 1 Other required Field needs to be updated in the view: author
	widgets = {'title':forms.TextInput(
									attrs={'id':"title" ,'type':"text" ,
									'class':"validate" ,
									'requred':True}),
				'no_of_ques':forms.TextInput(attrs={'id':"no_of_ques",
											'type':"text",'class':"validate",
											'required':True}),
				'time_lim':forms.TextInput(attrs={'id':"time_lim",
											'type':"text",'class':"validate",
											'required':True}),
				
			}
class QuestionCreationForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['question']
		widgets={
				'question':forms.TextInput(
									attrs={'id':"id_question" ,'type':"text" ,
									'class':"validate" ,
									'requred':True}),
		}
	# 1 Other required Field needs to be updated in the view: quiz
class OptionCreationForm(forms.ModelForm):
	class Meta:
		model = Option
		fields = ['option1','option2','option3','option4']
		widgets={
				'option1':forms.TextInput(
									attrs={'id':"id_option1" ,'type':"text" ,
									'class':"validate" ,
									'requred':True}),
				'option2':forms.TextInput(
									attrs={'id':"id_option2" ,'type':"text" ,
									'class':"validate" ,
									'requred':True}),
				'option3':forms.TextInput(
									attrs={'id':"id_option3" ,'type':"text" ,
									'class':"validate" ,
									'requred':True}),
				'option4':forms.TextInput(
									attrs={'id':"id_option4" ,'type':"text" ,
									'class':"validate" ,
									'requred':True}),

		}
	# 2 Other required Fields need to be updated in the view: quiz,question
class AnswerCreationForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['extra_info']
		widgets={
				'extra_info':forms.TextInput(
									attrs={'id':"id_extra_info" ,'type':"text" ,
									'class':"validate",'placeholder':"Add Extra Info...",
									'requred':True}),
		}
	# 3 Other required Fields need to be updated in the view: quiz,question,corr_ans
		# corr_ans also because it is easier to send then via POST using name attribute
		# and then access in request.POST dictionary.