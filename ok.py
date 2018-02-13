import sqlite3


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

#x=35532-34163
#for i in range(1,1369*2+1):
#cursor.execute('DELETE FROM heatmap_input WHERE id={}'.format(i))
#13/7:23-14 13/7:23-15 14/7:20-16 15/7:17-32 15/7:17-59 15/8:17-45
cursor.execute('DELETE FROM heatmap_input WHERE Timestamp="7/7:16-17"')
conn.commit()
