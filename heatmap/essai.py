from . import models

lines= models.Input.objects.values_list('node_sender')
print(lines)