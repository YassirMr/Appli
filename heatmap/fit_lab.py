import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.stats
from math import log10
from sklearn.metrics import mean_squared_error
from heatmap import models
from django.conf import settings



def draw(f,d):
    received_power=[]
    R_Tequation = []
    R_logdistance = []
    R_2ray = []
    R_hata = []
    gaindict = {'all': 9, 'ant0': 3, 'ant1': 3, 'ant2': 3}
    row_nodes = [9, 14, 18, 22, 25, 29, 34, 36]
    row_distance = np.arange(1.36, 10.88, 1.36)
    raw=[]
    for i in row_nodes:
        raw = models.Input.objects.values_list('Rss').filter(Timestamp=d, node_sender=4, node_receiver=i,
                                                             frequency=f)
        for i in raw:
            received_power.append(float(i[0]))

    plt.plot(row_distance, received_power, 'ro', label="r2lab")
    plt.title('Power decrease when node 4 is the sender Tx:14 dBm')
    plt.xlabel('Distance : meters')
    plt.ylabel('Received power (dBm)')

    for i in row_distance:
        R_2ray.append(int(14 / 100) - 40 * log10(i) + 10 * log10(gaindict["all"]))

    plt.plot(row_distance, R_2ray, 'yo', label="2ray")

    # ploting the log distance path loss model, (gamma=2 , Xg=0)

    for i in row_distance:
        R_logdistance.append(
            float(14) - 10 * 2 * log10(i / 1.36) + (float(received_power[0]) - 14))

    plt.plot(row_distance, R_logdistance, 'b^', label="log distance")
    print('Mean quare error r2lab/log: {}'.format(mean_squared_error(received_power, R_logdistance)))
    error_r2lab_log = mean_squared_error(received_power, R_logdistance)

    # ploting the telecom equation model
    for i in row_distance:
        R_Tequation.append(14 + gaindict["all"] + gaindict["all"] - (
        35.45 + 20 * log10(int(f)) + 20 * log10(i / 1000)))
    plt.plot(row_distance, R_Tequation, 'g^', label="Telecom equ")

    # ploting the hata model
    for i in row_distance:
        c = 0.8 + (1.1 * log10(int(f)) - 0.7) - 1.56 * log10(int(f))
        R_hata.append(14 - (69.55 + 26.16 * log10(int(f)) - c + 44.9 * log10(i / 1000)))
    # print(26.16*log10(args.freq)-c+44.9*log10(i/1000))
    plt.plot(row_distance, R_hata, 'mo', label="hata model")
    print('Mean quare error r2lab/hata: {}'.format(mean_squared_error(received_power, R_hata)))
    error_r2lab_hata=mean_squared_error(received_power, R_hata)

    plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.)  # 1.05
    # Here the confidence bounds are computed
    confidence = 0.95
    a = 1.0 * np.array(received_power)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1 + confidence) / 2., n - 1)

    plt.plot([row_distance[0], row_distance[-1]], [m - h, m - h], 'r')
    plt.text(row_distance[-1], m - h, 'lower confidence bound')
    plt.plot([row_distance[0], row_distance[-1]], [m + h, m + h], 'r')
    plt.text(row_distance[-1], m + h, 'higher confidence bound')

    #return plt.show()
    dir = settings.BASE_DIR
    plt.savefig(dir + "/heatmap/static/heatmap/images/fig2.png")
    return [error_r2lab_log, error_r2lab_hata]