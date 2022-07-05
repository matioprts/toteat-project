import numpy as np
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import json

# request = requests.get("https://storage.googleapis.com/backupdatadev/ejercicio/ventas.json")
# data = request.json()

with open('json_data.json') as json_file:
    data = json.load(json_file)

# Dates Data Structures
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
# Payment Data Structures
payments = dict()
amounts_week_per_client = list()
amounts_weekend_per_client = list()
# Clients Data Structures
diners_per_zone = dict()
# Waiters Data Structures
waiters = dict()
# Products Data Structure
total_amount = 0
amount_per_type = dict()

for order in data:
  # Dates Info
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
  # Payment Info
  for payment in order['payments']:
    if payments.get(payment['type']):
      payments[payment['type']] += 1
    else:
      payments[payment['type']] = 1
  if start_date.weekday() <= 4:
    amounts_week_per_client.append(int(order['total']/order['diners']))
  else:
    amounts_weekend_per_client.append(int(order['total']/order['diners']))
  # Clients Info
  if diners_per_zone.get(order['zone']):
    if diners_per_zone[order['zone']].get(order['diners']):
      diners_per_zone[order['zone']][order['diners']] += 1
    else:
      diners_per_zone[order['zone']][order['diners']] = 1
  else:
    diners_per_zone[order['zone']] = dict()
    diners_per_zone[order['zone']][order['diners']] = 1
  # Waiters Info
  if waiters.get(order['waiter']):
    waiters[order['waiter']] += 1
  else:
    waiters[order['waiter']] = 1
  # Products Info
  total_amount += order['total']
  for product in order['products']:
    if amount_per_type.get(product['category']):
      amount_per_type[product['category']] += product['price']*product['quantity']
    else:
      amount_per_type[product['category']] = product['price']*product['quantity']

days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
values = list(days_counter.values())

fig = plt.figure(figsize = (10, 5))
plt.bar(days, values, color ='maroon',
        width = 0.4)
plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
plt.xlabel("Dia")
plt.ylabel("Cantidad de Pedidos")
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
plt.ylabel("Cantidad de Pedidos")
plt.title("Pedidos por horario")
plt.savefig('./resultados/pedidos_por_horario.png')

eating_times = []
for hour in hours_eating:
  eating_times.append(str(hour)[:-3])
eating_times.sort()
set_times = set(eating_times)
fig = plt.figure(figsize = (15, 6))
plt.hist(eating_times, color='maroon', edgecolor='black', bins=int(len(set_times)/5))
plt.xticks(rotation=90, fontsize='x-small')
plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
plt.xlabel("Hora")
plt.ylabel("Cantidad de Pedidos")
plt.title("Tiempo de Clientes en Restaurant")
plt.savefig('./resultados/tiempos_clientes_restaurant.png')

filtered_payments = list(payments.keys())
filtered_payments.sort()
sort_values = list()
for payment in filtered_payments:
  sort_values.append(payments[payment])

fig = plt.figure(figsize = (15, 6))
plt.bar(filtered_payments, sort_values, color ='maroon',
        width = 0.4)
plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
plt.xlabel("Método de pago")
plt.ylabel("Cantidad de Pedidos")
plt.title("Métodos de pago")
plt.savefig('./resultados/metodo_pago.png')

zones = []
for zone in diners_per_zone.keys():
  filtered_diners = list(diners_per_zone[zone].keys())
  filtered_diners.sort()
  sort_values = list()
  for diners in filtered_diners:
    sort_values.append(diners_per_zone[zone][diners])
  zones.append(sort_values)

longest_diners_zone = max(zones, key=len)
zones_labels = list(diners_per_zone.keys())
diners_labels = [i for i in range(1,len(longest_diners_zone)+1)]

# set width of bar
barWidth = 0.25
colors = ['c', 'm', 'g', 'b', 'r', 'y', 'k', 'w']
fig = plt.subplots(figsize =(12, 5))

br_flag = False
for index in range(len(zones)):
  # Set position of bar on X axis
  if not br_flag:
    br = np.arange(len(longest_diners_zone))
    br_flag = True
  else:
    br = [x + barWidth for x in br]
  plt.bar(br, zones[index], color=colors[index], width = barWidth,
        edgecolor ='black', label=zones_labels[index])

# Adding Xticks
plt.xlabel('Clientes por zona', fontweight ='bold', fontsize = 15)
plt.ylabel('Cantidad de Pedidos', fontweight ='bold', fontsize = 15)

plt.xticks([r + barWidth for r in range(len(longest_diners_zone))], diners_labels)
plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
plt.legend()
plt.savefig('./resultados/clientes_por_zona.png')

waiters_names = list(waiters.keys())
waiters_values = list(waiters.values())

fig = plt.figure(figsize = (15, 6))
plt.bar(waiters_names, waiters_values, color ='maroon',
        width = 0.4)
plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
plt.xlabel("Garzon(a)")
plt.ylabel("Cantidad de Pedidos")
plt.title("Ordenes por Garzon(a)")
plt.savefig('./resultados/ordenes_garzones.png')

labels_pie = list()
percentage_pie = list()
max_percentage = False
for type in amount_per_type.keys():
  labels_pie.append(type)
  percentage = amount_per_type[type]/total_amount
  percentage_pie.append(percentage)
  if not max_percentage or max_percentage < percentage:
    max_percentage = percentage
explode = list()
for percentage in percentage_pie:
  if percentage == max_percentage:
    explode.append(0.1)
  else:
    explode.append(0)

fig1, ax1 = plt.subplots()
ax1.pie(percentage_pie, explode=explode, labels=labels_pie, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.text(0.01, 0.01, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
plt.title("Distribución del Ingreso por tipo de plato")
plt.savefig('./resultados/distribucion_ingreso.png')
