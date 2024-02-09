import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def cargar_archivos():
    archivos = filedialog.askopenfilenames(title="Seleccione los archivos CSV")
    return archivos

def cargar_txt():
    archivo_txt = filedialog.askopenfilename(title="Seleccione el archivo TXT")
    return archivo_txt

def procesar_datos():
    try:
        archivos = cargar_archivos()
        ruta_archivo_txt = cargar_txt()
        
        # Definir las columnas que te interesan (nombre y precio)
        columnas = [1, 5, 6, 9]  # Las columnas están indexadas desde 0

        # Crear una lista de DataFrames
        dataframes = []
        for archivo, nombre_df in zip(archivos, ['Barracas', 'Cofarsur', 'Del Sud']):
            df = pd.read_csv(archivo, sep=';', usecols=columnas, header=None, encoding='ISO-8859-1')
            df.columns = ["Codigo", 'Nombre', "Gramaje", 'Precio']
            df['Archivo'] = nombre_df  # Agregar una columna con el nombre del archivo
            dataframes.append(df)

        # Concatenar el nombre y el gramaje
        for df in dataframes:
            df['Nombre Producto'] = df['Nombre'] + ' ' + df['Gramaje']

        # Encontrar la mejor opción para cada código de barras
        codigo_barras_unicos = set(dataframes[0]['Codigo'])
        mejor_opcion = pd.DataFrame({'Codigo': list(codigo_barras_unicos)})

        # Crear un DataFrame que contenga el nombre del producto para cada código de barras
        nombres_df = dataframes[0][['Codigo', 'Nombre Producto']]
        for df in dataframes:
            mejor_precio = df.groupby('Codigo')['Precio'].min().reset_index()
            mejor_opcion = mejor_opcion.merge(mejor_precio, on='Codigo', suffixes=('', f'_{df["Archivo"].iloc[0]}'))

        # Renombrar las columnas
        mejor_opcion.rename(columns={'Precio': 'Barracas'}, inplace=True)

        # Agregar los nombres de los archivos a las columnas de precio
        for df in dataframes:
            mejor_opcion.rename(columns={f'Precio_{df["Archivo"].iloc[0]}': f'Precio_{df["Archivo"].iloc[0]}'}, inplace=True)

        # Combinar el DataFrame de nombres con el DataFrame de mejor opción
        mejor_opcion = mejor_opcion.merge(nombres_df, on='Codigo')

        # Leer el archivo de texto en un DataFrame sin utilizar la primera fila como encabezados
        BaseTxt = pd.read_csv(ruta_archivo_txt, sep='\t', header=None)

        # Asignar nombres a las columnas
        BaseTxt.columns = ['Codigo', 'Producto', 'Condicion', 'CantidadDeseada', 'Cantidad']

        # Eliminar las filas con valores no válidos en la columna "Codigo"
        BaseTxt = BaseTxt[BaseTxt['Codigo'].str.isnumeric()]

        # Convertir la columna "Codigo" a tipo int64
        BaseTxt["Codigo"] = BaseTxt["Codigo"].astype("int64")

        # Calcula el mínimo para cada fila entre las tres columnas de precio
        mejor_opcion['Recomendado'] = mejor_opcion[['Barracas', 'Precio_Cofarsur', 'Precio_Del Sud']].idxmin(axis=1)

        # Limpia el nombre de la columna recomendada
        mejor_opcion['Recomendado'] = mejor_opcion['Recomendado'].str.replace('Precio_', '')

        # Convertir la columna "Codigo" en mejor_opcion a int64
        mejor_opcion['Codigo'] = mejor_opcion['Codigo'].astype('int64')

        # Realizar la fusión (join) en la columna "Codigo"
        mejor_opcion_filtrado = pd.merge(mejor_opcion, BaseTxt, on="Codigo", how="inner")

        # Guardar el DataFrame resultante en un archivo CSV
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
        mejor_opcion.to_csv(ruta, index=False)
        
        messagebox.showinfo("Proceso completado", "Los datos se han procesado y guardado en un archivo CSV correctamente.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Procesador de datos")
root.geometry("400x200")

# Botones
btn_cargar_archivos = tk.Button(root, text="Cargar archivos CSV", command=procesar_datos)
btn_cargar_archivos.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
