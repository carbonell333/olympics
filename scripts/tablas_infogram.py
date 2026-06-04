"""
Generacion de tablas para Infogram.

Este script prepara las tablas finales utilizadas en la visualizacion
storytelling del proyecto "Canon biometrico del atleta olimpico".

Para ejecutarlo desde la raiz del proyecto:

    python scripts/tablas_infogram.py

Los archivos generados se guardan en:

    data/processed/

Si se ejecuta de nuevo, los archivos existentes se sobrescriben.
"""

import pandas as pd

from utilidades import (
    obtener_raiz_proyecto,
    cargar_datos,
    crear_variables_derivadas,
    crear_grupo_disciplina,
    filtrar_biometria,
    exportar_csv,
)

def traducir_sexo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Traduce la variable Sex a etiquetas en castellano.
    """
    df = df.copy()
    df["Sexo"] = df["Sex"].map({
        "M": "Hombres",
        "F": "Mujeres"
    })
    return df


def crear_resumen_dataset(df: pd.DataFrame, df_bio: pd.DataFrame) -> pd.DataFrame:
    """
    Crea una tabla resumen con indicadores generales del dataset.
    """
    resumen = pd.DataFrame(
        {
            "Indicador": [
                "Registros tras eliminar duplicados",
                "Atletas unicos",
                "Periodo inicial",
                "Periodo final",
                "Deportes",
                "Registros biometricos desde 1960",
            ],
            "Valor": [
                len(df),
                df["ID"].nunique(),
                df["Year"].min(),
                df["Year"].max(),
                df["Sport"].nunique(),
                len(df_bio),
            ],
        }
    )

    return resumen


def crear_contexto_participacion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea tabla de contexto con numero de atletas unicos y porcentaje de mujeres
    por año olimpico.

    Para mantener la coherencia con el analisis biometrico principal,
    se utilizan solo los Juegos Olimpicos de verano.
    """
    df_summer = df[df["Season"] == "Summer"].copy()

    df_unicos = df_summer.drop_duplicates(subset=["Year", "ID"])

    contexto = (
        df_unicos
        .groupby("Year")
        .agg(
            atletas=("ID", "nunique"),
            porcentaje_mujeres=("Sex", lambda x: round((x == "F").mean() * 100, 2)),
        )
        .reset_index()
    )

    return contexto


