from django import forms

from . import models
import operator


def list_sort(a):
    b = []
    for i in a:
        b.append((i.split(":")[0].split("/")[0], i.split(":")[0].split("/")[1], i.split(":")[1]))
    b.sort(key=operator.itemgetter(1, 0))
    del a[:]
    for t in b:
        a.append("{}/{}:{}".format(t[0], t[1], t[2]))

class UploadFileForm(forms.ModelForm):
     class Meta:
        model = models.UploadFile
        fields = '__all__'

class ChoiceForm(forms.Form):
    Frequencies = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
        choices=[('2412','2412'),('5180','5180')],
         )
class ChoiceforHeatmap(forms.Form):
    def __init__(self,*args,**kwargs):
        print("Show function")
        days = []
        outcome = models.Input.objects.values_list('Timestamp')
        for d in outcome:
            days.append(d[0])
        a = list(set(days))
        list_sort(a)
        super(ChoiceforHeatmap,self).__init__(*args,**kwargs)
        self.fields['Day'].choices = [(i,i) for i in a ]

    Frequencies = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                            choices=[('2412', '2412'), ('5180', '5180')],
                                            )

    Day = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],)#required=False, widget=forms.CheckboxSelectMultiple,
                                            #choices=[(i,i) for i in a ],

    Node = forms.ChoiceField(choices=((i,i) for i in range(1,38)),required=False, widget=forms.Select(), initial=1)

class ChoiceNode(forms.Form):
    Node_sender=forms.ChoiceField(choices=((i,i) for i in range(1,38)),required=False, widget=forms.Select(), initial=1)
    Node_receiver=forms.ChoiceField(choices=((i,i) for i in range(1,38)),required=False, widget=forms.Select(), initial=2)

class Fit(forms.Form):
    days = []
    outcome = models.Input.objects.values_list('Timestamp')
    for d in outcome:
        days.append(d[0])
    a = list(set(days))
    list_sort(a)
    Frequencies = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                            choices=[('2412', '2412'), ('5180', '5180')],
                                            )

    Day = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                    choices=[(i, i) for i in a],
                                    )