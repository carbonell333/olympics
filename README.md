# Canon biométrico del atleta olímpico

## Perfil físico, disciplina y rendimiento en los Juegos Olímpicos

Este repositorio contiene el código utilizado para preparar los datos del proyecto de visualización **“Canon biométrico del atleta olímpico: perfil físico, disciplina y rendimiento en los Juegos Olímpicos”**, desarrollado a partir del dataset *120 Years of Olympic Athletes Dataset*.

La visualización final se realiza en **Flourish**, mientras que este repositorio recoge el proceso reproducible de limpieza, transformación y generación de las tablas utilizadas en dicha visualización.

[Enlace a la visualización](https://public.flourish.studio/story/3692812/)

## Objetivo del proyecto

El objetivo del proyecto es analizar cómo varía el perfil físico de los atletas olímpicos en función de la disciplina deportiva, el sexo, la edad y la obtención de medalla.

La idea de “canon biométrico” se utiliza como punto de partida narrativo para plantear si existe un perfil físico común en la élite olímpica o si, por el contrario, cada disciplina selecciona características corporales distintas.

La pregunta principal que guía la visualización es:

> ¿Existe un perfil biométrico común en la élite olímpica o cada disciplina deportiva selecciona cuerpos distintos?

A partir de esta pregunta, el proyecto explora diferencias en altura, peso, IMC y edad entre disciplinas, así como la posible relación entre el perfil biométrico y el rendimiento competitivo.

## Dataset original

El archivo original `olympics.csv` no se incluye en este repositorio por tamaño y por pertenecer a la fuente original.

Para ejecutar el procesamiento, debe descargarse desde Kaggle:

120 Years of Olympic Athletes Dataset  
https://www.kaggle.com/datasets/abdullahmeo/120-years-of-olympic-athletes-dataset/data

Una vez descargado, debe colocarse en:

```text
data/raw/olympics.csv
```

El archivo principal contiene información sobre atletas olímpicos desde 1896 hasta 2016. Cada fila representa la participación de un atleta en un evento olímpico concreto.

Las principales variables utilizadas son:

* `ID`: identificador único del atleta.
* `Name`: nombre del atleta.
* `Sex`: sexo del atleta.
* `Age`: edad.
* `Height`: altura en centímetros.
* `Weight`: peso en kilogramos.
* `Team`: equipo.
* `NOC`: Comité Olímpico Nacional.
* `Games`: edición de los Juegos.
* `Year`: año.
* `Season`: temporada.
* `City`: ciudad anfitriona.
* `Sport`: deporte.
* `Event`: evento o prueba.
* `Medal`: medalla obtenida, si procede.

## Estructura del repositorio

```text
olympic-athletes-visualization/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── olympics.csv
│   └── processed/
│       ├── resumen_dataset.csv
│       ├── contexto_participacion.csv
│       ├── cobertura_biometrica_por_decada.csv
│       ├── altura_peso_disciplina.csv
│       ├── bmi_disciplina_sexo.csv
│       ├── bmi_resumen_disciplina_sexo.csv
│       ├── edad_disciplina.csv
│       ├── edad_resumen_disciplina.csv
│       └── delta_bmi_medallistas.csv
│
├── scripts/
    ├── tablas_flourish.py
    └── utilidades.py

```

## Preparación de los datos

El procesamiento de los datos se realiza mediante scripts en Python. El flujo principal incluye:

1. Carga del dataset original.
2. Eliminación de duplicados exactos.
3. Creación de variables derivadas.
4. Cálculo del IMC.
5. Creación de una variable binaria de medallista.
6. Subdivisión de disciplinas deportivas, especialmente atletismo.
7. Filtrado de registros para análisis biométrico.
8. Exportación de tablas finales para Flourish.

## Variables derivadas

Durante el procesamiento se generan varias variables derivadas.

### `Medallista`

Variable booleana que indica si el atleta obtuvo medalla.

```text
True  = obtuvo medalla
False = no obtuvo medalla
```

### `IMC`

Índice de Masa Corporal, calculado a partir del peso y la altura:

```text
IMC = peso (kg) / altura (m)^2
```

Dado que la altura del dataset está expresada en centímetros, se convierte previamente a metros.

### `Decada`

Década olímpica correspondiente al año de participación.

### `Disciplina`

Variable creada para agrupar deportes seleccionados y facilitar la comparación biométrica entre perfiles físicos diferenciados.

Las disciplinas principales utilizadas son:

* Gimnasia
* Natacion
* Halterofilia
* Atletismo - Velocidad
* Atletismo - Resistencia
* Atletismo - Lanzamientos

## Subdivisión de atletismo

La categoría original `Athletics` agrupa eventos con demandas fisiológicas muy diferentes. Para evitar mezclar perfiles no comparables, se subdivide en tres grupos:

* **Atletismo - Velocidad**: pruebas cortas, vallas cortas y relevos.
* **Atletismo - Resistencia**: medio fondo, fondo, maratón y obstáculos.
* **Atletismo - Lanzamientos**: peso, disco, martillo y jabalina.

Esta transformación permite comparar perfiles biométricos más homogéneos dentro del atletismo.

## Restricción temporal del análisis biométrico

El análisis biométrico se restringe a partir de 1960.

Esta decisión se debe a que en las primeras décadas del dataset la disponibilidad de datos de altura y peso es reducida. A partir de 1960, la cobertura de estas variables aumenta de forma considerable, lo que permite realizar comparaciones más consistentes.

El contexto global de participación olímpica se calcula utilizando todo el dataset, pero los análisis de altura, peso e IMC se realizan únicamente con registros desde 1960 y con datos biométricos completos.

## Tablas generadas

Los archivos generados en `data/processed/` son los que se utilizan posteriormente en Flourish.

| Archivo                               | Descripción                                                   |
| ------------------------------------- | ------------------------------------------------------------- |
| `resumen_dataset.csv`                 | Indicadores generales del dataset.                            |
| `contexto_participacion.csv`          | Número de atletas únicos y porcentaje de mujeres por año.     |
| `cobertura_biometrica_por_decada.csv` | Cobertura de altura y peso por década.                        |
| `altura_peso_disciplina.csv`          | Medianas de altura, peso e IMC por disciplina y sexo.         |
| `bmi_disciplina_sexo.csv`             | Tabla individual de IMC por disciplina y sexo.                |
| `bmi_resumen_disciplina_sexo.csv`     | Resumen de IMC por disciplina y sexo.                         |
| `edad_disciplina.csv`                 | Tabla individual de edad para disciplinas seleccionadas.      |
| `edad_resumen_disciplina.csv`         | Resumen de edad por disciplina.                               |
| `delta_bmi_medallistas.csv`           | Diferencia de IMC mediano entre medallistas y no medallistas. |

## Visualización final

La visualización final se estructura como una pieza de storytelling visual en Flourish. El objetivo no es construir un dashboard exploratorio, sino una narrativa visual guiada en torno a una pregunta principal: si existe o no un canon biométrico común en los Juegos Olímpicos.

Cada bloque responde a una pregunta concreta:

| Bloque             | Pregunta                                                    | Datos utilizados             |
| ------------------ | ----------------------------------------------------------- | ---------------------------- |
| Contexto olímpico  | ¿Cómo ha cambiado la participación olímpica?                | `contexto_participacion.csv` |
| Altura y peso      | ¿Existen perfiles físicos distintos según deporte?          | `altura_peso_disciplina.csv` |
| IMC por disciplina | ¿Qué deportes concentran perfiles más ligeros o robustos?   | `bmi_disciplina_sexo.csv`    |
| Edad               | ¿Qué patrones de edad caracterizan a distintas disciplinas? | `edad_disciplina.csv`        |
| Medallas           | ¿El IMC diferencia a medallistas y no medallistas?          | `delta_bmi_medallistas.csv`  |

## Instalación

Para ejecutar el proyecto, se recomienda crear un entorno virtual de Python.

```bash
python -m venv venv
```

Activar el entorno virtual:

En Windows:

```bash
venv\Scripts\activate
```

En macOS/Linux:

```bash
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Para generar las tablas procesadas utilizadas en Flourish, ejecutar desde la raíz del proyecto:

```bash
python scripts/tablas_flourish.py
```

El script lee el archivo original desde:

```text
data/raw/olympics.csv
```

y exporta las tablas finales en:

```text
data/processed/
```

No se utilizan rutas absolutas, por lo que el proyecto puede ejecutarse en cualquier ordenador siempre que se mantenga la estructura de carpetas.

Si el script se ejecuta de nuevo, los archivos existentes en `data/processed/` se sobrescriben.

## Requisitos

Las dependencias necesarias se indican en `requirements.txt`.

Contenido recomendado:

```text
pandas
numpy
```

Si se utiliza el notebook de exploración inicial, pueden añadirse también:

```text
matplotlib
seaborn
jupyter
```

## Herramienta de visualización

La visualización final se desarrolla en **Flowrish**, utilizando las tablas procesadas generadas por los scripts de este repositorio.

Flourish se emplea para:

* diseñar la narrativa visual;
* integrar gráficos, textos e iconos;
* incorporar animaciones e interacción;
* publicar la visualización final online.

El código de este repositorio se centra exclusivamente en la preparación reproducible de los datos.

## Limitaciones

El proyecto presenta algunas limitaciones relevantes:

* El dataset llega hasta 2016 y no incluye ediciones olímpicas más recientes.
* La cobertura de altura y peso es limitada en las primeras décadas.
* El IMC no distingue entre masa muscular y masa grasa.
* Algunas disciplinas deportivas son internamente heterogéneas.
* El análisis es observacional y no permite establecer relaciones causales.
* La comparación entre medallistas y no medallistas se realiza dentro de atletas olímpicos, es decir, dentro de una población de élite.

## Licencia

Este proyecto incluye código propio para limpieza y transformación de datos. Se recomienda utilizar una licencia abierta, por ejemplo MIT, para el código del repositorio.

El dataset original pertenece a su fuente correspondiente y debe citarse según las condiciones indicadas en Kaggle.

## Autoría

Proyecto desarrollado como parte de una práctica de visualización de datos.

La visualización final se publica en Flourish y el presente repositorio recoge el flujo reproducible de preparación de datos.
