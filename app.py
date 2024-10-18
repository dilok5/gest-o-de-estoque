import tkinter as tk
from tkinter import messagebox
import pymysql

# Conexão com o banco de dados MySQL
def conectar_bd():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='gtr3253',  # Ajuste sua senha MySQL
        db='estoque_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Função para adicionar produto
def adicionar_produto():
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    preco = entry_preco.get()

    if nome and quantidade and preco:
        conn = conectar_bd()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM produtos WHERE nome = %s', (nome,))
            produto = cursor.fetchone()

            if produto:
                nova_quantidade = produto['quantidade'] + int(quantidade)
                cursor.execute('UPDATE produtos SET quantidade = %s WHERE nome = %s', (nova_quantidade, nome))
            else:
                cursor.execute('INSERT INTO produtos (nome, quantidade, preco) VALUES (%s, %s, %s)', (nome, quantidade, preco))
        
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado/atualizado no estoque!")
        listar_produtos()
    else:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

# Função para remover produto
def remover_produto():
    nome = entry_nome.get()

    if nome:
        conn = conectar_bd()
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM produtos WHERE nome = %s', (nome,))
        
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", f"Produto '{nome}' removido do estoque.")
        listar_produtos()
    else:
        messagebox.showerror("Erro", "O nome do produto é necessário.")

# Função para listar produtos
def listar_produtos():
    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
    
    conn.close()

    listbox_produtos.delete(0, tk.END)

    if produtos:
        for produto in produtos:
            listbox_produtos.insert(tk.END, f"{produto['nome']} - {produto['quantidade']} unidades - R${produto['preco']}")
    else:
        listbox_produtos.insert(tk.END, "Estoque vazio.")

# Interface gráfica usando Tkinter
app = tk.Tk()
app.title("Sistema de Gestão de Estoque")

# Labels e entradas para cadastro de produtos
tk.Label(app, text="Nome do Produto").grid(row=0, column=0)
entry_nome = tk.Entry(app)
entry_nome.grid(row=0, column=1)

tk.Label(app, text="Quantidade").grid(row=1, column=0)
entry_quantidade = tk.Entry(app)
entry_quantidade.grid(row=1, column=1)

tk.Label(app, text="Preço").grid(row=2, column=0)
entry_preco = tk.Entry(app)
entry_preco.grid(row=2, column=1)

# Botões de ação
tk.Button(app, text="Adicionar Produto", command=adicionar_produto).grid(row=3, column=0, columnspan=2)
tk.Button(app, text="Remover Produto", command=remover_produto).grid(row=4, column=0, columnspan=2)

# Listbox para exibir os produtos
listbox_produtos = tk.Listbox(app, width=50, height=10)
listbox_produtos.grid(row=5, column=0, columnspan=2)

# Inicializar a lista de produtos
listar_produtos()

app.mainloop()
