from django import forms
from heatmap import models
import operator
from django.contrib.sites.models import Site


def list_sort(a):
    b = []
    for i in a:
        b.append((i.split(":")[0].split("/")[0], i.split(":")[0].split("/")[1], i.split(":")[1].split("-")[0],int(i.split(":")[1].split("-")[1])))
    b.sort(key=operator.itemgetter(1, 0,2,3))
    del a[:]
    for t in b:
        a.append("{}/{}:{}-{}".format(t[0], t[1], t[2],t[3]))

#class FieldForm(forms.Form):
#    Field = forms.CharField(widget=forms.HiddenInput)

class UploadFileForm(forms.ModelForm):
     class Meta:
        model = models.UploadFile
        fields = '__all__'

class ChoiceForm(forms.Form):
    Frequencies = forms.ChoiceField(required=True,label='Frequency',
                                    widget=forms.Select(),
                                    #initial=('2412', '2412'),
                                    choices=[('2412', '2412'), ('5180', '5180')],
                                    )
    Rate = forms.ChoiceField(required=True,label='Rate',
                                    widget=forms.Select(),
                                    initial=('6', '6'),
                                    choices=[('1', '1'), ('6', '6'),('54', '54')],
                                    )
    Transmission_power = forms.ChoiceField(required=True,label='Transmission Power',
                             widget=forms.Select(),
                             initial=('14', '14'),
                             choices=[('5', '5'), ('9', '9'),('14', '14')],
                             )
class ChoiceforHeatmap(forms.Form):

    def __init__(self,*args,**kwargs):
        days = []
        print(args[1]['Frequencies'])
        print(args[1]['Rate'])
        if len(args) > 0:
            if int(args[1]['Frequencies']) == 5180:
                outcome = models.Input.objects.values_list('Timestamp').filter(frequency=args[1]['Frequencies'],rate=args[1]['Rate'],transmission_power=args[1]['Transmission_power'])
                print("We are inside 5180")
            else:
                outcome = models.Input.objects.values_list('Timestamp').filter(frequency=args[1]['Frequencies'],rate=args[1]['Rate'],transmission_power=args[1]['Transmission_power'])
                print("We are inside 2412")
        #else:
            #outcome = models.Input.objects.values_list('Timestamp').filter(frequency=2412,rate=args[2],transmission_power=args[3])
        for d in outcome:
            days.append(d[0])
        a = list(set(days))
        list_sort(a)
        super(ChoiceforHeatmap, self).__init__(*args, **kwargs)
        if len(a)==0:
            self.fields['Day'].initial ='No days are available for the given selection'
        self.fields['Day'].choices = [(i, i) for i in a]
        #self.fields['Frequencies'].choices = [('2412', '2412'), ('5180', '5180')]
        #self.fields['Frequencies'].initial = args[1]
        #self.fields['Rate'].choices = [('1', '1'), ('6', '6'),('54', '54')]
        #self.fields['Rate'].initial = args[2]
        #self.fields['Transmission_power'].initial = args[3]
        #self.fields['Transmission_power'].choices = [('5', '5'), ('9', '9'),('14', '14')]
        #self.initial['Frenquencies'] = args[1]
        #self.initial['Rate'] = args[2]
        #self.initial['Transmission_power'] = args[3]



    Frequencies = forms.ChoiceField(required=False, label='Frequency', widget=forms.Select(attrs={"onChange": 'refresh()'}),initial=('2412','2412'),
                                            choices=[('2412', '2412'), ('5180', '5180')],
                                            )
    Rate = forms.ChoiceField(required=False,label='Rate',
                             widget=forms.Select(attrs={"onChange": 'refresh()'}),
                             #initial=('6', '6'),
                             choices=[('1', '1'), ('6', '6'),('54', '54')],
                             )
    Transmission_power = forms.ChoiceField(required=False,label='Transmission Power',
                                           widget=forms.Select(attrs={"onChange": 'refresh()'}),
                                           #initial=('14', '14'),
                                           choices=[('5', '5'), ('9', '9'),('14', '14')],
                                           )
    Antenna = forms.ChoiceField(required=False,label='Antenna Used',
                                           widget=forms.Select(),
                                           initial=('all', 'all'),
                                           choices=[('all', 'all'), ('0', '0'), ('1', '1'), ('2', '2')],
                                           )
    Day = forms.MultipleChoiceField(required=True,widget=forms.CheckboxSelectMultiple,choices=[],label='TimeStamp')

    Node = forms.ChoiceField(choices=((i,i) for i in range(1,38)),required=False, widget=forms.Select(), initial=1,label='Node Sender')

class ChoiceNode(forms.Form):
    Node_sender=forms.ChoiceField(choices=((i,i) for i in range(1,38)),required=True,initial=(1,1), widget=forms.Select())
    Node_receiver=forms.ChoiceField(choices=((i,i) for i in range(1,38)),required=True,initial=(2,2), widget=forms.Select())
    Rate = forms.ChoiceField(required=True,
                             widget=forms.Select(),
                             initial=('6', '6'),
                             choices=[('1', '1'), ('6', '6'), ('54', '54')],
                             )
    Transmission_power = forms.ChoiceField(required=True,
                                           widget=forms.Select(),
                                           initial=('14', '14'),
                                           choices=[('5', '5'), ('9', '9'), ('14', '14')],
                                           )
class Fit(forms.Form):
    def __init__(self,*args,**kwargs):
        days = []
        if len(args)>0:
            if int(args[1]['Frequencies'])==5180:
                outcome = models.Input.objects.values_list('Timestamp').filter(frequency=args[1]['Frequencies'],rate=args[1]['Rate'],transmission_power=args[1]['Transmission_power'])
                print("We are inside 5180")
            else:
                outcome = models.Input.objects.values_list('Timestamp').filter(frequency=args[1]['Frequencies'],rate=args[1]['Rate'],transmission_power=args[1]['Transmission_power'])
                print("We are inside 2412")
        #else:
        #    outcome = models.Input.objects.values_list('Timestamp').filter(frequency=2412)
        for d in outcome:
            days.append(d[0])
        a = list(set(days))
        list_sort(a)
        super(Fit,self).__init__(*args,**kwargs)
        self.fields['Day'].choices = [(i,i) for i in a ]

    Frequencies = forms.ChoiceField(required=False,
                                            widget=forms.Select(attrs={"onChange": 'refresh()'}),
                                            initial=('2412', '2412'),
                                            choices=[('2412', '2412'), ('5180', '5180')],
                                            )
    Day = forms.MultipleChoiceField(required=True ,widget=forms.CheckboxSelectMultiple,
                                    choices=[],
                                    )
    Rate = forms.ChoiceField(required=False, label='Rate',
                             widget=forms.Select(attrs={"onChange": 'refresh()'}),
                             # initial=('6', '6'),
                             choices=[('1', '1'), ('6', '6'), ('54', '54')],
                             )
    Transmission_power = forms.ChoiceField(required=False, label='Transmission Power',
                                           widget=forms.Select(attrs={"onChange": 'refresh()'}),
                                           # initial=('14', '14'),
                                           choices=[('5', '5'), ('9', '9'), ('14', '14')],
                                           )
    Antenna = forms.ChoiceField(required=False, label='Antenna Used',
                                widget=forms.Select(),
                                initial=('all', 'all'),
                                choices=[('all', 'all'), ('0', '0'), ('1', '1'), ('2', '2')],
                                )