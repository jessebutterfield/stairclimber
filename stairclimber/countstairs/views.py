from countstairs.models import DailyStairs, UserPreferences, CustomStairCount

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader, RequestContext

from datetime import datetime,date,timedelta

import calendar

# Create your views here.

mnames = "January February March April May June July August September October November December"
mnames = mnames.split()

@login_required(login_url='/accounts/login/')
def home(request):
	user = request.user
	day = date.today()
	dailyStairs,_ = DailyStairs.objects.get_or_create(day=day, climber=user)
	upDown = user.userpreferences.upDown
	customStairs = CustomStairCount.objects.filter(user=user).order_by('-count')
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

@login_required(login_url='/accounts/login/')
def editCustomSettings(request):
	user = request.user
	customStairs = CustomStairCount.objects.filter(user=user).order_by('-count')
	return render_to_response('countstairs/editCustom.html', 
							  {'user':user, 'customStairCounts':customStairs},
							  context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')
def newPreset(request, id):
	user = request.user
	steps = int(request.POST["steps"])
	name = request.POST["label"]
	if(int(id) == 0):
		stairCount = CustomStairCount.objects.create(user=user, steps=steps, name=name)
	else:
		stairCount = CustomStairCount.objects.get(id=id)
		stairCount.name = name
		stairCount.steps = steps
	stairCount.save()
	return HttpResponseRedirect(reverse('countstairs.views.editCustomSettings'))

def newMonth(request, year, month, change):
	year, month = int(year), int(month)
	if change in ("next", "prev"):
		d, mdelta = date(year, month, 15), timedelta(days=31)
		if change == "next":   
			d += mdelta
		elif change == "prev": 
			d -= mdelta
		year, month = d.timetuple()[0:2]
	return HttpResponseRedirect(reverse('countstairs.views.month', args=(year,month)))
   
def currentMonth(request):
	year, month = date.today().timetuple()[0:2]
	return HttpResponseRedirect(reverse('countstairs.views.month', args=(year,month)))

@login_required(login_url='/accounts/login/')	
def month(request, year, month):
	user = request.user
	"""Listing of days in `month`."""
	year, month = int(year), int(month)


	# init variables
	cal = calendar.Calendar()
	cal.setfirstweekday(6)
	month_days = cal.itermonthdays(year, month)
	lst = [[]]
	week = 0

	# make month lists containing list of days for each week
	# each day tuple will contain list of entries and 'current' indicator
	today = datetime.now()
	for day in month_days:
		steps = current = False   # are there entries for this day; current day?
		if day:
			#TODO: fix this to a get and a try 
			n = date(year,month,day)
			steps,_ = DailyStairs.objects.get_or_create(day=n, climber=user)
			if(today.year == year and today.month == month and today.day == day):
				current = True

		lst[week].append((day, steps, current))
		if len(lst[week]) == 7:
			lst.append([])
			week += 1

	return render_to_response("countstairs/month.html", dict(year=year, month=month, user=request.user,
						month_days=lst, mname=mnames[month-1]))





