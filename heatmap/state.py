#In this script i will just query the database and get last value of rss for each node.
#We can also run some algorithm that gives back a report about best value got, worst etc..

#return a list from here, and from the view send elements of the list

from heatmap import models
import operator
def list_sort(a):
    b = []
    for i in a:
        b.append((i.split(":")[0].split("/")[0], i.split(":")[0].split("/")[1],int(i.split(":")[1].split('-')[0]),int(i.split(":")[1].split('-')[1])))
    b.sort(key=operator.itemgetter(1, 0,2,3))
    del a[:]
    for t in b:
        a.append("{}/{}:{}-{}".format(t[0], t[1], t[2],t[3]))
def show():
    rss2=[]
    rss5=[]
    days2 = []
    days5 = []
    outcome2 = models.Input.objects.values_list('Timestamp').filter(frequency=2412,rate=6,transmission_power=14)
    outcome5 = models.Input.objects.values_list('Timestamp').filter(frequency=5180,rate=6,transmission_power=14)
    for d in outcome2:
        days2.append(d[0])
    a2 = list(set(days2))
    list_sort(a2)
    for d in outcome5:
        days5.append(d[0])
    a5 = list(set(days5))
    list_sort(a5)
    raw2 = models.Input.objects.values_list('Rss_mrc').filter(Timestamp=a2[-1],
                                                         frequency=2412,rate=6,transmission_power=14)
    raw5 = models.Input.objects.values_list('Rss_mrc').filter(Timestamp=a5[-1],
                                                         frequency=5180,rate=6,transmission_power=14)
    for i in raw2:
            rss2.append(float(i[0]))
    for i in raw5:
            rss5.append(float(i[0]))
    v21="In 2ghz Node sender {} Node receiver {} it received {}".format(best(rss2)[0],best(rss2)[1],best(rss2)[2])
    v51= "In 5ghz Node sender {} Node receiver {} it received {}".format(best(rss5)[0],best(rss5)[1],best(rss5)[2])
    v22="In 2ghz Node sender {} Node receiver {} it received {} ".format(worst(rss2)[0], worst(rss2)[1],worst(rss2)[2])
    v52="In 5ghz Node sender {} Node receiver {} it received {} ".format(worst(rss5)[0], worst(rss5)[1],worst(rss5)[2])
    v3=""
    v4=""
    if prob(2,[a2[-3],a2[-2],a2[-1]])[0]:
        v3="There is a problem with node {} it received {} among the 3 last days from respectively {}".format(prob(2,[a2[-3],a2[-2],a2[-1]])[1],prob(2,[a2[-3],a2[-2],a2[-1]])[2],prob(2,[a2[-3],a2[-2],a2[-1]])[3])
    if prob(5,[a5[-3],a5[-2],a5[-1]])[0]:
        v4="There is a problem with node {} it received {} among the 3 last days from respectively {}".format(prob(5,[a5[-3],a5[-2],a5[-1]])[1],prob(5,[a5[-3],a5[-2],a5[-1]])[2],prob(5,[a5[-3],a5[-2],a5[-1]])[3])
    #return [v21,v51,v22,v52,v3,v4]
    return [[v21, v51],[v22, v52],[v3, v4]]

def prob(t,e):
    if t==2:
        bad=[]
        sender=[]
        received = []
        for i in e:
            rss=[]
            raw = models.Input.objects.values_list('Rss_mrc').filter(Timestamp=i,
                                                          frequency=2412,rate=6,transmission_power=14)
            for i in raw:
                rss.append(float(i[0]))
            received.append(worst(rss)[2])   # worst value of rss
            bad.append(worst(rss)[1])   # the node having a problem
            sender.append(worst(rss)[0])  # the senders to this node
        if len(list(set(bad)))==1:
            return [True,list(set(bad))[0],received,sender]
        else:
            return [False]
    elif t == 5:
        bad = []
        sender = []
        received = []
        for i in e:
            rss = []
            raw = models.Input.objects.values_list('Rss_mrc').filter(Timestamp=i,
                                                                  frequency=5180,rate=6,transmission_power=14)
            for i in raw:
                rss.append(float(i[0]))
            received.append(worst(rss)[2])  # worst value of rss
            bad.append(worst(rss)[1])  # the node having a problem
            sender.append(worst(rss)[0])  # the senders to this node
        if len(list(set(bad))) == 1:
            return [True, list(set(bad))[0], received, sender]
        else:
            return [False]
    return [False]


def worst(list):
    k=list.index(sorted(list)[0])   # find a way to get rid of the -100
    i=int(k/37)+1
    j=k-37*(i-1)+1
    return [i,j,sorted(list)[0]]
def best(list):
    k = list.index(sorted(list)[-38])
    i = int(k / 37) + 1
    j = k - 37 * (i - 1) + 1
    return [i, j,sorted(list)[-38]]
def last_rss():
    days2=[]
    rss2=[]
    average=[]
    outcome2 = models.Input.objects.values_list('Timestamp').filter(frequency=2412,rate=6,transmission_power=14)
    for d in outcome2:
        days2.append(d[0])
    a2 = list(set(days2))
    list_sort(a2)
    for n in range(1,38):
        raw2 = models.Input.objects.values_list('Rss_mrc').filter(Timestamp=a2[-1],
                                                          frequency=2412,node_receiver=n,rate=6,transmission_power=14)
        for i in raw2:
            rss2.append(float(i[0]))
        del rss2[n-1]
        average.append(sum(rss2)/len(rss2))
    #print(average)
    return average
