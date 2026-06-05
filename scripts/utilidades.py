"""
Funciones auxiliares para preparar los datos del proyecto
"Canon biometrico del atleta olimpico".

Este modulo contiene funciones reutilizables para:
- cargar y limpiar el dataset original,
- calcular variables derivadas,
- clasificar disciplinas deportivas,
- filtrar los datos biometricos,
- exportar tablas para Flourish.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def obtener_raiz_proyecto() -> Path:
    """
    Devuelve la ruta raiz del proyecto a partir de la ubicacion del script.
    Esto evita usar rutas absolutas y permite ejecutar el codigo en cualquier ordenador.
    """
    return Path(__file__).resolve().parents[1]


def cargar_datos(ruta_csv: Path) -> pd.DataFrame:
    """
    Carga el dataset original y elimina duplicados exactos.
    """
    df = pd.read_csv(ruta_csv)
    df = df.drop_duplicates()
    return df


def crear_variables_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea variables derivadas necesarias para el analisis:
    - Medallista: indica si el atleta obtuvo medalla.
    - IMC: indice de masa corporal.
    - Decada: decada olimpica.
    """
    df = df.copy()

    df["Medallista"] = df["Medal"].notna()

    df["IMC"] = df["Weight"] / ((df["Height"] / 100) ** 2)

    df["Decada"] = (df["Year"] // 10) * 10

    return df


def clasificar_atletismo(evento: str) -> str:
    """
    Clasifica eventos de atletismo en subgrupos mas homogeneos.

    La categoria Athletics del dataset original es muy heterogenea, por lo que
    se subdivide en velocidad, resistencia y lanzamientos. El resto de pruebas
    de atletismo se dejan fuera del analisis biometrico principal.
    """
    if pd.isna(evento):
        return np.nan

    evento = str(evento).lower()

    # Velocidad: pruebas cortas, vallas cortas y relevos
    patrones_velocidad = [
        "100 metres", "200 metres", "400 metres",
        "100 metres hurdles", "110 metres hurdles", "400 metres hurdles",
        "4 x 100 metres relay", "4 x 400 metres relay"
    ]

    # Resistencia: medio fondo, fondo, maraton y obstaculos
    patrones_resistencia = [
        "800 metres", "1,500 metres", "1500 metres",
        "5,000 metres", "5000 metres",
        "10,000 metres", "10000 metres",
        "marathon", "3,000 metres steeplechase", "3000 metres steeplechase"
    ]

    # Lanzamientos
    patrones_lanzamientos = [
        "shot put", "discus throw", "hammer throw", "javelin throw"
    ]

    if any(patron in evento for patron in patrones_velocidad):
        return "Atletismo - Velocidad"

    if any(patron in evento for patron in patrones_resistencia):
        return "Atletismo - Resistencia"

    if any(patron in evento for patron in patrones_lanzamientos):
        return "Atletismo - Lanzamientos"

    return np.nan


def crear_grupo_disciplina(df: pd.DataFrame, incluir_baloncesto: bool = True) -> pd.DataFrame:
    """
    Crea una variable de disciplina agrupada para el analisis biometrico.

    Se seleccionan disciplinas con perfiles fisicos contrastados:
    - Gimnasia
    - Natacion
    - Halterofilia
    - Baloncesto, opcional
    - Atletismo subdividido en velocidad, resistencia y lanzamientos
    """
    df = df.copy()
    df["Disciplina"] = pd.Series(pd.NA, index=df.index, dtype="string")

    df.loc[df["Sport"] == "Gymnastics", "Disciplina"] = "Gimnasia"
    df.loc[df["Sport"] == "Swimming", "Disciplina"] = "Natacion"
    df.loc[df["Sport"] == "Weightlifting", "Disciplina"] = "Halterofilia"

    if incluir_baloncesto:
        df.loc[df["Sport"] == "Basketball", "Disciplina"] = "Baloncesto"

    mask_atletismo = df["Sport"] == "Athletics"
    df.loc[mask_atletismo, "Disciplina"] = df.loc[mask_atletismo, "Event"].apply(
        clasificar_atletismo
    )

    return df


def filtrar_biometria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra el dataset para los analisis biometricos.

    Se restringe a partir de 1960 porque la cobertura de altura y peso
    es mucho mas consistente desde esa decada.
    """
    columnas_necesarias = ["Height", "Weight", "Age", "IMC", "Disciplina"]

    df_bio = df[
        (df["Year"] >= 1960)
        & df[columnas_necesarias].notna().all(axis=1)
    ].copy()

    return df_bio


def exportar_csv(df: pd.DataFrame, ruta_salida: Path) -> None:
    """
    Exporta un DataFrame a CSV usando utf-8-sig para mejorar compatibilidad
    con Excel e Flourish.
    """
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")
