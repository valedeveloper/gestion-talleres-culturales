import pandas as pd
import os
import csv

clase_precios = {
    "Pintura": 6000,
    "Teatro": 8000,
    "Musica": 10000,
    "Danza": 7000
}

class Participante:
    def __init__(self, id, nombre, edad, taller_inscrito, mes_participacion, clases_asistidas):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.taller_inscrito = taller_inscrito
        self.mes_participacion = mes_participacion
        self.clases_asistidas = clases_asistidas

    def calcular_pago(self):
        valor_clase = clase_precios.get(self.taller_inscrito, 0)
        return valor_clase * int(self.clases_asistidas)

    def reporte_participante(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edad": self.edad,
            "taller_inscrito": self.taller_inscrito,
            "mes_participacion": self.mes_participacion,
            "clases_asistidas": self.clases_asistidas,
            "valor_clase": clase_precios.get(self.taller_inscrito, 0),
            "total_pagado": self.calcular_pago()
        }


class GestionParticipantes:
   
    def __init__(self, archivo='app/participantes.csv'):
        self.archivo = archivo
        self.contador_id = self.obtener_ultimo_id() + 1
        self.campos = ["id", "nombre", "edad", "taller_inscrito", "mes_participacion","clases_asistidas", "valor_clase", "total_pagado"
]

    def mostrar_participantes(self):
        if os.path.isfile(self.archivo):
            return pd.read_csv(self.archivo)
        else:
            return pd.DataFrame(columns=self.campos)

    def añadir_participante(self, nombre, edad, taller_inscrito, mes_participacion, clases_asistidas):
        nuevo = Participante(self.contador_id, nombre, edad, taller_inscrito, mes_participacion, clases_asistidas)
        participante=nuevo.reporte_participante()
        print(participante)
        with open(self.archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.campos)
            if os.path.getsize(self.archivo) == 0:
                writer.writeheader()
            writer.writerow(nuevo.reporte_participante())
        self.contador_id += 1
    
    def modificar_participante(self, id, nombre, edad, taller_inscrito, mes_participacion, clases_asistidas):
        df=self.mostrar_participantes()
        df['id'] = df['id'].astype(str)
        id = str(id)
        if id in df['id'].values:
            df.loc[df['id'] == id, 'nombre'] = nombre
            df.loc[df['id'] == id, 'edad'] = edad
            df.loc[df['id'] == id, 'taller_inscrito'] = taller_inscrito
            df.loc[df['id'] == id, 'mes_participacion'] = mes_participacion
            df.loc[df['id'] == id, 'clases_asistidas'] = clases_asistidas

            df.to_csv(self.archivo, index=False)
            return True  
        
        else:
            return False
    
    def eliminar_receta_por_id(self, id_eliminar):
        df=self.mostrar_participantes()
        df['id'] = df['id'].astype(str)
        id = str(id_eliminar)

        if id_eliminar in df['id'].values:
            participantes = df[df['id'] != id_eliminar]  
            participantes.to_csv(self.archivo, index=False) 
            return True
        else:
            return False

    # def actualizar_archivo(self):
    #     return self.mostrar_participantes()
    
    def obtener_ultimo_id(self):
        if os.path.isfile(self.archivo):
             df = self.mostrar_participantes()
             if not df.empty:
                 return df["id"].max()
        return 0
