import tkinter as tk
from tkinter import filedialog, messagebox


current_grid_data = []

def mostrar_reporte(title, contenido):
    ventana_reporte = tk.Toplevel(ventana1)
    ventana_reporte.title(f"Reporte - {title}")
    texto_widget = tk.Text(ventana_reporte, wrap="none", width=80, height=20)
    texto_widget.insert(tk.END, contenido)
    texto_widget.config(state=tk.DISABLED)
    texto_widget.pack(padx=10,pady=10)
                     
# TODO: implementar reportes
def listado_alumnos():
    if not current_grid_data:
        messagebox.showinfo("Reporte", "No hay datos cargados.")
        return
    reporte = "Alumno\tMateria\tNota 1\tNota 2\tNota 3\tNota Final\n"
    for row in current_grid_data:
        reporte += "\t".join(row) + "\n"
    mostrar_reporte("Listado completo de alumnos", reporte)

def promedio_por_materia():
    if not current_grid_data:
        messagebox.showinfo("Reporte", "No hay datos cargados.")
        return
    materia_notas = {}
    for row in current_grid_data:
        materia = row[1]
        nota_final = float(row[5])
        if materia not in materia_notas:
            materia_notas[materia] = []
        materia_notas[materia].append(nota_final)
    reporte = "Materia\tPromedio\n"
    for materia, notas in materia_notas.items():
        promedio = sum(notas) / len(notas)
        reporte += f"{materia}\t{promedio:.2f}\n"
    mostrar_reporte("Promedio general por materia", reporte)

