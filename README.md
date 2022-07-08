# Instrucciones toteat-project

## Configuración
Para poder utilizar el código es necesario contar con ciertas librerias:
- pandas
- numpy
- matplotlib

Por lo que si no se cuenta con estas, se deben instalar con el comando: *pip install {libreria}*

Para comenzar el programa se debe utilizar el comando: python *./main.py*

## Funcionamiento
A grandes rasgos, el código recolecta el json de la ruta provista en el enunciado, adquiere los datos y los procesa iterando sobre cada uno de los objetos dentro de la lista, obteniendo información relevante y realizando cálculos pequeños sobre la marcha. Para esto, el programa usa las estructuras de datos definidas en la sección # Data Structures

Luego de tener la información poblada y procesada, procede a llamar al archivo *plotter.py* encargado de graficar la información necesaria y almacenar los archivos en formato *.png* en la carpeta resultados **(debe crear esta carpeta si no la tiene en el repositorio raíz)**.

Finalmente, a través de pandas se obtienen dataframes para un par de datos interesantes a estudiar a nivel estadístico y son pasados a la función *generate_pdf* en el archivo *pdf_generator.py* para crear el reporte final con los gráficos y estadísticas recopiladas, el cual también será guardado en la carpeta resultados.
