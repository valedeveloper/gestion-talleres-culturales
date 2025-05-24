import tkinter as tk
from tkinter import messagebox
from tkinter import font
from logica import GestionParticipantes
from analisis import DataAnalyzer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk
import matplotlib.pyplot as plt

participantes = GestionParticipantes()

#Crear ventana principal
base = tk.Tk()
base.title("Gestor de Participantes")
base.geometry("1200x600")
base.resizable(False, False)

#Fuente en negrita para etiquetas
negrita = font.Font(weight="bold")

#Entradas
tk.Label(base, text="Nombre:", font=negrita).grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(base)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(base, text="Edad:", font=negrita).grid(row=1, column=0, padx=5, pady=5)
entry_edad = tk.Entry(base)
entry_edad.grid(row=1, column=1, padx=5, pady=5)

opciones_taller = ["Pintura", "Teatro", "Musica", "Danza"]
entry_taller_inscrito = tk.StringVar(base)
entry_taller_inscrito.set(opciones_taller[0])  #Valor por defecto
menu_taller_inscrito = tk.OptionMenu(base,entry_taller_inscrito, *opciones_taller)
menu_taller_inscrito.grid(row=2, column=1, padx=5, pady=5)


tk.Label(base, text="Mes de participación:", font=negrita).grid(row=3, column=0, padx=5, pady=5)
entry_mes_participacion = tk.Entry(base)
entry_mes_participacion.grid(row=3, column=1, padx=5, pady=5)

tk.Label(base, text="Clases asistidas:", font=negrita).grid(row=4, column=0, padx=5, pady=5)
entry_clases_asistidas = tk.Entry(base)
entry_clases_asistidas.grid(row=4, column=1, padx=5, pady=5)


tk.Label(base, text="Buscar por Id:", font=negrita).grid(row=5, column=0, padx=5, pady=5)
entry_id_participante = tk.Entry(base)
entry_id_participante.grid(row=5, column=1, padx=5, pady=5)

#Area de texto para mostrar participantes
text_area = tk.Text(base, height=15, width=120)
text_area.grid(row=6, column=0, columnspan=4, padx=5, pady=10)

#Funciones
def agregar_participante():
    nombre = entry_nombre.get().strip()
    edad = entry_edad.get().strip()
    taller_inscrito = entry_taller_inscrito.get()
    mes = entry_mes_participacion.get().strip()
    clases = entry_clases_asistidas.get().strip()

    if not all([nombre, edad, taller_inscrito, mes, clases]):
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return

    participantes.añadir_participante(nombre, edad, taller_inscrito, mes, clases)
    messagebox.showinfo("Éxito", "Participante registrado.")
    mostrar_participantes()
    limpiar_campos()

def editar_participante():
    id=entry_id_participante.get()
    nombre = entry_nombre.get().strip()
    edad = entry_edad.get().strip()
    taller_inscrito = entry_taller_inscrito.get()
    mes = entry_mes_participacion.get().strip()
    clases = entry_clases_asistidas.get().strip()

    if not all([id,nombre, edad, taller_inscrito, mes, clases]):
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
        return
    resultado=participantes.modificar_participante(id,nombre, edad, taller_inscrito, mes, clases)

    if resultado:
        messagebox.showinfo("Éxito", "Participante modificado.")
    else:
        messagebox.showwarning("Aviso", "No existen registros de este ID")
    limpiar_campos()
    mostrar_participantes()

def eliminar_participante():
    id=entry_id_participante.get()
    if not id:
        messagebox.showwarning("Campos vacío", "Por favor ingrese el ID a eliminar.")
        return

    resultado=participantes.eliminar_receta_por_id(id)

    if resultado:
        messagebox.showinfo("Éxito", "Participante eliminado.")
    else:
        messagebox.showwarning("Aviso", "No existen registros de este ID")
    limpiar_campos()
    mostrar_participantes()


