import sqlite3


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

x=35532-34163
for i in range(1,1369*2+1):
 cursor.execute('DELETE FROM heatmap_input WHERE id={}'.format(i))
conn.commit()
