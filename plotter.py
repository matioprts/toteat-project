import matplotlib.pyplot as plt
import numpy as np

def plot_bar(x_data, y_data, init_date, end_date, x_label, y_label, title, path):
  plt.figure(figsize = (12, 5))
  plt.bar(x_data, y_data, color ='maroon',
          width = 0.4)
  plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.title(title)
  plt.savefig(path)

def plot_bar_with_full_labels(x_data, y_data, init_date, end_date, x_label, y_label, title, path):
  plt.figure(figsize = (10, 5))
  plt.xticks(np.arange(min(x_data), max(x_data)+1, 1.0))
  plot_bar(x_data, y_data, init_date, end_date, x_label, y_label, title, path)

def plot_hist_with_degrees_labels(data, bins, rotation, init_date, end_date, x_label, y_label, title, path):
  plt.figure(figsize = (15, 5))
  plt.hist(data, color='maroon', edgecolor='black', bins=bins)
  plt.xticks(rotation=rotation, ha= 'right', fontsize='x-small')
  plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.title(title)
  plt.savefig(path)

def plot_multiple_bars(array_mapped, main_dict, range_start, init_date, end_date, x_label, y_label, title, path, longest_map=None, bar_width=0.25):
  if not longest_map:
    longest_map = len(max(array_mapped, key=len))
  type_labels = list(main_dict.keys())
  x_labels = [i for i in range(range_start,longest_map+range_start)]

  # set width of bar
  colors = ['c', 'm', 'g', 'b', 'r', 'y', 'k', 'peru', 'salmon', 'gray', 'deeppink', 'lime']
  plt.subplots(figsize =(12, 5))

  br_flag = False
  for index in range(len(array_mapped)):
    # Set position of bar on X axis
    if not br_flag:
      br = np.arange(longest_map)
      br_flag = True
    else:
      br = [x + bar_width for x in br]
    plt.bar(br, array_mapped[index], color=colors[index], width = bar_width,
          edgecolor ='black', label=type_labels[index], align='center')

  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.title(title)
  plt.xticks([r + bar_width for r in range(longest_map)], x_labels)
  plt.text(0.01, 0.89, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
  plt.legend()
  plt.savefig(path)

def plot_pie(percentages, explode, labels, init_date, end_date, title, path):
  colors = ['c', 'm', 'g', 'r', 'y', 'peru', 'salmon', 'gray', 'deeppink', 'lime', 'gold']
  _, ax1 = plt.subplots()
  ax1.pie(percentages, explode=explode, labels=labels, autopct='%1.1f%%',
          shadow=True, startangle=90, colors=colors)
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  plt.text(0.01, 0.01, f'Ventana de estudio\nFecha Inicio: {init_date.date()}\nFecha Término: {end_date.date()}', fontsize=11, transform=plt.gcf().transFigure)
  plt.title(title)
  plt.savefig(path)