def crear_cobertura_biometrica(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la cobertura de altura y peso por decada.
    Sirve para justificar el filtro temporal desde 1960.
    """
    cobertura = (
        df
        .groupby("Decada")
        .agg(
            registros=("ID", "count"),
            con_altura=("Height", lambda x: x.notna().sum()),
            con_peso=("Weight", lambda x: x.notna().sum()),
            con_altura_y_peso=(
                "ID",
                lambda x: df.loc[x.index, ["Height", "Weight"]].notna().all(axis=1).sum(),
            ),
        )
        .reset_index()
    )

    cobertura["porcentaje_altura_y_peso"] = round(
        cobertura["con_altura_y_peso"] / cobertura["registros"] * 100,
        2
    )

    return cobertura


def crear_altura_peso_disciplina(df_bio: pd.DataFrame) -> pd.DataFrame:
    """
    Crea tabla con medianas de altura y peso por disciplina y sexo.
    Pensada para un scatter plot en Infogram.
    """
    tabla = (
        df_bio
        .groupby(["Disciplina", "Sexo"])
        .agg(
            altura_mediana=("Height", "median"),
            peso_mediano=("Weight", "median"),
            imc_mediano=("IMC", "median"),
            n=("ID", "count"),
        )
        .reset_index()
    )

    tabla["altura_mediana"] = round(tabla["altura_mediana"], 1)
    tabla["peso_mediano"] = round(tabla["peso_mediano"], 1)
    tabla["imc_mediano"] = round(tabla["imc_mediano"], 2)

    return tabla


def crear_bmi_disciplina_sexo(df_bio: pd.DataFrame) -> pd.DataFrame:
    """
    Crea tabla individual de IMC por disciplina y sexo.
    Esta tabla permite crear distribuciones, boxplots o violin plots.
    """
    columnas = ["ID", "Name", "Year", "Sexo", "Disciplina", "IMC", "Medallista"]
    tabla = df_bio[columnas].copy()
    tabla["IMC"] = round(tabla["IMC"], 2)
    return tabla


def crear_bmi_resumen_disciplina_sexo(df_bio: pd.DataFrame) -> pd.DataFrame:
    """
    Crea resumen de IMC por disciplina y sexo.
    Sirve para etiquetas o graficos agregados.
    """
    tabla = (
        df_bio
        .groupby(["Disciplina", "Sexo"])
        .agg(
            n=("ID", "count"),
            imc_mediano=("IMC", "median"),
            imc_q1=("IMC", lambda x: x.quantile(0.25)),
            imc_q3=("IMC", lambda x: x.quantile(0.75)),
        )
        .reset_index()
    )

    for col in ["imc_mediano", "imc_q1", "imc_q3"]:
        tabla[col] = round(tabla[col], 2)

    return tabla


def crear_edad_disciplina(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea tabla individual de edad para disciplinas seleccionadas.
    """
    deportes_edad = [
        "Rhythmic Gymnastics",
        "Swimming",
        "Gymnastics",
        "Athletics",
        "Weightlifting",
        "Fencing",
        "Shooting",
        "Equestrianism",
    ]

    nombres_es = {
        "Rhythmic Gymnastics": "Gimnasia ritmica",
        "Swimming": "Natacion",
        "Gymnastics": "Gimnasia",
        "Athletics": "Atletismo",
        "Weightlifting": "Halterofilia",
        "Fencing": "Esgrima",
        "Shooting": "Tiro",
        "Equestrianism": "Equitacion",
    }

    tabla = df[
        (df["Sport"].isin(deportes_edad))
        & df["Age"].notna()
    ][["ID", "Name", "Year", "Sexo", "Sport", "Age"]].copy()
 
    tabla["Disciplina"] = tabla["Sport"].map(nombres_es)
    tabla = tabla.drop(columns=["Sport"])

    return tabla


def crear_edad_resumen_disciplina(df_edad: pd.DataFrame) -> pd.DataFrame:
    """
    Crea resumen de edad por disciplina.
    """
    tabla = (
        df_edad
        .groupby("Disciplina")
        .agg(
            n=("ID", "count"),
            edad_mediana=("Age", "median"),
            edad_q1=("Age", lambda x: x.quantile(0.25)),
            edad_q3=("Age", lambda x: x.quantile(0.75)),
            edad_minima=("Age", "min"),
            edad_maxima=("Age", "max"),
        )
        .reset_index()
    )

    return tabla


def crear_delta_bmi_medallistas(df_bio: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la diferencia de IMC mediano entre medallistas y no medallistas.

    Delta IMC = IMC mediano de medallistas - IMC mediano de no medallistas.
    """
    resumen = (
        df_bio
        .groupby(["Disciplina", "Sexo", "Medallista"])
        .agg(
            imc_mediano=("IMC", "median"),
            n=("ID", "count"),
        )
        .reset_index()
    )

    tabla = resumen.pivot_table(
        index=["Disciplina", "Sexo"],
        columns="Medallista",
        values="imc_mediano"
    ).reset_index()

    tabla = tabla.rename(columns={
        False: "imc_no_medallistas",
        True: "imc_medallistas",
    })

    tabla["delta_imc"] = tabla["imc_medallistas"] - tabla["imc_no_medallistas"]

    for col in ["imc_no_medallistas", "imc_medallistas", "delta_imc"]:
        tabla[col] = round(tabla[col], 2)

    return tabla


def main() -> None:
    """
    Ejecuta todo el flujo de preparacion y exportacion de tablas.
    """
    raiz = obtener_raiz_proyecto()

    ruta_raw = raiz / "data" / "raw" / "olympics.csv"
    ruta_processed = raiz / "data" / "processed"

    print("Cargando datos...")
    df = cargar_datos(ruta_raw)

    print("Creando variables derivadas...")
    df = crear_variables_derivadas(df)
    df = crear_grupo_disciplina(df, incluir_baloncesto=False)
    df = traducir_sexo(df)

    print("Filtrando datos biometricos...")
    df_bio = filtrar_biometria(df)

    print("Creando tablas para Infogram...")

    resumen_dataset = crear_resumen_dataset(df, df_bio)
    contexto_participacion = crear_contexto_participacion(df)
    cobertura_biometrica = crear_cobertura_biometrica(df)
    altura_peso = crear_altura_peso_disciplina(df_bio)
    bmi_individual = crear_bmi_disciplina_sexo(df_bio)
    bmi_resumen = crear_bmi_resumen_disciplina_sexo(df_bio)
    edad_individual = crear_edad_disciplina(df)
    edad_resumen = crear_edad_resumen_disciplina(edad_individual)
    delta_bmi = crear_delta_bmi_medallistas(df_bio)

    print("Exportando CSV...")

    exportar_csv(resumen_dataset, ruta_processed / "resumen_dataset.csv")
    exportar_csv(contexto_participacion, ruta_processed / "contexto_participacion.csv")
    exportar_csv(cobertura_biometrica, ruta_processed / "cobertura_biometrica_por_decada.csv")
    exportar_csv(altura_peso, ruta_processed / "altura_peso_disciplina.csv")
    exportar_csv(bmi_individual, ruta_processed / "bmi_disciplina_sexo.csv")
    exportar_csv(bmi_resumen, ruta_processed / "bmi_resumen_disciplina_sexo.csv")
    exportar_csv(edad_individual, ruta_processed / "edad_disciplina.csv")
    exportar_csv(edad_resumen, ruta_processed / "edad_resumen_disciplina.csv")
    exportar_csv(delta_bmi, ruta_processed / "delta_bmi_medallistas.csv")

    print("Proceso completado.")
    print(f"Tablas exportadas en: {ruta_processed}")


if __name__ == "__main__":
    main()