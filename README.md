# Registro de Talleres Culturales Comunitarios 🎨🎭🎶💃

Sistema de gestión para registrar, analizar y visualizar datos de participación en talleres culturales de una casa de la cultura. Este proyecto fue desarrollado como parte del Proyecto Integrador para la materia de programación orientada a objetos.

## 🧠 Objetivo
Crear una aplicación interactiva que permita:
- Registrar datos de participantes en talleres de pintura, teatro, música y danza.
- Gestionar asistencias mensuales y calcular valores pagados por taller.
- Visualizar estadísticas y gráficos que faciliten el análisis de participación.

## 🧰 Tecnologías y Librerías
- `Python 3.x`
- `Tkinter` – Interfaz gráfica
- `Pandas` – Manipulación de datos
- `Matplotlib` – Visualización de datos
- `Git/GitHub` – Control de versiones
- `Programación Orientada a Objetos (POO)` – Estructura del código

## 📋 Funcionalidades
### Interfaz gráfica
- Registro de participantes (nombre, edad, taller, mes, clases asistidas).
- Botones para:
  - Registrar nuevo participante
  - Modificar datos existentes
  - Eliminar participante
  - Mostrar todos los registros
  - Generar reportes estadísticos

### Lógica interna (POO)
- `Clase Participante`: almacena y gestiona datos individuales.
- `Clase Analisis`: realiza operaciones de análisis estadístico y generación de reportes.

### Reportes (Pandas + Matplotlib)
- Total de participantes registrados.
- Participantes con datos incompletos.
- Promedio de pagos por taller.
- Taller con mayor número de participantes.
- Participante con mayor valor pagado.
- Gráficos:
  - Barras: número de participantes por taller
  - Histograma: edades
  - Circular: distribución de participantes por taller

