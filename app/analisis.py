import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    def __init__(self, data):
        self.df = pd.read_csv(data)  

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

#Gráfico de barras de número de participantes por talle
    def barras_participante_taller(self):
        plt.figure(figsize=(8, 6))  # Establece tamaño de figura
        sns.countplot(
            data=self.df,
            x="taller_inscrito",
            order=self.df["taller_inscrito"].value_counts().index,
            palette="viridis" 
        )
        plt.title('Número de Participantes por Taller')
        plt.xlabel('Taller Inscrito')
        plt.ylabel('Número de Participantes')
        plt.xticks(rotation=45)
        plt.tight_layout() 
        plt.show()
    
  
  
    def histograma_edades(self):
        plt.figure(figsize=(8, 6))
        
        sns.histplot(
            data=self.df,
            x="edad",
            bins=range(self.df["edad"].min(), self.df["edad"].max() + 1),  # Un bin por edad exacta
            color="skyblue"
        )
        
        # Establecer ticks en X con todos los valores posibles de edad
        plt.xticks(range(self.df["edad"].min(), self.df["edad"].max() + 1))  

        plt.title('Distribución de Edades de Participantes')
        plt.xlabel('Edad')
        plt.ylabel('Cantidad')
        plt.tight_layout()
        plt.show()

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
        plt.axis("equal")  # Hace que el gráfico sea un círculo perfecto
        plt.tight_layout()
        plt.show()


data = DataAnalyzer("app\participantes.csv") 
print(data.summary())
print("El total de participantes es:",data.total_participantes())
print("El promedio de pagos:",data.promedio_pagos_taller())
print("El taller mayor es:", data.taller_mayor())
print("Partcipante con mayoy pago",data.participante_mayor_valor_pagado()["nombre"])
data.grafico_circular()
