from statistics import mean
import numpy as np
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import json
import plotter
import pandas as pd

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
duplicated_products = dict()
total_sell = 0
sell_per_product = dict()
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
  products = dict()
  total_amount += order['total']
  for product in order['products']:
    if amount_per_type.get(product['category']):
      amount_per_type[product['category']] += product['price']*product['quantity']
    else:
      amount_per_type[product['category']] = product['price']*product['quantity']
    if products.get(product['name']):
      products[product['name']] += 1
    else:
      products[product['name']] = 1
    if sell_per_product.get(product['name']):
      sell_per_product[product['name']] += 1
    else:
      sell_per_product[product['name']] = 1
    total_sell += 1
  for product in products.keys():
    if products[product] > 1:
      if duplicated_products.get(product):
        if duplicated_products[product].get(products[product]):
          duplicated_products[product][products[product]] += 1
        else:
          duplicated_products[product][products[product]] = 1
      else:
        duplicated_products[product] = dict()
        duplicated_products[product][products[product]] = 1

days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
values = list(days_counter.values())

plotter.plot_bar(days,values,init_date,end_date,"Día","Cantidad de Pedidos","Pedidos Diarios","./resultados/pedidos_diarios.png")

filtered_hours = list(hours_counter.keys())
filtered_hours.sort()
sort_values = list()
for hour in filtered_hours:
  sort_values.append(hours_counter[hour])

plotter.plot_bar_with_full_labels(filtered_hours,sort_values,init_date,end_date,"Hora","Cantidad de Pedidos","Pedidos por Horario","./resultados/pedidos_por_horario.png")

# eating_times = []
# for hour in hours_eating:
#   eating_times.append(str(hour)[:-3])
# eating_times.sort()
# set_times = set(eating_times)

# plotter.plot_hist_with_degrees_labels(eating_times,int(len(set_times)/5),90,init_date,end_date,"Hora","Cantidad de Pedidos","Tiempo de Clientes en Restaurant","./resultados/tiempos_clientes_restaurant")

filtered_payments = list(payments.keys())
filtered_payments.sort()
sort_values = list()
for payment in filtered_payments:
  sort_values.append(payments[payment])

plotter.plot_bar(filtered_payments,sort_values,init_date,end_date,"Método de Pago","Cantidad de Pedidos","Métodos de pago","./resultados/metodo_pago.png")

zones = []
for zone in diners_per_zone.keys():
  filtered_diners = list(diners_per_zone[zone].keys())
  filtered_diners.sort()
  sort_values = list()
  for diners in filtered_diners:
    sort_values.append(diners_per_zone[zone][diners])
  zones.append(sort_values)

plotter.plot_multiple_bars(zones,diners_per_zone,1,init_date,end_date,"Clientes por Zona","Cantidad de Pedidos","Distribución de Clientes por Zona","./resultados/clientes_por_zona.png")

waiters_names = list(waiters.keys())
waiters_values = list(waiters.values())

plotter.plot_bar(waiters_names,waiters_values,init_date,end_date,"Garzon(a)","Cantidad de Pedidos","Ordenes por Garzon(a)","./resultados/ordenes_garzones.png")

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

plotter.plot_pie(percentage_pie,explode,labels_pie,init_date,end_date,"Distribución del Ingreso por Tipo de Plato","./resultados/distribucion_ingreso.png")

longest_map = 0
for product in duplicated_products.keys():
  aux = max(duplicated_products[product])
  if aux > longest_map:
    longest_map = aux

products_repeated = []
for product in duplicated_products.keys():
  filtered_numbers = list(duplicated_products[product].keys())
  filtered_numbers.sort()
  sort_values = list()
  for index in range(2,longest_map+1):
    if duplicated_products[product].get(index):
      sort_values.append(duplicated_products[product][index])
    else:
      sort_values.append(0)
  products_repeated.append(sort_values)

plotter.plot_multiple_bars(products_repeated,duplicated_products,2,init_date,end_date,"Cantidad de Repetidos por Mesa","Cantidad de Pedidos","Platos Repetidos por Mesa","./resultados/productos_repetidos.png", longest_map=longest_map-1, bar_width=0.075)

labels_sales = list()
percentage_sales = list()
for product in sell_per_product.keys():
  labels_sales.append(product)
  percentage = sell_per_product[product]/total_sell
  percentage_sales.append(percentage)
explode = list()
for percentage in percentage_sales:
  explode.append(0)

plotter.plot_pie(percentage_sales,explode,labels_sales,init_date,end_date,"Distribución de las Ventas","./resultados/distribucion_ventas.png")

eating_times = []
for hour in hours_eating:
  eating_times.append(str(hour)[:-3])

df_amounts_week = pd.DataFrame(amounts_week_per_client)
print(df_amounts_week.describe())
df_amounts_weekend = pd.DataFrame(amounts_weekend_per_client)
print(df_amounts_weekend.describe())
