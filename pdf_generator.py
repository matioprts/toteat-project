from fpdf import FPDF

def generate_pdf(df_amounts_week, df_amounts_weekend):
  # 1. Set up the PDF doc basics
  pdf = FPDF()
  pdf.add_page()
  pdf.set_font('Arial', 'B', 16)

  # 2. Layout the PDF doc contents
  ## Title
  pdf.cell(0, 10, 'Análisis de datos: "La pikada de la esquina"', align='C')
  pdf.set_font('Arial', 'B', 14)
  ## Line breaks
  pdf.ln(20)
  # Subtitle
  pdf.cell(40, 5, 'Gráficos relevantes')
  ## Line breaks
  pdf.ln(10)
  ## Image
  pdf.image('./resultados/pedidos_diarios.png', w=200)
  ## Line breaks
  pdf.ln(5)
  ## Image
  pdf.image('./resultados/pedidos_por_horario.png', w=200)
  ## Line breaks
  pdf.add_page()
  ## Image
  pdf.image('./resultados/distribucion_ingreso.png', x=30, w=150)
  ## Line breaks
  pdf.ln(5)
  ## Image
  pdf.image('./resultados/distribucion_ventas.png', x=30, w=150)
  ## Line breaks
  pdf.ln(5)
  ## Image
  pdf.image('./resultados/clientes_por_zona.png', w=200)
  ## Line breaks
  pdf.ln(5)
  ## Image
  pdf.image('./resultados/tiempos_clientes_restaurant.png', w=200)
  ## Line breaks
  pdf.ln(5)
  ## Image
  pdf.image('./resultados/metodo_pago.png', w=200)
  ## Line breaks
  pdf.ln(5)
  ## Image
  pdf.image('./resultados/ordenes_garzones.png', w=200)
  ## Line breaks
  pdf.ln(5)
  ## Image
  pdf.image('./resultados/productos_repetidos.png', w=200)
  ## Line breaks
  pdf.ln(5)
  # Subtitle
  pdf.cell(40, 5, 'Estadísticas relevantes')
  ## Line breaks
  pdf.ln(10)
  pdf.set_font('Arial', 'B', 12)
  pdf.cell(0, 5, 'Monto percibido por cliente en la semana (Lunes-Jueves)')
  pdf.ln(10)
  pdf.cell(0, 5, f'Ventas totales: {df_amounts_week.count().item()}')
  pdf.ln(5)
  pdf.cell(0, 5, f'Promedio: ${int(df_amounts_week.mean().item())}')
  pdf.ln(5)
  pdf.cell(0, 5, f'Desviación estándar: ${int(df_amounts_week.std().item())}')
  pdf.ln(5)
  pdf.cell(0, 5, f'Monto mínimo: ${df_amounts_week.min().item()}')
  pdf.ln(5)
  pdf.cell(0, 5, f'Monto máximo: ${df_amounts_week.max().item()}')
  pdf.ln(10)
  pdf.cell(0, 5, 'Monto percibido por cliente en el fin de semana (Viernes-Domingo)')
  pdf.ln(10)
  pdf.cell(0, 5, f'Ventas totales: {df_amounts_weekend.count().item()}')
  pdf.ln(5)
  pdf.cell(0, 5, f'Promedio: ${int(df_amounts_weekend.mean().item())}')
  pdf.ln(5)
  pdf.cell(0, 5, f'Desviación estándar: ${int(df_amounts_weekend.std().item())}')
  pdf.ln(5)
  pdf.cell(0, 5, f'Monto mínimo: ${df_amounts_weekend.min().item()}')
  pdf.ln(5)
  pdf.cell(0, 5, f'Monto máximo: ${df_amounts_weekend.max().item()}')

  return pdf.output('./resultados/analisis_datos.pdf', 'F')
