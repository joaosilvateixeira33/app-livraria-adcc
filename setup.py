# Programa de configuração para o cx_Freeze poder "Buildar"
import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "includes": ["tkinter"], "include_files": ["logo.png", "cadastro.png", "importar.png", "lista.png", "livro.png", "quantidade.png", "sair.png", "livros.ico"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Livraria Adcc",
    version="1.0",
    description="Programa voltado para biblioteca seminario teologico adcc",
    options={"build_exe": build_exe_options},
    executables=[Executable(script="biblioteca_adcc.py", base=base,icon="livros.ico")]
)

# Fim Config