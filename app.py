import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Configuración del color de fondo para los campos de entrada
ENTRY_BG_COLOR = "white"

archivos_csv = {}
archivo_txt = ""
descuentos = {"Barracas": 0, "Cofarsur": 0, "Del Sud": 0}
entry_descuentos = {}  # Inicialización del diccionario para los campos de entrada de descuentos


def mostrar_datos_csv(archivo_csv):
    try:
        df = pd.read_csv(archivo_csv, sep=';', encoding='ISO-8859-1')
        messagebox.showinfo("Datos CSV", f"Datos del archivo CSV:\n{df.head()}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar datos CSV: {str(e)}")


def cargar_archivo_csv(nombre_df):
    global archivos_csv
    archivo_csv = filedialog.askopenfilename(title=f"Seleccione el archivo CSV para {nombre_df}")
    archivos_csv[nombre_df] = archivo_csv
    if nombre_df != "Barracas":  # Mostrar datos solo si no es Barracas
        mostrar_datos_csv(archivo_csv)

def cargar_archivo_txt():
    global archivo_txt
    archivo_txt = filedialog.askopenfilename(title="Seleccione el archivo TXT")

def procesar_datos():
    try:
        if not archivos_csv:
            messagebox.showerror("Error", "Por favor, primero cargue los archivos CSV.")
            return
        elif not archivo_txt:
            messagebox.showerror("Error", "Por favor, primero cargue el archivo TXT.")
            return
        
        for key, value in descuentos.items():
            descuentos[key] = int(entry_descuentos[key].get())

        columnas = [1, 5, 6, 9]  

        dataframes = []
        for nombre_df, archivo_csv in archivos_csv.items():
            df = pd.read_csv(archivo_csv, sep=';', usecols=columnas, header=None, encoding='ISO-8859-1')
            df.columns = ["Codigo", 'Nombre', "Gramaje", 'Precio']
            df['Archivo'] = nombre_df  
            df['Precio'] = df['Precio'] * (1 - descuentos[nombre_df] / 100)
            dataframes.append(df)

        for df in dataframes:
            df['Nombre Producto'] = df['Nombre'] + ' ' + df['Gramaje']

        codigo_barras_unicos = set(dataframes[0]['Codigo'])
        mejor_opcion = pd.DataFrame({'Codigo': list(codigo_barras_unicos)})

        nombres_df = dataframes[0][['Codigo', 'Nombre Producto']]
        for df in dataframes:
            mejor_precio = df.groupby('Codigo')['Precio'].min().reset_index()
            mejor_opcion = mejor_opcion.merge(mejor_precio, on='Codigo', suffixes=('', f'_{df["Archivo"].iloc[0]}'))

        mejor_opcion.rename(columns={'Precio': 'Barracas'}, inplace=True)

        for df in dataframes:
            mejor_opcion.rename(columns={f'Precio_{df["Archivo"].iloc[0]}': f'Precio_{df["Archivo"].iloc[0]}'}, inplace=True)

        mejor_opcion = mejor_opcion.merge(nombres_df, on='Codigo')

        BaseTxt = pd.read_csv(archivo_txt, sep='\t', header=None)
        BaseTxt.columns = ['Codigo', 'Producto', 'Condicion', 'CantidadDeseada', 'Cantidad']
        BaseTxt = BaseTxt[BaseTxt['Codigo'].str.isnumeric()]
        BaseTxt["Codigo"] = BaseTxt["Codigo"].astype("int64")

        mejor_opcion['Recomendado'] = mejor_opcion[['Barracas', 'Precio_Cofarsur', 'Precio_Del Sud']].idxmin(axis=1)
        mejor_opcion['Recomendado'] = mejor_opcion['Recomendado'].str.replace('Precio_', '')
        mejor_opcion['Codigo'] = mejor_opcion['Codigo'].astype('int64')

        mejor_opcion_filtrado = pd.merge(mejor_opcion, BaseTxt, on="Codigo", how="inner")

        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
        mejor_opcion.to_csv(ruta, index=False)
        
        messagebox.showinfo("Proceso completado", "Los datos se han procesado y guardado en un archivo CSV correctamente.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

def filtrar_precios_barracas():
    try:
        global archivos_csv
        if not archivos_csv:
            messagebox.showerror("Error", "Por favor, primero cargue los archivos CSV.")
            return

        archivo_csv_barracas = archivos_csv.get("Barracas")
        df_barracas = pd.read_csv(archivo_csv_barracas, sep=';', usecols=[1,5, 9], header=None, encoding='ISO-8859-1')
        df_barracas.columns = ['Codigo','Nombre', 'Precio']

        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
        df_barracas.to_csv(ruta, index=False)
        
        messagebox.showinfo("Proceso completado", "Los precios de Barracas se han guardado en un archivo CSV correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

def filtrar_precios_cofarsur():
    try:
        global archivos_csv
        if not archivos_csv:
            messagebox.showerror("Error", "Por favor, primero cargue los archivos CSV.")
            return

        archivo_csv_cofarsur = archivos_csv.get("Cofarsur")
        df_cofarsur = pd.read_csv(archivo_csv_cofarsur, sep=';', usecols=[1,5,9], header=None, encoding='ISO-8859-1')
        df_cofarsur.columns = ['Codigo','Nombre', 'Precio']

        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
        df_cofarsur.to_csv(ruta, index=False)
        
        messagebox.showinfo("Proceso completado", "Los precios de Cofarsur se han guardado en un archivo CSV correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

def filtrar_precios_delsud():
    try:
        global archivos_csv
        if not archivos_csv:
            messagebox.showerror("Error", "Por favor, primero cargue los archivos CSV.")
            return

        archivo_csv_delsud = archivos_csv.get("Del Sud")
        df_delsud = pd.read_csv(archivo_csv_delsud, sep=';', usecols=[1,5,9], header=None, encoding='ISO-8859-1')
        df_delsud.columns = ['Codigo','Nombre', 'Precio']

        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
        df_delsud.to_csv(ruta, index=False)
        
        messagebox.showinfo("Proceso completado", "Los precios de Del Sud se han guardado en un archivo CSV correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error: {str(e)}")

root = tk.Tk()
root.title("Procesador de datos")
root.geometry("600x400")

# Configuración del color de fondo para los campos de entrada
root.option_add("*Entry*background", ENTRY_BG_COLOR)

frame_barracas = tk.Frame(root)
frame_barracas.pack(pady=5)
btn_cargar_barracas = tk.Button(frame_barracas, text="Cargar archivo CSV de Barracas", command=lambda: cargar_archivo_csv("Barracas"))
btn_cargar_barracas.pack(side="left")
entry_descuentos["Barracas"] = tk.Entry(frame_barracas)
entry_descuentos["Barracas"].pack(side="left")

frame_cofarsur = tk.Frame(root)
frame_cofarsur.pack(pady=5)
btn_cargar_cofarsur = tk.Button(frame_cofarsur, text="Cargar archivo CSV de Cofarsur", command=lambda: cargar_archivo_csv("Cofarsur"))
btn_cargar_cofarsur.pack(side="left")
entry_descuentos["Cofarsur"] = tk.Entry(frame_cofarsur)
entry_descuentos["Cofarsur"].pack(side="left")

frame_delsud = tk.Frame(root)
frame_delsud.pack(pady=5)
btn_cargar_delsud = tk.Button(frame_delsud, text="Cargar archivo CSV de Del Sud", command=lambda: cargar_archivo_csv("Del Sud"))
btn_cargar_delsud.pack(side="left")
entry_descuentos["Del Sud"] = tk.Entry(frame_delsud)
entry_descuentos["Del Sud"].pack(side="left")

btn_cargar_txt = tk.Button(root, text="Cargar archivo TXT", command=cargar_archivo_txt)
btn_cargar_txt.pack(pady=5)

btn_procesar = tk.Button(root, text="Procesar datos", command=procesar_datos)
btn_procesar.pack(pady=5)

btn_filtrar_barracas = tk.Button(root, text="Filtrar precios por Barracas", command=filtrar_precios_barracas)
btn_filtrar_barracas.pack(pady=5)

btn_filtrar_cofarsur = tk.Button(root, text="Filtrar precios por Cofarsur", command=filtrar_precios_cofarsur)
btn_filtrar_cofarsur.pack(pady=5)

btn_filtrar_delsud = tk.Button(root, text="Filtrar precios por Del Sud", command=filtrar_precios_delsud)
btn_filtrar_delsud.pack(pady=5)

root.mainloop()
