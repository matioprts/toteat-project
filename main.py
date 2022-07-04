import numpy as np
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter


request = requests.get("https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json")
data = request.json()

timestamps = list()
weekdays = list()
init_date = None
end_date = None
days_counter = {
  0: 0,
  1: 0,
  2: 0,
  3: 0,
  4: 0,
  5: 0,
  6: 0
}
hours_counter = dict()
hours_eating = list()
for order in data:
  start_date = datetime.strptime(order['date_opened'], '%Y-%m-%d %H:%M:%S')
  finish_date = datetime.strptime(order['date_closed'], '%Y-%m-%d %H:%M:%S')
  timestamps.append((start_date, finish_date))
  if not init_date or init_date > start_date:
    init_date = start_date
  if not end_date or end_date < finish_date:
    end_date = finish_date
  days_counter[start_date.weekday()] += 1
  if hours_counter.get(start_date.hour):
    hours_counter[start_date.hour] += 1
  else:
    hours_counter[start_date.hour] = 1
  hours_eating.append(finish_date-start_date)

days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
values = list(days_counter.values())

fig = plt.figure(figsize = (10, 5))
plt.bar(days, values, color ='maroon',
        width = 0.4)
plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
plt.xlabel("Dia")
plt.ylabel("# Pedidos")
plt.title("Pedidos diarios")
plt.savefig('./resultados/pedidos_diarios.png')

filtered_hours = list(hours_counter.keys())
filtered_hours.sort()
sort_values = list()
for hour in filtered_hours:
  sort_values.append(hours_counter[hour])

fig = plt.figure(figsize = (10, 5))
plt.xticks(np.arange(min(filtered_hours), max(filtered_hours)+1, 1.0))
plt.bar(filtered_hours, sort_values, color ='maroon',
        width = 0.4)
plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
plt.xlabel("Hora")
plt.ylabel("# Pedidos")
plt.title("Pedidos por horario")
plt.savefig('./resultados/pedidos_por_horario.png')
