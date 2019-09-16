from django import forms
from .models import Quiz,Question,Option,Answer

class QuizCreationForm(forms.ModelForm):
	class Meta:
		model = Quiz
		fields = ['title','no_of_ques','time_lim']
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
	# 1 Other required Field needs to be updated in the view: quiz
class OptionCreationForm(forms.ModelForm):
	class Meta:
		model = Option
		fields = ['option1','option2','option3','option4']
	# 2 Other required Fields need to be updated in the view: quiz,question
class AnswerCreationForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['corr_answer','extra_info']
	# 2 Other required Fields need to be updated in the view: quiz,question