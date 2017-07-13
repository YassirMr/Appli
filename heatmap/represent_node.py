import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from heatmap import models
from django.conf import settings
import operator

def list_sort(a):
    b = []
    for i in a:
        b.append((i.split(":")[0].split("/")[0], i.split(":")[0].split("/")[1], i.split(":")[1]))
    b.sort(key=operator.itemgetter(1, 0))
    del a[:]
    for t in b:
        a.append("{}/{}:{}".format(t[0], t[1], t[2]))
def draw(n_s,n_r):
    days = []
    outcome = models.Input.objects.values_list('Timestamp')
    for d in outcome:
        days.append(d[0])
    a = list(set(days))
    list_sort(a)
    rss2 = []
    rss5 = []
    for i in a:
        raw= models.Input.objects.values_list('Rss').filter(Timestamp=i,node_sender=n_s,node_receiver=n_r,frequency=2412)
        for i in raw:
            rss2.append(float(i[0]))
    #print("Rssi received in 2ghz")
    #print(rss2)
    b = range(1, len(rss2) + 1)
    my_xticks = []
    for i in a:
        my_xticks.append(i)
    plt.xticks(b, my_xticks,fontsize= 8)
    plt.plot(b, rss2, 'r', linewidth=2.0, label="2ghz")
    plt.title('Node {} => Node {} '.format(n_s, n_r))
    plt.xlabel('Time format D/M:H')
    plt.ylabel('Received power (dBm)')

    for i in a:
        raw = models.Input.objects.values_list('Rss').filter(Timestamp=i, node_sender=n_s, node_receiver=n_r,
                                                             frequency=5180)
        for i in raw:
            rss5.append(float(i[0]))
    #print("Rssi received in 5ghz")
    #print(rss5)
    b = range(1, len(rss5) + 1)
    plt.plot(b, rss5, 'b', linewidth=2.0, label="5ghz")
    plt.legend(bbox_to_anchor=(0.805, 1), loc=2, borderaxespad=0.)

    dir = settings.BASE_DIR
    plt.savefig(dir + "/heatmap/static/heatmap/images/fig1.png")
    return [rss2,rss5]