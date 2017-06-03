import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from . import models

def draw(n_s,n_r,a):
    rss2 = []
    rss5 = []
    for i in a:
        raw= models.Input.objects.values_list('Rss').filter(Timestamp=i,node_sender=n_s,node_receiver=n_r,frequency=2412)
        for i in raw:
            rss2.append(i[0])
    #print("Rssi received in 2ghz")
    #print(rss2)
    b = range(1, len(rss2) + 1)
    my_xticks = []
    for i in a:
        my_xticks.append(i)
    plt.xticks(b, my_xticks)
    plt.plot(b, rss2, 'r', linewidth=2.0, label="2ghz")
    plt.title('Node {} => Node {} '.format(n_s, n_r))
    plt.xlabel('Time format D/M:H')
    plt.ylabel('Received power (dBm)')

    for i in a:
        raw = models.Input.objects.values_list('Rss').filter(Timestamp=i, node_sender=n_s, node_receiver=n_r,
                                                             frequency=5180)
        for i in raw:
            rss5.append(i[0])
    #print("Rssi received in 5ghz")
    #print(rss5)
    b = range(1, len(rss5) + 1)
    plt.plot(b, rss5, 'b', linewidth=2.0, label="5ghz")
    plt.legend(bbox_to_anchor=(0.805, 1), loc=2, borderaxespad=0.)
    return plt  #to return many values one can choose to return a tuple
#Should be nice to show rss2 and rss5 in a tab and have node receiver first value initiated to 2