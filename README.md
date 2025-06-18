# MiDato

¿Sabías que el 70% de los pequeños comercios toma decisiones sin basarse en datos?

En un entorno cada vez más competitivo, donde las grandes cadenas usan datos para optimizar cada decisión, los negocios familiares siguen trabajando a ciegas.

Este tema me toca de cerca: mi padre tiene un pequeño negocio en el pueblo. Tras años de esfuerzo, se enfrentaba a desafios como el exceso de stock o la toma de decisiones por intuición, por lo que cuando me introduje en el mundo de los datos, vi una gran oportunidad.

Analicé la información de sus ventas y descubrí que productos se venden más, en qué momentos del año, y cuáles se compran juntos. Así nació MiDato, una app web fácil de usar que traduce los datos en decisiones inteligentes.

Ahora se compra y vende de manera estratégica, se entiende al cliente y se lanzan promociones más efectivas.
En pocas palabras, MiDato permite a un pequeño comercio usar los datos como lo haría una gran cadena como Amazon

¿El resultado? Más claridad, menos errores y un aumento potencial de hasta un 30% en las ventas

Para mí, este proyecto no es solo una solución técnica, es personal. Nació de querer ayudar a mi padre, y ahora quiero que MiDato ayude a muchos más como él.

A diferencia de herramientas costosas y genéricas, MiDato es accesible y está pensada desde la realidad del pequeño comercio.
Con MiDato, la ciencia de datos es una aliada del comercio local y cualquier tienda, por pequeña que sea, toma decisiones como una gran empresa. Con datos, no con suerte.

# Streamlit App con Modelos de Recomendación y Predicción

Este proyecto consiste en una aplicación web desarrollada con [Streamlit](https://streamlit.io/) que integra dos modelos de machine learning:

- **Modelo de Recomendación:** Sugerencias personalizadas basadas en tickets de compra.
- **Modelo de Predicción:** Predicción de ventas mensuales a partir de artículos introducidos por el usuario.

## Demo

Puedes ejecutar la aplicación localmente con el siguiente comando:

```bash
streamlit run app.py
```

## Estructura del proyecto

📁 streamlit/
│
├── app.py  
├── models/
│ ├── modelo_recomendador.py
│ └── modelo_predictivo.py
├── pages/
│ ├── \_1_Recomendador.py
│ └── \_2_Predictor.py
├── requirements.txt  
└── README.md
