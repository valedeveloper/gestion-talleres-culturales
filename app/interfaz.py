import tkinter as tk
from tkinter import messagebox
from tkinter import font
from logica import GestionParticipantes

participantes = GestionParticipantes()

# Crear ventana principal
base = tk.Tk()
base.title("Gestor de Participantes")
base.geometry("800x600")
base.resizable(False, False)

# Fuente en negrita para etiquetas
negrita = font.Font(weight="bold")

# Entradas
tk.Label(base, text="Nombre:", font=negrita).grid(row=0, column=0, padx=5, pady=5)
entry_nombre = tk.Entry(base)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(base, text="Edad:", font=negrita).grid(row=1, column=0, padx=5, pady=5)
entry_edad = tk.Entry(base)
entry_edad.grid(row=1, column=1, padx=5, pady=5)

opciones_taller = ["Pintura", "Teatro", "Musica", "Danza"]
entry_taller_inscrito = tk.StringVar(base)
entry_taller_inscrito.set(opciones_taller[0])  # Valor por defecto
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

# Área de texto para mostrar participantes
text_area = tk.Text(base, height=15, width=120)
text_area.grid(row=6, column=0, columnspan=4, padx=5, pady=10)

# Funciones
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

# Botones
tk.Button(base, text="Registrar Participante", bg="#90EE90", command=agregar_participante).grid(row=8, column=0, columnspan=2, padx=5, pady=5)
tk.Button(base, text="Editar Participante", bg="#ADD8E6", command=editar_participante).grid(row=9, column=0, columnspan=2, padx=5, pady=5)
tk.Button(base, text="Eliminar Participante", bg="#ADD8E6", command=eliminar_participante).grid(row=8, column=1, columnspan=2, padx=5, pady=5)
tk.Button(base, text="Mostrar Participantes", bg="#ADD8E6", command=mostrar_participantes).grid(row=9, column=1, columnspan=2, padx=5, pady=5)




# Mostrar recetas automáticamente al cargar
df_recetas = participantes.mostrar_participantes()
if not df_recetas.empty :
    texto_tabla = df_recetas.to_string(index=False)
    columnas_recetas = df_recetas.columns
    # encabezado = "  ".join([str(col).upper() for col in columnas_recetas])
    # text_area.insert(tk.END, f"{encabezado}\n")
    text_area.insert(tk.END, texto_tabla)
else:
    text_area.insert(tk.END, "No hay Participantes Registrados.")
# Ejecutar app
base.mainloop()
