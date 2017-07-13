import plotly
import plotly.graph_objs as go
from heatmap import models
import operator
from plotly import tools
def list_sort(a):
 b=[]
 for i in a:
  b.append((int(i.split(":")[0].split("/")[0]),int(i.split(":")[0].split("/")[1]),int(i.split(":")[1])))
 b.sort(key=operator.itemgetter(1,0,2))
 del a[:]
 for t in b:
  a.append("{}/{}:{}".format(t[0],t[1],t[2]))

def draw(f,d,n):
    in_for_diff=[]
    rss = []
    list_sort(d)
    d=d[-2:]
    for k in d:
        raw= models.Input.objects.values_list('Rss').filter(Timestamp=k,frequency=f,node_sender=n)
        for i in raw:
            rss.append(i[0])
    fig = tools.make_subplots(rows=1, cols=2, subplot_titles=(
    'D/M:H {}	T {}	freq {}'.format(d[0], 14,f),
    'D/M:H {}	T {}	freq {}'.format(d[1],14, f)))
    t=1
    for day in range(0, 2):
        lines = rss[day * 37:day * 37 + 37]
        lines[int(n) - 1] = "Sender"
        data = go.Heatmap(
        z=[
            ["{}".format(lines[4]), "{}".format(lines[9]), "{}".format(lines[14]), "", "", "", "{}".format(lines[29]),
             "{}".format(lines[34]), "{}".format(lines[36])],
            ["{}".format(lines[3]), "{}".format(lines[8]), "{}".format(lines[13]), "{}".format(lines[17]),
             "{}".format(lines[21]), "{}".format(lines[24]), "{}".format(lines[28]), "{}".format(lines[33]),
             "{}".format(lines[35])],
            ["{}".format(lines[2]), "{}".format(lines[7]), "{}".format(lines[12]), "{}".format(lines[16]),
             "{}".format(lines[20]), "{}".format(lines[23]), "{}".format(lines[27]), "{}".format(lines[32]), ""],
            ["{}".format(lines[1]), "{}".format(lines[6]), "{}".format(lines[11]), "", "{}".format(lines[19]), "",
             "{}".format(lines[26]), "{}".format(lines[31]), ""],
            ["{}".format(lines[0]), "{}".format(lines[5]), "{}".format(lines[10]), "{}".format(lines[15]),
             "{}".format(lines[18]), "{}".format(lines[22]), "{}".format(lines[25]), "{}".format(lines[30]), ""]
        ],
        zmin=-100,
        zmax=0
    )

        trace = go.Scatter(
        # displaying text (values), each couple (x,y) has a corresponding text value (x1,y1,text1) ainsi de suite
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8,
           0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3,
           4, 4, 4, 4, 4, 4, 4, 4, 4],
        mode='text',
        text=["{}".format(lines[4]), "{}".format(lines[9]), "{}".format(lines[14]), "", "", "", "{}".format(lines[29]),
              "{}".format(lines[34]), "{}".format(lines[36]), "{}".format(lines[3]), "{}".format(lines[8]),
              "{}".format(lines[13]), "{}".format(lines[17]), "{}".format(lines[21]), "{}".format(lines[24]),
              "{}".format(lines[28]), "{}".format(lines[33]), "{}".format(lines[35]),
              "{}".format(lines[2]), "{}".format(lines[7]), "{}".format(lines[12]), "{}".format(lines[16]),
              "{}".format(lines[20]), "{}".format(lines[23]), "{}".format(lines[27]), "{}".format(lines[32]), "",
              "{}".format(lines[1]), "{}".format(lines[6]), "{}".format(lines[11]), "", "{}".format(lines[19]), "",
              "{}".format(lines[26]), "{}".format(lines[31]), "",
              "{}".format(lines[0]), "{}".format(lines[5]), "{}".format(lines[10]), "{}".format(lines[15]),
              "{}".format(lines[18]), "{}".format(lines[22]), "{}".format(lines[25]), "{}".format(lines[30]), ""]
    )
        lines[int(n) - 1] = 0
        in_for_diff.append(lines)
        fig.append_trace(data, 1, t)
        fig.append_trace(trace, 1, t)
        t += 1
    r1 = diff(in_for_diff)
    plotly.offline.plot(fig, filename="Heatmap.html")
    return r1

def diff(liste):
    lines = []
    rss1=liste[0]
    rss2 = liste[1]
    for (j, i) in zip(rss2, rss1):
        lines.append('{:02f}'.format(float(j) - float(i)))

    trace = go.Scatter(
        # displaying text (values), each couple (x,y) has a corresponding text value (x1,y1,text1) ainsi de suite
        x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1, 2, 3, 4, 5, 6, 7, 8,
           0, 1, 2, 3, 4, 5, 6, 7, 8],
        y=[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3,
           4, 4, 4, 4, 4, 4, 4, 4, 4],
        mode='text',
        text=["{}".format(lines[4]), "{}".format(lines[9]), "{}".format(lines[14]), "", "", "", "{}".format(lines[29]),
              "{}".format(lines[34]), "{}".format(lines[36]), "{}".format(lines[3]), "{}".format(lines[8]),
              "{}".format(lines[13]), "{}".format(lines[17]), "{}".format(lines[21]), "{}".format(lines[24]),
              "{}".format(lines[28]), "{}".format(lines[33]), "{}".format(lines[35]),
              "{}".format(lines[2]), "{}".format(lines[7]), "{}".format(lines[12]), "{}".format(lines[16]),
              "{}".format(lines[20]), "{}".format(lines[23]), "{}".format(lines[27]), "{}".format(lines[32]), "",
              "{}".format(lines[1]), "{}".format(lines[6]), "{}".format(lines[11]), "", "{}".format(lines[19]), "",
              "{}".format(lines[26]), "{}".format(lines[31]), "",
              "{}".format(lines[0]), "{}".format(lines[5]), "{}".format(lines[10]), "{}".format(lines[15]),
              "{}".format(lines[18]), "{}".format(lines[22]), "{}".format(lines[25]), "{}".format(lines[30]), ""]
    )
    fig = tools.make_subplots(rows=1, cols=1)
    fig.append_trace(trace, 1, 1)
    plotly.offline.plot(fig, filename="Diff.html")