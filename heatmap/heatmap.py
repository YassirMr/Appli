import plotly
import plotly.graph_objs as go
from plotly import tools
from . import models

def draw(f,d,n):
    lines = []
    print(f)
    print(d)
    raw= models.Input.objects.values_list('Rss').filter(Timestamp=d,frequency=f,node_sender=n)
    for i in raw:
     lines.append(i[0])
    lines[int(n)- 1] = "Sender"
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
    D = [data, trace]

    fig = go.Figure(data=D)
    return plotly.offline.plot(fig, filename="freq {} n {} sender, ant=all, T=14 dBm".format(f, n))
