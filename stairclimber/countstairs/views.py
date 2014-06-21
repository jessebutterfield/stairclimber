from countstairs.models import DailyStairs, UserPreferences, CustomStairCount

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext

from datetime import date

# Create your views here.


@login_required(login_url='/accounts/login/')
def home(request):
	user = request.user
	day = date.today()
	dailyStairs,_ = DailyStairs.objects.get_or_create(day=day, climber=user)
	upDown = user.userpreferences.upDown
	customStairs = CustomStairCount.objects.filter(user=user).order_by('count')
	return render_to_response('countstairs/home.html', 
                              {'dailyStairs':dailyStairs,'user':user,'upDown':upDown, 'customStairCounts':customStairs},
                              context_instance=RequestContext(request))

@login_required(login_url='/accounts/login')
def addPreset(request, id):
	submit = request.POST.get('submit','total')
	if(submit == 'up'):
		direction = 'up'
	elif(submit == 'down'):
		direction = 'down'
	else:
		direction = 'total'
	stairCount = CustomStairCount.objects.get(id=id)
	stairCount.count += 1
	stairCount.save()
	return addStairs(request, direction, stairCount.steps)


@login_required(login_url='/accounts/login/')
def oneTimeAdd(request):
	submit = request.POST.get('submit','total')
	if(submit == 'up'):
		direction = 'up'
	elif(submit == 'down'):
		direction = 'down'
	else:
		direction = 'total'
	steps = int(request.POST["steps"])
	return addStairs(request, direction, steps)

def addStairs(request, direction, numStairs):
	user = request.user
	day = date.today()
	dailyStairs,_ = DailyStairs.objects.get_or_create(day=day, climber=user)
	dailyStairs.total += numStairs
	if(direction == 'up'):
		dailyStairs.up += numStairs
	if(direction == 'down'):
		dailyStars.down += numStairs
	dailyStairs.save()
	return HttpResponseRedirect(reverse('countstairs.views.home'))



