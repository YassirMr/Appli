from django import forms
from heatmap import models
import operator
from django.contrib.sites.models import Site


def list_sort(a):
    b = []
    for i in a:
        b.append((i.split(":")[0].split("/")[0], i.split(":")[0].split("/")[1], i.split(":")[1]))
    b.sort(key=operator.itemgetter(1, 0))
    del a[:]
    for t in b:
        a.append("{}/{}:{}".format(t[0], t[1], t[2]))

#class FieldForm(forms.Form):
#    Field = forms.CharField(widget=forms.HiddenInput)

class UploadFileForm(forms.ModelForm):
     class Meta:
        model = models.UploadFile
        fields = '__all__'

class ChoiceForm(forms.Form):
    Frequencies = forms.ChoiceField(required=True,
                                    widget=forms.Select(),
                                    #initial=('2412', '2412'),
                                    choices=[('2412', '2412'), ('5180', '5180')],
                                    )
class ChoiceforHeatmap(forms.Form):
    def __init__(self,*args,**kwargs):
        days = []
        if len(args) > 0:
            if int(args[1]) == 5180:
                outcome = models.Input.objects.values_list('Timestamp').filter(frequency=5180)
                print("We are inside 5180")
            else:
                outcome = models.Input.objects.values_list('Timestamp').filter(frequency=2412)
                print("We are inside 2412")
        else:
            outcome = models.Input.objects.values_list('Timestamp').filter(frequency=2412)
        for d in outcome:
            days.append(d[0])
        a = list(set(days))
        list_sort(a)
        super(ChoiceforHeatmap, self).__init__(*args, **kwargs)
        self.fields['Day'].choices = [(i, i) for i in a]


    Frequencies = forms.ChoiceField(required=True, widget=forms.Select(attrs={"onChange": 'refresh()'}),initial=('2412','2412'),
                                            choices=[('2412', '2412'), ('5180', '5180')],
                                            )

    Day = forms.MultipleChoiceField(required=True,widget=forms.CheckboxSelectMultiple,choices=[],)

    Node = forms.ChoiceField(choices=((i,i) for i in range(1,38)),required=True, widget=forms.Select(), initial=1)

class ChoiceNode(forms.Form):
    Node_sender=forms.ChoiceField(choices=((i,i) for i in range(1,38)),required=True,initial=(1,1), widget=forms.Select())
    Node_receiver=forms.ChoiceField(choices=((i,i) for i in range(1,38)),required=True,initial=(2,2), widget=forms.Select())

class Fit(forms.Form):
    def __init__(self,*args,**kwargs):
        days = []
        if len(args)>0:
            if int(args[1])==5180:
                outcome = models.Input.objects.values_list('Timestamp').filter(frequency=5180)
                print("We are inside 5180")
            else:
                outcome = models.Input.objects.values_list('Timestamp').filter(frequency=2412)
                print("We are inside 2412")
        else:
            outcome = models.Input.objects.values_list('Timestamp').filter(frequency=2412)
        for d in outcome:
            days.append(d[0])
        a = list(set(days))
        list_sort(a)
        super(Fit,self).__init__(*args,**kwargs)
        self.fields['Day'].choices = [(i,i) for i in a ]

    Frequencies = forms.ChoiceField(required=True,
                                            widget=forms.Select(attrs={"onChange": 'refresh()'}),
                                            initial=('2412', '2412'),
                                            choices=[('2412', '2412'), ('5180', '5180')],
                                            )
    Day = forms.MultipleChoiceField(required=True ,widget=forms.CheckboxSelectMultiple,
                                    choices=[],
                                    )