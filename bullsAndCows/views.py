from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from bullsAndCows.forms import BullsCowsForm

from itertools import product
from random import shuffle

digits = '0123456789'
size = 4

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    offset = int(offset)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def bulls_cows(request):
        
    if request.method == 'POST':
        form = BullsCowsForm(request.POST)
        score = (int(request.POST['bulls']), int(request.POST['cows'])) 
        request.session["scores"].append(score)
        request.session["history"].append({'ans': request.session["ans"], 'score': score})
        choices = request.session["choices"] 
        if len(choices) > 0:       
            choices = [c for c in choices if highestPointers(c, request.session["ans"]) == score]            
            request.session["choices"] = choices
            shuffle(request.session["choices"])
        if len(choices) > 0:
            request.session["ans"] = choices[0]
            for choice in choices:
                if len(set(choice)) == 4:
                    request.session["ans"] = choice
                    break
            request.session["answers"].append(request.session["ans"])
        found = score == (size, 0)
        if(len(choices)) == 1 and not found:
            request.session["history"].append({'ans': request.session["ans"], 'score': (4,0)})            
            found = True
        error = False
        if len(choices) == 0:
            error = True
        csrfContext = RequestContext(request, {'form': form, 
            'ans': request.session["ans"],
            'history': request.session["history"],
            'found': found,
            'error': error})
        return render(request, "bulls_cows.html", csrfContext.flatten())
    else:        
        form = BullsCowsForm()
        request.session["choices"] = list(product(digits, repeat=size))
        shuffle(request.session["choices"])
        request.session["answers"] = []
        request.session["scores"]  = []
        request.session["history"]  = []
        request.session["ans"] = request.session["choices"][0]  
        for choice in request.session["choices"]:
            if len(set(choice)) == 4:
                request.session["ans"] = choice
                break      
        request.session["answers"].append(request.session["ans"])        
        csrfContext = RequestContext(request, {'form': form, 'ans': request.session["ans"]})
        return render(request, 'bulls_cows.html', csrfContext.flatten())
    
def highestPointers(possibility, guess):
    flag = False
    b = c = 0
    g_z = []
    p_z = []
    for p,g in zip(possibility, guess):
        if p == g:
            b += 1
        else:
            g_z.append(g)
            p_z.append(p)
    c = cows_(g_z, p_z)    
    return (b,c)    

def cows_(a, b):
    c = 0
    a_app = {}
    for i in a:
        if not i in a_app:
            a_app[i] = 0
        a_app[i] += 1
    for i in b:
        if i in a_app and a_app[i] > 0:
            a_app[i] -= 1
            c += 1
    return c 