import sqlite3
import customtkinter as ct
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from tkinter import filedialog
from PIL import ImageTk, Image

livros = sqlite3.connect('livros.db')
emprestimo = sqlite3.connect('emprestimo.db')

cursor_livros = livros.cursor()
cursor_emprestimo = emprestimo.cursor()

cursor_livros.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        titulo VARCHAR(255),
        autor VARCHAR(255),
        ano INT,
        quantidade INT
    )
""")

cursor_emprestimo.execute("""
    CREATE TABLE IF NOT EXISTS emprestimos (
        nome_cliente VARCHAR(100),
        livro_emprestado VARCHAR(100),
        data_emprestimo DATE
    )
""")

livros.commit()
emprestimo.commit()

def adicionar_livro():
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    ano = entry_ano.get()
    quantidade = entry_quantidade.get()

    # Inserir o livro no banco de dados
    cursor_livros.execute("INSERT INTO livros (titulo, autor, ano, quantidade) VALUES ('"+titulo+"', '"+autor+"','"+str(ano)+"', '"+str(quantidade)+"')")
    livros.commit()
    
    # Limpar os campos de entrada
    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    entry_ano.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)

    messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")

def fechar_conexao():
    # Fechar a conexão com o banco de dados
    janela.destroy()

def listar_livros():
    cursor = cursor_livros
    cursor.execute("SELECT titulo, autor, ano, quantidade FROM livros")
    livros = cursor.fetchall()

    # Criar a janela de exibição dos livros
    janela_livros = tk.Toplevel(janela)
    janela_livros.title("Lista de Livros")
    janela_livros.geometry("900x900")

    # Criar uma árvore (Treeview) para exibir os livros
    tree_livros = ttk.Treeview(janela_livros)
    tree_livros["columns"] = ("Título", "Autor", "Ano", "Quantidade")
    tree_livros.column("#0", width=0, stretch=tk.NO)
    tree_livros.column("Título", width=150, anchor=tk.W)
    tree_livros.column("Autor", width=150, anchor=tk.W)
    tree_livros.column("Ano", width=70, anchor=tk.CENTER)
    tree_livros.column("Quantidade", width=80, anchor=tk.CENTER)

    tree_livros.heading("#0", text="", anchor=tk.W)
    tree_livros.heading("Título", text="Título", anchor=tk.W)
    tree_livros.heading("Autor", text="Autor", anchor=tk.W)
    tree_livros.heading("Ano", text="Ano", anchor=tk.CENTER)
    tree_livros.heading("Quantidade", text="Quantidade", anchor=tk.CENTER)

    tree_livros.pack(fill=tk.BOTH, expand=True)

    # Adicionar os livros à árvore
    for livro in livros:
        tree_livros.insert("", tk.END, values=livro)

def quantidade_livros():
    # Consultar quantidade de livros no banco de dados
    cursor_livros.execute("SELECT COUNT(*) FROM livros")
    quantidade = cursor_livros.fetchone()[0]

    messagebox.showinfo("Quantidade de Livros", f"Total de Livros: {quantidade}")

def abrir_janela_cadastro():
    def exibir_emprestimos():
        # Consultar empréstimos no banco de dados
        cursor = cursor_emprestimo
        cursor.execute("SELECT * FROM emprestimos")
        emprestimos = cursor.fetchall()

        tree_emprestimo = ttk.Treeview(janela_cadastro)
        tree_emprestimo["columns"] = ("Nome", "Titulo", "Data")
        tree_emprestimo.column("Nome", width=150, anchor=tk.W)
        tree_emprestimo.column("Titulo", width=150, anchor=tk.W)
        tree_emprestimo.column("Data", width=70, anchor=tk.CENTER)

        tree_emprestimo.heading("Nome", text="Nome", anchor=tk.W)
        tree_emprestimo.heading("Titulo", text="Titulo", anchor=tk.W)
        tree_emprestimo.heading("Data", text="Data", anchor=tk.CENTER)

        tree_emprestimo.pack(fill=tk.BOTH, expand=True)

        # Adicionar os livros à árvore
        for novo in emprestimos:
            tree_emprestimo.insert("", tk.END, values=novo)

    def cadastrar_emprestimo():
        cursor = cursor_emprestimo
        nome_cliente = entry_nome_cliente.get()
        livro_emprestado = entry_livro_emprestado.get()
        data_emprestimo = entry_data_emprestimo.get()

        # Inserir os dados do empréstimo no banco de dados
        cursor = cursor_emprestimo
        cursor.execute("INSERT INTO emprestimos (nome_cliente, livro_emprestado, data_emprestimo) VALUES ('"+nome_cliente+"', '"+livro_emprestado+"','"+data_emprestimo+"')")
        emprestimo.commit()

        # Limpar os campos de entrada
        entry_nome_cliente.delete(0, tk.END)
        entry_livro_emprestado.delete(0, tk.END)
        entry_data_emprestimo.delete(0, tk.END)

        # Exibir mensagem de sucesso
        messagebox.showinfo("Cadastro de Empréstimo", "Empréstimo cadastrado com sucesso!")

    # Criar a janela de cadastro de empréstimo
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Cadastro de Empréstimo")
    janela_cadastro.geometry("600x600")


    # Criar rótulos e campos de entrada para nome do cliente, livro emprestado e data de empréstimo
    label_nome_cliente = ct.CTkLabel(janela_cadastro, text="Nome do Cliente:")
    label_nome_cliente.pack()
    entry_nome_cliente = ct.CTkEntry(janela_cadastro)
    entry_nome_cliente.pack()

    label_livro_emprestado = ct.CTkLabel(janela_cadastro, text="Livro Emprestado:")
    label_livro_emprestado.pack()
    entry_livro_emprestado = ct.CTkEntry(janela_cadastro)
    entry_livro_emprestado.pack()

    label_data_emprestimo = ct.CTkLabel(janela_cadastro, text="Data de Empréstimo:")
    label_data_emprestimo.pack()
    entry_data_emprestimo = ct.CTkEntry(janela_cadastro)
    entry_data_emprestimo.pack()

    # Criar botão para cadastrar empréstimo
    btn_cadastrar_emprestimo = ct.CTkButton(janela_cadastro, text="Cadastrar Empréstimo", command=cadastrar_emprestimo)
    btn_cadastrar_emprestimo.pack(padx=5, pady=5)

    btn_exibir_emprestimos = ct.CTkButton(janela_cadastro, text="Exibir Empréstimos", command=exibir_emprestimos)
    btn_exibir_emprestimos.pack()

    # Manter a janela aberta
    janela_cadastro.mainloop()

def importar_livro():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])

    # Verificar se o usuário selecionou um arquivo
    if not caminho_arquivo:
        return

    # Abrir o arquivo Excel usando o pandas
    try:
        df = pd.read_excel(caminho_arquivo)
    except FileNotFoundError:
        tk.messagebox.showerror("Erro", "Arquivo não encontrado")
        return

    # Verificar se o arquivo possui as colunas corretas
    if "Título" not in df.columns or "Autor" not in df.columns or "Ano" not in df.columns or "Quantidade" not in df.columns:
        tk.messagebox.showerror("Erro", "O arquivo Excel não possui as colunas corretas")
        return

    # Iterar sobre os registros e inserir no banco de dados
    cursor = cursor_livros
    for _, row in df.iterrows():
        titulo = row["Título"]
        autor = row["Autor"]
        ano = row["Ano"]
        quantidade = row["Quantidade"]

        cursor.execute("INSERT INTO livros (titulo, autor, ano, quantidade) VALUES ('"+titulo+"', '"+str(autor)+"','"+str(ano)+"', '"+str(quantidade)+"')")

    livros.commit()

    # Exibir mensagem de sucesso
    tk.messagebox.showinfo("Importar Livros", "Livros importados com sucesso!")


# Janela principal
janela = tk.Tk()
janela.iconbitmap('livros.ico')
janela.title("Biblioteca ADCC")
janela.geometry("400x400")

#imagens dos botoes
imagem_igreja = ct.CTkImage(Image.open("logo.png"), size=(100, 100))
imagem_adicionar = ct.CTkImage(Image.open("livro.png"))
imagem_listar = ct.CTkImage(Image.open("lista.png"))
imagem_quantidade = ct.CTkImage(Image.open("quantidade.png"))
imagem_emprestimo = ct.CTkImage(Image.open("cadastro.png"))
imagem_importar = ct.CTkImage(Image.open("importar.png"))
imagem_sair = ct.CTkImage(Image.open("sair.png"))

#  fonts
font_textos =("Arial", 12, "bold")
font_botoes =("calibre", 12, "bold")

# Criar os campos de entrada e rótulos
rotulo_logo = ct.CTkLabel(janela, text=" ", image=imagem_igreja)
rotulo_logo.grid(row=0, column=0, pady=5)
texto_logo = ct.CTkLabel(janela, text="ASSEMBLÉIA DE DEUS\nMINISTERIO CENTRAL DE COSMOS")
texto_logo.grid(row=0, column=1)

titulo_livro = ct.CTkLabel(janela, text="Titulo do Livro:", font=font_textos)
titulo_livro.grid(row=1, column=0, pady=4, padx=0)
entry_titulo = ct.CTkEntry(janela, height=4)
entry_titulo.grid(row=1, column=1)

autor_livro = ct.CTkLabel(janela, text="Autor do livro:", font=font_textos)
autor_livro.grid(row=2, column=0, pady=4)
entry_autor = ct.CTkEntry(janela,  height=4)
entry_autor.grid(row=2, column=1)

ano_livro = ct.CTkLabel(janela, text="Ano do Livro:", font=font_textos)
ano_livro.grid(row=3, column=0, pady=4)
entry_ano = ct.CTkEntry(janela, height=4)
entry_ano.grid(row=3, column=1)

livro_quantidade = ct.CTkLabel(janela, text="Quantidade:", font=font_textos)
livro_quantidade.grid(row=4, column=0, pady=4)
entry_quantidade = ct.CTkEntry(janela, height=4)
entry_quantidade.grid(row=4, column=1)

# Botões
btn_adicionar = ct.CTkButton(janela, text="Adicionar Livro", command=adicionar_livro, image=imagem_adicionar, font=font_botoes)
btn_adicionar.grid(row=5, column=0, padx=4)

btn_listar = ct.CTkButton(janela, text="Listar Livros", command=listar_livros, image=imagem_listar, font=font_botoes)
btn_listar.grid(row=5, column=1, padx=5, pady=5)

btn_quantidade = ct.CTkButton(janela, text="Quantidade", command=quantidade_livros, image=imagem_quantidade, font=font_botoes)
btn_quantidade.grid(row=6, column=0)

btn_abrir_janela_cadastro = ct.CTkButton(janela, text="Empréstimo", command=abrir_janela_cadastro, image=imagem_emprestimo, font=font_botoes)
btn_abrir_janela_cadastro.grid(row=6, column=1)

btn_importar_livros = ct.CTkButton(janela, text="Importar Livros", command=importar_livro, image=imagem_importar, font=font_botoes)
btn_importar_livros.grid(row=7, column=0, pady=5)

# Criar botão para fechar a aplicação
btn_fechar = ct.CTkButton(janela, text="Fechar", command=fechar_conexao, image=imagem_sair, font=font_botoes)
btn_fechar.grid(row=7, column=1)

janela.mainloop()