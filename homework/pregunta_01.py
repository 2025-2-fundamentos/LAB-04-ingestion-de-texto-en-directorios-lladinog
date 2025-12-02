# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """

    import os
    import zipfile
    import pandas as pd

    ruta_zip = os.path.join("files", "input.zip")
    carpeta_input = os.path.join("files", "input")

    # Descomprimir solo si la carpeta aún no existe
    if not os.path.isdir(carpeta_input) and os.path.isfile(ruta_zip):
        with zipfile.ZipFile(ruta_zip, "r") as zf:
            zf.extractall("files")

    # Carpeta de salida dentro de files/
    carpeta_output = os.path.join("files", "output")
    os.makedirs(carpeta_output, exist_ok=True)

    def obtener_base_split(nombre_split: str) -> str:
        """
        Devuelve la ruta base donde están las carpetas 'train' o 'test'.

        Soporta las dos estructuras posibles:
        - files/input/train/...
        - files/input/input/train/...
        """
        candidato1 = os.path.join(carpeta_input, nombre_split)
        candidato2 = os.path.join(carpeta_input, "input", nombre_split)

        if os.path.isdir(candidato1):
            return candidato1
        if os.path.isdir(candidato2):
            return candidato2

        # Si ninguno existe, igual devolvemos candidato1 para que falle de forma clara
        return candidato1

    def construir_dataset(nombre_split):
        """
        Construye el DataFrame para 'train' o 'test'
        recorriendo las subcarpetas negative, neutral y positive.
        """
        base_split = obtener_base_split(nombre_split)
        filas = []

        for sentimiento in ["negative", "neutral", "positive"]:
            carpeta_sent = os.path.join(base_split, sentimiento)
            if not os.path.isdir(carpeta_sent):
                continue

            for archivo in sorted(os.listdir(carpeta_sent)):
                if not archivo.endswith(".txt"):
                    continue

                ruta_archivo = os.path.join(carpeta_sent, archivo)
                with open(ruta_archivo, encoding="utf-8") as f:
                    texto = f.read().strip()

                filas.append({"phrase": texto, "target": sentimiento})

        return pd.DataFrame(filas, columns=["phrase", "target"])

    # Construir y guardar los dos datasets
    df_train = construir_dataset("train")
    df_test = construir_dataset("test")

    df_train.to_csv(os.path.join(carpeta_output, "train_dataset.csv"), index=False)
    df_test.to_csv(os.path.join(carpeta_output, "test_dataset.csv"), index=False)
