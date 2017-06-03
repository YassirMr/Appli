from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader
import datetime
from django.http import HttpResponseRedirect
from . import forms
from . import models
from django.contrib import messages
from . import heatmap
from . import represent_node
from . import fit_lab
import operator



def index(request):
        form = forms.ChoiceForm(request.POST)
        data = {'form': form}

        return render(request, 'heatmap/index.html', data)


def importer(request):
        print("beginning")
        if request.method == 'POST':
                print("inside post")
                form = forms.UploadFileForm(request.POST, request.FILES)
                form2 = forms.ChoiceForm(request.POST)
                if (form.is_valid() and form2.is_valid()):
                        new_file = models.UploadFile(file=request.FILES['file'])
                        new_file.save()
                        b = request.POST.get('Frequencies')
                        datasave(request.FILES['file'], b)
                        return HttpResponseRedirect(reverse('heatmap:index'))
                else:
                        messages.info(request, 'Thank you!')
                        return HttpResponseRedirect(reverse('heatmap:index'))

        else:
                print("inside else")
                form = forms.UploadFileForm()
                form2 = forms.ChoiceForm()

                data = {'form': form , "form2":form2 }
                print("end")
                return render(request,'heatmap/import.html', data)

def datasave(file,f):
        t=0
        a=[]
        now = datetime.datetime.now()
        day = "{}/{}:{}".format(now.day, now.month, now.hour)
        received_power=[]
        for line in file:
                received_power.append(line.decode('utf-8').split()[2])
        for y in range(1,38):
                for z in range(1,38):
                        a.append(models.Input(Timestamp=day,node_sender=y,node_receiver=z,frequency=f,rate=6,transmission_power=14,Rss=str(received_power[t])))
                        t+=1
        models.Input.objects.bulk_create(a)

def show(request):
        form = forms.ChoiceforHeatmap(request.POST)
        data = {'form': form }
        if request.method == 'POST':
                if form.is_valid():
                        data = {'form': form}
                        heatmap.draw(request.POST.get('Frequencies'),request.POST.get('Day'),request.POST.get('Node'))
                        return HttpResponseRedirect(reverse('heatmap:show'))


        return render(request, 'heatmap/show.html', data)

def list_sort(a):
    b = []
    for i in a:
        b.append((i.split(":")[0].split("/")[0], i.split(":")[0].split("/")[1], i.split(":")[1]))
    b.sort(key=operator.itemgetter(1, 0))
    del a[:]
    for t in b:
        a.append("{}/{}:{}".format(t[0], t[1], t[2]))
def node(request):
        days = []
        outcome = models.Input.objects.values_list('Timestamp')
        for d in outcome:
                days.append(d[0])
        a = list(set(days))
        list_sort(a)
        form = forms.ChoiceNode(request.POST)
        data = {'form': form}
        if request.method == 'POST':
                if form.is_valid():
                        data = {'form': form}
                        represent_node.draw(request.POST.get('Node_sender'), request.POST.get('Node_receiver'), a).show()
                        return HttpResponseRedirect(reverse('heatmap:node'))
                else:
                        return HttpResponseRedirect(reverse('heatmap:node'))
        else:
                return render(request, 'heatmap/node.html', data)

def fit(request):
        form = forms.Fit(request.POST)
        data = {'form': form}
        #get the days here ?
        if request.method == 'POST':
                if form.is_valid():
                        #data = {'form': form}
                        fit_lab.draw(request.POST.get('Frequencies'), request.POST.get('Day'))  #
                        messages.info(request, 'voila')
                        return HttpResponseRedirect(reverse('heatmap:fit'))


        return render(request, 'heatmap/fit.html', data)





