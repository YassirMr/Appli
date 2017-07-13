from django.core.urlresolvers import reverse
from django.shortcuts import render
import datetime
from django.http import HttpResponseRedirect
from heatmap import forms
from heatmap import models
from django.contrib import messages
from heatmap import heatmap
from heatmap import represent_node
from heatmap import fit_lab
from heatmap import state

def index(request):
        if request.method == 'POST':
                list = state.show()
                #data = {'v21':list[0],'v51':list[1],'v22':list[2],'v52':list[3],'v3':list[4],'v4':list[5]}
                average = state.last_rss()
                data = {'v1': list[0],'v2': list[1], 'v3': list[2],'average':average}
                return render(request, 'heatmap/index.html', data)
        return render(request, 'heatmap/index.html')


def importer(request):
        print("beginning")
        if request.method == 'POST':
                print("inside post")
                form = forms.UploadFileForm(request.POST, request.FILES)
                #form2 = forms.ChoiceForm(request.POST)
                if form.is_valid():
                        #new_file = models.UploadFile(file=request.FILES['file'])
                        #new_file.save() no need to save the file it's gonna be redundant information..
                        b = request.POST.get('Frequencies')
                        datasave(request.FILES['file'], b)
                        return HttpResponseRedirect(reverse('heatmap:index'))
                else:
                        if not (request.POST.get('Frequencies') is None):
                                messages.info(request, 'Thank you!')
                                return HttpResponseRedirect(reverse('heatmap:index'))
                        return HttpResponseRedirect(reverse('heatmap:importer'))
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
        form = forms.ChoiceForm()
        if 'Frequencies' in request.session:
                if int(request.session['Frequencies']) == 2412:
                        form.fields['Frequencies'].initial = 5180
                else:
                        form.fields['Frequencies'].initial = 2412
        data = {'form': form, 'msg': ''}
        if request.method == 'POST':
                form = forms.ChoiceforHeatmap(request.POST, request.POST.get('Frequencies'))
                request.session['Frequencies'] = request.POST.get('Frequencies')
                if form.is_valid():
                        data = {'form': form}
                        heatmap.draw(request.POST.get('Frequencies'), request.POST.getlist('Day'), request.POST.get('Node'))
                        # request.POST.getlist('Day') this way to get the list !
                        return render(request, 'heatmap/show.html', data)

                else:
                        form = forms.ChoiceforHeatmap(request.POST, request.POST.get('Frequencies'))
                        data = {'form': form, 'msg': "Then select a day, a node and submit"}
                return render(request, 'heatmap/show.html', data)

        return render(request, 'heatmap/show.html', data)

def node(request):
        if request.method == 'POST':
                form = forms.ChoiceNode(request.POST)
                if form.is_valid():
                        obj= represent_node.draw(request.POST.get('Node_sender'), request.POST.get('Node_receiver'))
                        c = obj[0]
                        d = obj[1]
                        represent_node.plt.close()
                        messages.success(request, "sucess", extra_tags="1")
                        data = {'form': form, 'c': c, 'd':d}
                        return render(request, 'heatmap/node.html', data)
        else:
                form = forms.ChoiceNode()
                data = {'form': form}
        return render(request, 'heatmap/node.html', data)

def fit(request):
        form = forms.ChoiceForm()
        if 'Frequencies' in request.session:
                if int(request.session['Frequencies'])==2412:
                        form.fields['Frequencies'].initial = 5180
                else:
                        form.fields['Frequencies'].initial = 2412
        data = {'form': form, 'msg':''}
        if request.method == 'POST':
                if len(messages.get_messages(request)._loaded_messages) > 0:   #way too much of control in here..
                        storage = messages.get_messages(request)
                        del storage._loaded_messages[0]
                form = forms.Fit(request.POST, request.POST.get('Frequencies'))
                request.session['Frequencies']=request.POST.get('Frequencies')
                if form.is_valid():
                        print("Form is valid")
                        obj = fit_lab.draw(request.POST.get('Frequencies'), request.POST.get('Day'))
                        fit_lab.plt.close()
                        c = obj[0]
                        d = obj[1]
                        messages.success(request, "sucess", extra_tags="2")
                        data = {'form': form, 'c': c, 'd': d}
                        return render(request, 'heatmap/fit.html', data)
                else:

                        form = forms.Fit(request.POST,request.POST.get('Frequencies'))
                        data = {'form': form, 'msg':"Then select a day and submit"}
                return render(request, 'heatmap/fit.html', data)

        if  len(messages.get_messages(request)._loaded_messages)>0:
                storage = messages.get_messages(request)
                del storage._loaded_messages[0]
        return render(request, 'heatmap/fit.html', data)




def forfit(request): #for testing purposes
        return HttpResponseRedirect(reverse('heatmap:index'))

