from flask import Flask, request, render_template
import pandas as pd
import joblib
from pathlib import Path
app=Flask(__name__)
#carga el modelo cuando se inicia el servidor
CARPETA=Path(__file__).parent
modelo=joblib.load(CARPETA.parent/'modelo'/'vino.joblib')

TIPOS=['Tinto','Blanco']

#campos del formulario: (columna del modelo, etiqueta, unidad)
CAMPOS=[
    ('acidez_fija','Acidez fija','g/L'),
    ('acidez_volatil','Acidez volátil','g/L'),
    ('acido_citrico','Ácido cítrico','g/L'),
    ('azucar_residual','Azúcares residuales','g/L'),
    ('cloruros','Cloruros','g/L'),
    ('dioxido_azufre_libre','Dióxido de azufre libre','mg/L'),
    ('dioxido_azufre_total','Dióxido de azufre total','mg/L'),
    ('densidad','Densidad','g/cm³'),
    ('ph','pH',''),
    ('sulfatos','Sulfatos','g/L'),
    ('alcohol','Alcohol','% vol'),
]
def leer_vino(formulario):
    #recibir datos del formulario en el mismo orden que usó el modelo al entrenar
    datos={columna:[float(formulario[columna])] for columna,_,_ in CAMPOS}
    return pd.DataFrame(datos)[modelo.feature_names_in_]


def generar_insights(tipo, valores):
    try:
        valores_num = {clave: float(valor) for clave, valor in valores.items() if valor not in ('', None)}
    except (TypeError, ValueError):
        return []

    alcohol = valores_num.get('alcohol', 0)
    densidad = valores_num.get('densidad', 0)
    ph = valores_num.get('ph', 0)
    azucar = valores_num.get('azucar_residual', 0)
    sulfatos = valores_num.get('sulfatos', 0)
    acidez = valores_num.get('acidez_fija', 0)

    insights = []

    if alcohol >= 12.5:
        insights.append('Tiene un alcohol alto, lo que suele dar un vino con más cuerpo y personalidad.')
    elif alcohol < 10:
        insights.append('El alcohol es moderado, por lo que el perfil tiende a sentirse más ligero y fresco.')

    if densidad > 0.995:
        insights.append('La densidad es alta y sugiere un vino más intenso y con mayor estructura.')
    elif densidad < 0.990:
        insights.append('La densidad baja indica un perfil más ligero y más aerodinámico.')

    if ph < 3.3:
        insights.append('La acidez es marcada, lo que suele reforzar la frescura y la vibración del vino.')
    elif ph > 3.7:
        insights.append('El pH es más suave, por lo que el vino puede sentirse menos ácido y más redondo.')

    if azucar < 1.5:
        insights.append('Los azúcares residuales son bajos, así que el vino se percibe menos dulce.')
    elif azucar > 2.2:
        insights.append('Hay un nivel de azúcar más notable, lo que puede dar un perfil más dulce.')

    if sulfatos > 0.6:
        insights.append('Los sulfatos están altos, lo que ayuda a la estabilidad y la conservación del vino.')

    if tipo == 'Tinto' and alcohol >= 11.5:
        insights.append('Como es tinto, este nivel de alcohol puede reforzar su carácter más intenso y profundo.')
    elif tipo == 'Blanco' and acidez > 6.2:
        insights.append('Como es blanco, la acidez fuerte puede encajar muy bien con una sensación fresca y cítrica.')

    return insights[:3] if insights else ['La composición está bien equilibrada, con un perfil estable y uniforme.']


@app.route('/', methods=['GET'])
def inicio():
    tipo=request.args.get('tipo','Tinto')
    return render_template('index.html',campos=CAMPOS,tipos=TIPOS,tipo=tipo,valores={})

@app.route('/predecir', methods=['POST'])
def predecir():
    tipo=request.form.get('tipo','Tinto')
    valores=request.form.to_dict()
    try:
        df=leer_vino(request.form)
    except (KeyError,ValueError):
        return render_template('index.html',campos=CAMPOS,tipos=TIPOS,tipo=tipo,
                               valores=valores,
                               error='Revisa los datos: todos los campos deben ser números.')
    #prediccion y que tan seguro está el modelo
    prediccion=modelo.predict(df)[0]
    probabilidad=modelo.predict_proba(df)[0][list(modelo.classes_).index(prediccion)]
    insights=generar_insights(tipo, valores)
    return render_template('index.html',campos=CAMPOS,tipos=TIPOS,tipo=tipo,
                           valores=valores,
                           prediccion=prediccion,
                           probabilidad=round(probabilidad*100),
                           insights=insights)

if __name__=='__main__':
    app.run(debug=True)
