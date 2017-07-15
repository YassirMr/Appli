from django.db import models

class Input(models.Model):
    Timestamp = models.CharField(max_length=90)
    node_sender = models.CharField(max_length=50)
    node_receiver = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    transmission_power = models.CharField(max_length=50)
    rate = models.CharField(max_length=50)
    Rss_mrc = models.CharField(max_length=20)
    Rss_ant0 = models.CharField(max_length=20)
    Rss_ant1 = models.CharField(max_length=20)
    Rss_ant2 = models.CharField(max_length=20)

#    def raw(self):
#        return "Time {} Sender {} Receiver {} Rssi {} ".format(self.Time_text,self.node_sender_text,self.node_receiver_text,self.Rss_text)

class UploadFile(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d')