def alumnos_mayor():
    if not current_grid_data:
        messagebox.showinfo("Reporte", "No hay datos cargados.")
        return
    # Usar ventana personalizada para pedir el valor de alumnos mayores
    ventana_valor = tk.Toplevel(ventana1)
    ventana_valor.title("Ingrese valor de nota")
    tk.Label(ventana_valor, text="Mostrar alumnos con Nota Final mayor a:").pack(padx=10, pady=10)
    entrar_valor = tk.Entry(ventana_valor)
    entrar_valor.pack(padx=10, pady=5)
    entrar_valor.focus_set()

    def generar_reporte():
        try:
            valor = float(entrar_valor.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido.", parent=ventana_valor)
            return
        reporte = "Alumno\tMateria\tNota Final\n"
        for row in current_grid_data:
            if float(row[5]) > valor:
                reporte += f"{row[0]}\t{row[1]}\t{row[5]}\n"
        ventana_valor.destroy()
        mostrar_reporte(f"Alumnos con Nota Final mayor a {valor}", reporte)

    tk.Button(ventana_valor, text="Aceptar", command=generar_reporte).pack(pady=10)

def alumnos_menor():
    if not current_grid_data:
        messagebox.showinfo("Reporte", "No hay datos cargados.")
        return
    reporte = "Alumno\tMateria\tNota 1\tNota 2\tNota 3\n"
    for row in current_grid_data:
        notas = [float(row[2]), float(row[3]), float(row[4])]
        if any(nota < 4 for nota in notas):
            reporte += f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n"
    mostrar_reporte("Alumnos con al menos una nota menor a 4", reporte)

def apro_desaprobado():
    if not current_grid_data:
        messagebox.showinfo("Reporte", "No hay datos cargados.")
        return
    estadisticas = {}
    for row in current_grid_data:
        materia = row[1]
        nota_final = float(row[5])
        if materia not in estadisticas:
            estadisticas[materia] = {'aprobados': 0, 'desaprobados': 0}
        if nota_final >= 6:
            estadisticas[materia]['aprobados'] += 1
        else:
            estadisticas[materia]['desaprobados'] += 1
    reporte = "Materia\tAprobados\tDesaprobados\n"
    for materia, datos in estadisticas.items():
        reporte += f"{materia}\t{datos['aprobados']}\t{datos['desaprobados']}\n"
    mostrar_reporte("Aprobados y desaprobados por materia", reporte)

def encab_grid(frame):
    encabezado = ["Alumno", "Materia", "Nota 1", "Nota 2", "Nota 3", "Nota Final"]
    for col, header_text in enumerate(encabezado):
        header_label = tk.Label(frame, text=header_text, font=("Arial", 10, "bold"), relief="raised", padx=5, pady=5)
        header_label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
    return encabezado

def load_data_into_grid(frame, data):
    for widget in frame.winfo_children():
        widget.destroy()

    headers = encab_grid(frame)

    for row_idx, row_data in enumerate(data):
        for col_idx, cell_data in enumerate(row_data):
            celd_label = tk.Label(frame, text=str(cell_data), font=("Arial", 10), relief="groove", padx=5, pady=5)
            celd_label.grid(row=row_idx + 1, column=col_idx, sticky="nsew", padx=1, pady=1)

    for col in range(len(headers)):
        frame.grid_columnconfigure(col, weight=1)

def cargarDatosArchivo():
    global current_grid_data
    file_camin = filedialog.askopenfilename(
        title="Seleccionar archivo de alumnos",
        filetypes=[("Archivos CSV", "*.csv")]
    )
    if file_camin:
        try:
            with open(file_camin, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                datos_leidos = []
                for line in lines:
                    # Dividimos la línea por comas y la añadimos como tupla
                    partes = line.strip().split(',')
                    if len(partes) == 6: 
                        datos_leidos.append(tuple(partes))
                    else:
                        messagebox.showwarning("Advertencia de formato", f"Se omitió una línea con formato incorrecto (no 6 columnas): {line.strip()}")

            current_grid_data.extend(datos_leidos)
            load_data_into_grid(frame, current_grid_data)
            messagebox.showinfo("Carga exitosa", f"Datos cargados desde: {file_camin}")

        except Exception as e:
            messagebox.showerror("Error de lectura", f"No se pudo leer el archivo: {e}")
    else:
        print("Carga de archivo cancelada.")


def insertion_sort(arr, key_index, reverse=False, is_numeric=False):
    """
    Ordena una lista de tuplas usando el algoritmo de inserción.

    Args:
        arr (list): La lista de tuplas a ordenar.
        key_index (int): El índice de la columna por la cual ordenar.
        reverse (bool): Si es True, ordena en orden descendente.
        is_numeric (bool): Si es True, intenta convertir el valor de la clave a float para la comparación.
    """
    n = len(arr)
    for i in range(1, n):
        actual_item = arr[i]
        j = i - 1
        while j >= 0:
            val_j = arr[j][key_index]
            val_actual = actual_item[key_index]

            if is_numeric:
                try:
                    val_j = float(val_j)
                    val_actual = float(val_actual)
                except ValueError:
                    pass

            if reverse:
                if val_j < val_actual:
                    arr[j + 1] = arr[j]
                    j = j - 1
                else:
                    break
            else: # Orden ascendente
                if val_j > val_actual:
                    arr[j + 1] = arr[j]
                    j = j - 1
                else:
                    break
        arr[j + 1] = actual_item
    return arr

# --- Funciones de Ordenamiento ---
def ordenarPorNombre():
    global current_grid_data
    if not current_grid_data:
        messagebox.showinfo("Advertencia", "No hay datos para ordenar. Por favor, cargue un archivo primero.")
        return

    # El índice de la columna"Alumno" es 0
    # Orden alfabético ascendente
    sorted_data = insertion_sort(list(current_grid_data), key_index=0, reverse=False, is_numeric=False)
    current_grid_data = sorted_data # Actualiza la variable global
    load_data_into_grid(frame, current_grid_data) # Recarga la grilla con los datos ordenados
    messagebox.showinfo("Ordenamiento", "Datos ordenados por Nombre de Alumno.")

def ordenarPorNota():
    # TODO: reimplementar como burbuja
    global current_grid_data
    if not current_grid_data:
        messagebox.showinfo("Advertencia", "No hay datos para ordenar. Por favor, cargue un archivo primero.")
        return

    # El índice de la columna "Nota Final" es 5
    # Orden descendente (mayor a menor) y es numérico
    sorted_data = insertion_sort(list(current_grid_data), key_index=5, reverse=True, is_numeric=True)
    current_grid_data = sorted_data # Actualiza la variable global
    load_data_into_grid(frame, current_grid_data) # Recarga la grilla con los datos ordenados
    messagebox.showinfo("Ordenamiento", "Datos ordenados por Nota Final (Mayor a Menor).")


def abrir_dialogo_ingreso_manual():
    dialogo = tk.Toplevel(ventana1)
    dialogo.title("Ingreso Manual de Alumno")
    dialogo.geometry("350x300")
    dialogo.transient(ventana1) # Hace que el diálogo se muestre por encima de la ventana principal
    dialogo.grab_set() # Bloquea la interacción con la ventana principal mientras el diálogo está abierto
    dialogo.focus_set() # Pone el foco en el diálogo

    # Etiquetas y campos de entrada
    labels = ["Alumno:", "Materia:", "Nota 1:", "Nota 2:", "Nota 3:"]
    entries = {} # Diccionario para guardar las referencias a los Entry widgets

    for i, text in enumerate(labels):
        tk.Label(dialogo, text=text, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(dialogo)
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
        entries[text.replace(":", "").strip().replace(" ", "_").lower()] = entry # Guarda el Entry con un nombre clave

    # Función para guardar los datos ingresados
    def guardar_datos():
        global current_grid_data
        alumno = entries["alumno"].get().strip()
        materia = entries["materia"].get().strip()
        nota1_str = entries["nota_1"].get().strip()
        nota2_str = entries["nota_2"].get().strip()
        nota3_str = entries["nota_3"].get().strip()

        # Validar y convertir notas
        try:
            nota1 = float(nota1_str)
            nota2 = float(nota2_str)
            nota3 = float(nota3_str)


            if  not alumno:
                messagebox.showwarning("Error de Alumno", "Debe ingresar un nombre alumno.", parent=dialogo)
                return
            if  not materia:
                messagebox.showwarning("Error de Materia", "Debe ingresar una materia.", parent=dialogo)
                return


            # Validar rango de notas (ejemplo: 0 a 10)
            if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10 and 0 <= nota3 <= 10):
                messagebox.showwarning("Error de Nota", "Las notas deben estar entre 0 y 10.", parent=dialogo)
                return

            # Calcular Nota Final
            nota_final = round((nota1 + nota2 + nota3) / 3, 2) # Redondear a 2 decimales

            # Crear el nuevo registro del alumno
            new_student_data = (alumno, materia, str(int(nota1)), str(int(nota2)), str(int(nota3)), str(nota_final))
            # Convertimos notas a string para que coincida con el formato de carga de CSV

            current_grid_data.append(new_student_data) # Añadir a los datos existentes
            load_data_into_grid(frame, current_grid_data) # Actualizar la grilla
            messagebox.showinfo("Éxito", "Alumno guardado correctamente.", parent=dialogo)
            dialogo.destroy() # Cerrar el diálogo

        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingrese valores numéricos válidos para las notas.", parent=dialogo)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}", parent=dialogo)

    # Botones
    btn_guardar = tk.Button(dialogo, text="Guardar", command=guardar_datos)
    btn_guardar.grid(row=len(labels), column=0, padx=10, pady=10, sticky="ew")

    btn_cancelar = tk.Button(dialogo, text="Cancelar", command=dialogo.destroy)
    btn_cancelar.grid(row=len(labels), column=1, padx=10, pady=10, sticky="ew")

    dialogo.grid_columnconfigure(1, weight=1) # Hace que la columna de entrada se expanda


ventana1 = tk.Tk()
ventana1.geometry("600x400")
ventana1.title("Gestión de Calificaciones")


menubar1 = tk.Menu(ventana1)
ventana1.config(menu=menubar1)
opciones1 = tk.Menu(menubar1, tearoff=0)
opciones1.add_command(label="Cargar archivo", command=cargarDatosArchivo)
opciones1.add_command(label="Ingreso manual", command=abrir_dialogo_ingreso_manual)
menubar1.add_cascade(label="Ingresar Calificación", menu=opciones1)

opciones2 = tk.Menu(menubar1, tearoff=0)
opciones2.add_command(label="Listado completo de alumnos y sus notas con promedio", command=listado_alumnos)
opciones2.add_command(label="Promedio general por matereia", command=promedio_por_materia)
opciones2.add_command(label="Alumno con nota final mayor a valor un dado", command=alumnos_mayor)
opciones2.add_command(label="Alumno con nota menor a 4", command=alumnos_menor)
opciones2.add_command(label="Cantidad de aprobados y desaprobados por materias", command=apro_desaprobado)
menubar1.add_cascade(label="Elegir reporte", menu=opciones2) 

opciones3 = tk.Menu(menubar1, tearoff=0)
opciones3.add_command(label="Por Nombre Alumno", command=ordenarPorNombre)
opciones3.add_command(label="Por Nota Final", command=ordenarPorNota)
menubar1.add_cascade(label="Ordenar por", menu=opciones3) 

opciones4 = tk.Menu(menubar1, tearoff=0)
opciones4.add_command(label="Salir", command=ventana1.quit)
menubar1.add_cascade(label="Finalizar", menu=opciones4) 


frame = tk.Frame(ventana1, bg="lightgray", padx=10, pady=10) 
frame.pack(pady=20, fill="both", expand=True) 


encab_grid(frame)

ventana1.mainloop()
