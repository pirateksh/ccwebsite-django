from django import template
register = template.Library()
from ..models import Question,Answer,Option,Quiz

@register.simple_tag
def get_options(question):
	ops = Option.objects.all().filter(question=question).first()
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
@register.filter
def times(count):
	return range(int(count))

