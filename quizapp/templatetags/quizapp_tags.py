from django import template
register = template.Library()
from ..models import Quiz,Question,Answer,Option,Quiz,CurrentQuiz
from django.contrib.auth.models import Group #for has_group filter

@register.simple_tag
def get_options(question):
	ops = Option.objects.all().filter(question=question.quiz_ques_id).first()
	o=[]
	o.append(ops.option1)
	o.append(ops.option2)
	if(ops.option3 and ops.option4):
		o.append(ops.option3)
		o.append(ops.option4)
	return o

@register.simple_tag
def get_ans(question):
	a = Answer.objects.all().filter(question=question).first()
	return a.corr_answer

@register.simple_tag
def chk_atmp(question,user):
	a = CurrentQuiz.objects.all().filter(question=question.quiz_ques_id,user=user).first()
	if a:
		return int(a.sel_ans)
	else:
		return False
@register.filter
def times(count):
	return range(int(count))
	
@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