def mostrar_participantes():
    text_area.delete("1.0", tk.END)
    df = participantes.mostrar_participantes()
    if not df.empty:
        text_area.insert(tk.END, df.to_string(index=False))
    else:
        text_area.insert(tk.END, "No hay participantes registrados.")

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_id_participante.delete(0,tk.END)
    entry_mes_participacion.delete(0, tk.END)
    entry_clases_asistidas.delete(0, tk.END)

def mostrar_busqueda():
    id = entry_id_participante.get().strip()
    if not id:
        messagebox.showwarning("Falta ID", "Por favor ingresa un ID para buscar.")
        return
    resultado = participantes.buscar_participante(id)
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, resultado)

def mostrar_analisis():
    try:
        #Ventana emergente https://www.geeksforgeeks.org/python-tkinter-toplevel-widget/
        analisis_window = tk.Toplevel(base)
        analisis_window.title("Análisis de Datos")
        analisis_window.geometry("1000x700")
        
        # https://www.geeksforgeeks.org/access-the-actual-tab-widget-of-ttknotebook-in-python-tkinter/
        notebook = ttk.Notebook(analisis_window)
        
        tab_reporte = ttk.Frame(notebook)
        text_reporte = tk.Text(tab_reporte, wrap=tk.WORD, font=("Times New Roman", 10))
        scroll = tk.Scrollbar(tab_reporte, command=text_reporte.yview)
        text_reporte.configure(yscrollcommand=scroll.set)
        
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text_reporte.pack(expand=True, fill=tk.BOTH)
        
        tab_graficos = ttk.Frame(notebook)
        
        main_frame = ttk.Frame(tab_graficos)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        notebook.add(tab_reporte, text="Reporte")
        notebook.add(tab_graficos, text="Gráficos")
        notebook.pack(expand=True, fill=tk.BOTH)
        
        analyzer = DataAnalyzer("app/participantes.csv")
        reporte = analyzer.generar_reporte_completo()
        text_reporte.insert(tk.END, reporte)
        
        if not analyzer.df.empty:
            #Grafico de barras
            fig1 = analyzer.barras_participante_taller()
            canvas1 = FigureCanvasTkAgg(fig1, master=scrollable_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
            
            #Histograma 
            fig2 = analyzer.histograma_edades()
            canvas2 = FigureCanvasTkAgg(fig2, master=scrollable_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
            
            #Grafico circular
            fig3 = analyzer.grafico_circular()
            canvas3 = FigureCanvasTkAgg(fig3, master=scrollable_frame)
            canvas3.draw()
            canvas3.get_tk_widget().pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
            
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el análisis: {str(e)}")

#Frame para los botones
frame_botones = tk.Frame(base, bg="#E1E1E1", padx=20, pady=20)
frame_botones.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
#Botones
tk.Button(frame_botones, text="Registrar Participante", bg="#F17134", command=agregar_participante).grid(row=0, column=0, padx=16, pady=5)
tk.Button(frame_botones, text="Editar Participante", bg="#F17134", command=editar_participante).grid(row=0, column=1, padx=16, pady=5)
tk.Button(frame_botones, text="Eliminar Participante", bg="#F17134", command=eliminar_participante).grid(row=0, column=2, padx=16, pady=5)
tk.Button(frame_botones, text="Mostrar Participantes", bg="#F17134", command=mostrar_participantes).grid(row=0, column=3, padx=16, pady=5)
tk.Button(frame_botones, text="Buscar participante", bg="#F17134", command=mostrar_busqueda).grid(row=0, column=4, padx=16, pady=5)
tk.Button(frame_botones, text="Análisis", bg="#4CAF50", command=mostrar_analisis).grid(row=0, column=5, padx=10, pady=5)




#Mostrar recetas automaticamente al cargar
df_recetas = participantes.mostrar_participantes()
if not df_recetas.empty :
    texto_tabla = df_recetas.to_string(index=False)
    columnas_recetas = df_recetas.columns
    # encabezado = "  ".join([str(col).upper() for col in columnas_recetas])
    # text_area.insert(tk.END, f"{encabezado}\n")
    text_area.insert(tk.END, texto_tabla)
else:
    text_area.insert(tk.END, "No hay Participantes Registrados.")
base.mainloop()
