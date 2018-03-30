import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from heatmap import models
from django.conf import settings
import operator

def list_sort(a):
    b = []
    for i in a:
        b.append((int(i.split(":")[0].split("/")[0]), int(i.split(":")[0].split("/")[1]),int(i.split(":")[1].split('-')[0]),int(i.split(":")[1].split('-')[1])))
    b.sort(key=operator.itemgetter(1, 0,2,3))
    del a[:]
    for t in b:
        a.append("{}/{}:{}-{}".format(t[0], t[1], t[2],t[3]))
def draw(n_s,n_r,r,t):
    days_2ghz = []
    days_5ghz =[]
    rss_2ghz = [[] for i in range(1, 5)]
    rss_5ghz = [[] for i in range(1, 5)]
    raw = [[] for i in range(1, 5)]
    outcome = models.Input.objects.values_list('Timestamp').filter(frequency=2412,rate=r,transmission_power=t)
    for d in outcome:
        days_2ghz.append(d[0])
    a = list(set(days_2ghz))
    list_sort(a)
    a=a[-10:]
    outcome = models.Input.objects.values_list('Timestamp').filter(frequency=5180, rate=r, transmission_power=t)
    for d in outcome:
        days_5ghz.append(d[0])
    b = list(set(days_5ghz))
    list_sort(b)
    b = b[-10:]
    for i in a:
        raw[0]= models.Input.objects.values_list('Rss_mrc').filter(Timestamp=i,node_sender=n_s,node_receiver=n_r,frequency=2412, rate=r, transmission_power=t)
        raw[1]=models.Input.objects.values_list('Rss_ant0').filter(Timestamp=i, node_sender=n_s, node_receiver=n_r,
                                                                 frequency=2412, rate=r, transmission_power=t)
        raw[2]=models.Input.objects.values_list('Rss_ant1').filter(Timestamp=i, node_sender=n_s, node_receiver=n_r,
                                                                       frequency=2412, rate=r, transmission_power=t)
        raw[3]=models.Input.objects.values_list('Rss_ant2').filter(Timestamp=i, node_sender=n_s, node_receiver=n_r,
                                                                       frequency=2412, rate=r, transmission_power=t)
        for i,j,k,l in zip(raw[0],raw[1],raw[2],raw[3]):
            rss_2ghz[0].append(float(i[0]))
            rss_2ghz[1].append(float(j[0]))
            rss_2ghz[2].append(float(k[0]))
            rss_2ghz[3].append(float(l[0]))

    raw = [[] for i in range(1, 5)]
    for i in b:
        raw[0]= models.Input.objects.values_list('Rss_mrc').filter(Timestamp=i,node_sender=n_s,node_receiver=n_r,frequency=5180, rate=r, transmission_power=t)
        raw[1]=models.Input.objects.values_list('Rss_ant0').filter(Timestamp=i, node_sender=n_s, node_receiver=n_r,
                                                                 frequency=5180, rate=r, transmission_power=t)
        raw[2]=models.Input.objects.values_list('Rss_ant1').filter(Timestamp=i, node_sender=n_s, node_receiver=n_r,
                                                                       frequency=5180, rate=r, transmission_power=t)
        raw[3]=models.Input.objects.values_list('Rss_ant2').filter(Timestamp=i, node_sender=n_s, node_receiver=n_r,
                                                                       frequency=5180, rate=r, transmission_power=t)
        for i, j, k, l in zip(raw[0], raw[1], raw[2], raw[3]):
            rss_5ghz[0].append(float(i[0]))
            rss_5ghz[1].append(float(j[0]))
            rss_5ghz[2].append(float(k[0]))
            rss_5ghz[3].append(float(l[0]))

    plt.figure(1)
    plt.subplot(211)
    my_xticks = []
    c = range(1, len(a) + 1)
    for i in a:
        my_xticks.append(i)
    plt.xticks(c, my_xticks, fontsize=8)

    plt.plot(c, rss_2ghz[0], 'ro-', linewidth=2.0, label="mrc")
    plt.plot(c, rss_2ghz[1], 'bo-', linewidth=2.0, label="ant0")
    plt.plot(c, rss_2ghz[2], 'go-', linewidth=2.0, label="ant1")
    plt.plot(c, rss_2ghz[3], 'mo-', linewidth=2.0, label="ant2")

    plt.title('Node {} => Node {} in 2ghz'.format(n_s, n_r))
    plt.ylabel('Received power (dBm)')

    plt.subplot(212)
    my_xticks = []
    c = range(1, len(b) + 1)
    for i in b:
        my_xticks.append(i)
    plt.xticks(c, my_xticks, fontsize=8)

    plt.plot(c, rss_5ghz[0], 'ro-', linewidth=2.0, label="mrc")
    plt.plot(c, rss_5ghz[1], 'bo-', linewidth=2.0, label="ant0")
    plt.plot(c, rss_5ghz[2], 'go-', linewidth=2.0, label="ant1")
    plt.plot(c, rss_5ghz[3], 'mo-', linewidth=2.0, label="ant2")

    plt.ylabel('Received power (dBm)')
    plt.title('And in 5ghz',fontsize=8)
    plt.xlabel('Time format D/M:H-M')
    plt.legend(bbox_to_anchor=(0.975, 1), loc=2, borderaxespad=0.)

    dir = settings.BASE_DIR
    plt.savefig(dir + "/heatmap/static/heatmap/images/fig1.png")

    return [rss_2ghz,rss_5ghz]
