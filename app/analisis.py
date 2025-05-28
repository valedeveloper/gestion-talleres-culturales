import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    def __init__(self, data):
        try:
            self.df = pd.read_csv(data)
        except FileNotFoundError:
            # Crea la base de datos 
            self.df = pd.DataFrame(columns=[
                "id", "nombre", "edad", "taller_inscrito", 
                "mes_participacion", "clases_asistidas", 
                "valor_clase", "total_pagado"
            ]) 
        

    def summary(self):
        buffer = io.StringIO()  
        self.df.info(buf=buffer) 
        salida = buffer.getvalue()
        salida_describe = self.df.describe(include='all').to_string()
        salida += "\n\n" + salida_describe
        return salida
    def total_participantes(self):
        return len(self.df)
    def promedio_pagos_taller(self):
        return np.mean(self.df["total_pagado"])

#https://interactivechaos.com/es/manual/tutorial-de-pandas/el-metodo-valuecounts
    def taller_mayor(self):
        conteo = self.df["taller_inscrito"].value_counts()
        if not conteo.empty:
            taller = conteo.idxmax()
            cantidad = conteo.max()
            return taller, cantidad
        else:
            return "No hay datos", 0
    
    def participante_mayor_valor_pagado(self):
        max_fila = self.df.loc[self.df['total_pagado'].idxmax()]
        return max_fila

#Grafico de barras
    def barras_participante_taller(self):
        plt.figure(figsize=(8, 6))
        sns.countplot(
            data=self.df,
            x="taller_inscrito",
            order=self.df["taller_inscrito"].value_counts().index,
            # palette="viridis" 
        )
        plt.title('Número de Participantes por Taller')
        plt.xlabel('Taller Inscrito')
        plt.ylabel('Número de Participantes')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt.gcf() 
    
  
  
    def histograma_edades(self):
        plt.figure(figsize=(8, 6))
        sns.histplot(
            data=self.df,
            x="edad",
            bins=range(self.df["edad"].min(), self.df["edad"].max() + 1),
            color="skyblue"
        )
        plt.xticks(range(self.df["edad"].min(), self.df["edad"].max() + 1))
        plt.title('Distribución de Edades de Participantes')
        plt.xlabel('Edad')
        plt.ylabel('Cantidad')
        plt.tight_layout()
        return plt.gcf()

#https://www.geeksforgeeks.org/how-to-create-a-pie-chart-in-seaborn/
    def grafico_circular(self):
        plt.figure(figsize=(8, 6))
        conteo_talleres = self.df["taller_inscrito"].value_counts()
        plt.pie(
            conteo_talleres, 
            labels=conteo_talleres.index, 
            autopct='%1.1f%%', 
            colors=sns.color_palette("pastel") 
        )
        plt.title("Distribución de Participantes por Taller")
        plt.axis("equal")
        plt.tight_layout()
        return plt.gcf() 

    def generar_reporte_completo(self):
        """Genera un reporte unificado con todas las métricas"""
        reporte = ""
        if not self.df.empty:
            #Resumen
            buffer = io.StringIO()
            self.df.info(buf=buffer)
            reporte = buffer.getvalue() + "\n\n"
            reporte += self.df.describe(include='all').to_string()
            
            reporte += f"\n\n=== Métricas Clave ===\n"
            reporte += f"Total participantes: {len(self.df)}\n"
            reporte += f"Promedio de pagos: ${np.mean(self.df['total_pagado']):.2f}\n"
            
            taller, cantidad = self.taller_mayor()
            reporte += f"Taller más popular: {taller} ({cantidad} participantes)\n"
            
            participante_max = self.participante_mayor_valor_pagado()
            reporte += f"Mayor pago: {participante_max['nombre']} (${participante_max['total_pagado']})\n"
        else:
            reporte = "No hay datos para analizar."
        return reporte

if __name__ == "__main__": # esta es para poder hacer las pruebas que y que no nos muestre error al ejecutar interfaz ya que estas son solo pruebas
 ## https://docs.python.org/3/library/__main__.html
 data = DataAnalyzer("participantes.csv") 
 print(data.summary())
 print("El total de participantes es:",data.total_participantes())
 print("El promedio de pagos:",data.promedio_pagos_taller())
 print("El taller mayor es:", data.taller_mayor())
 print("Partcipante con mayor pago",data.participante_mayor_valor_pagado()["nombre"])
#data.grafico_circular()
