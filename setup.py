import sys
from cx_Freeze import setup, Executable

includes = ["datetime", "requests", "locale", "pymysql", "time"]

exe = Executable(
    script="main.py",  # Seu arquivo principal
    base=None,  # Normalmente, None ou "Console" para aplicativos de console
    #targetName="gaica",  # Nome do executável de saída
    icon=None,  # Ícone do aplicativo (opcional)
)

setup(
    name="Gaica",
    version="1.0",
    description="App Protótipo de leitura",
    options={"build_exe": {"includes": includes}},
    executables=[exe],
)
