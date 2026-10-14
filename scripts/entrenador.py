import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from conexion import obtener_conexion

conexion=obtener_conexion()
df_vino=pd.read_sql("SELECT * FROM vino",conexion)

#SEPARAR VARIABLES "X","y" (alta calidad = calificación de 7 o más)
X=df_vino.drop(columns=['id','tipo','calidad'])
y=(df_vino['calidad']>=7).map({True:'alta',False:'baja'})
print(f"VINOS DE ALTA CALIDAD: {(y=='alta').sum()} | BAJA CALIDAD: {(y=='baja').sum()}")

#DIVIDIR 80% ENTRENAMIENTO Y 20% PRUEBA PARA MEDIR EL MODELO
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=42,stratify=y)

#RANDOM FOREST: muchos árboles que votan; "balanced" compensa que hay pocos vinos de alta calidad
def crear_modelo():
    return RandomForestClassifier(n_estimators=200,class_weight='balanced',random_state=42)

modelo_prueba=crear_modelo()
modelo_prueba.fit(X_train,y_train)
predicciones=modelo_prueba.predict(X_test)
print(f"EFECTIVIDAD CON LOS VINOS DE PRUEBA: {accuracy_score(y_test,predicciones)*100:.2f}%")
print(classification_report(y_test,predicciones))

print("ENTRENANDO EL MODELO FINAL CON TODOS LOS VINOS")
modelo_produccion=crear_modelo()
modelo_produccion.fit(X,y)
joblib.dump(modelo_produccion,Path(__file__).parent.parent/'modelo'/'vino.joblib',compress=3)
print("MODELO GUARDADO EN modelo/vino.joblib")
