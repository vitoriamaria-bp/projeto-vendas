# Avaliação Continuada 4 - 1 ponto
# PROJETO DE VENDAS - parte 2
# Exercicios de CRUD completo (Produtos, Vendedores e Vendas)
# Entrega - dia 24/05/2026

from banco_de_dados.conexao import conectar, fechar_conexao
import mysql.connector

# PRODUTOS

def criar_produto():
    # Exercicio 1: cadastrar um novo produto na tabela produtos (descricao, preco).
    descricao_do_produto = input("Digite a descrição do produto: ")
    preco_do_produto = float(input("Digite o preço do produto: "))
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "INSERT INTO produtos (descricao, preco) VALUES (%s, %s)"
            cursor.execute(comando_sql, (descricao_do_produto, preco_do_produto))
            conexao.commit()
            print("Produto criado com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao criar produto: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def listar_produtos():
    # Exercicio 2: listar todos os produtos cadastrados com id, descricao e preco.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "SELECT id, descricao, preco FROM produtos"
            cursor.execute(comando_sql)
            lista_de_produtos = cursor.fetchall()
            for produto in lista_de_produtos:
                print(f"ID: {produto[0]} | Descrição: {produto[1]} | Preço: R$ {produto[2]:.2f}")
        except mysql.connector.Error as erro:
            print(f"Erro ao listar produtos: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def atualizar_produto():
    # Exercicio 3: atualizar descricao e/ou preco de um produto existente por id.
    listar_produtos()
    id_do_produto = int(input("Digite o ID do produto para atualizar: "))
    nova_descricao = input("Digite a nova descrição: ")
    novo_preco = float(input("Digite o novo preço: "))
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "UPDATE produtos SET descricao = %s, preco = %s WHERE id = %s"
            cursor.execute(comando_sql, (nova_descricao, novo_preco, id_do_produto))
            conexao.commit()
            print("Produto updated com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao atualizar produto: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def excluir_produto():
    # Exercicio 4: excluir um produto por id, treating dependencias em vendas_produtos.
    listar_produtos()
    id_do_produto = int(input("Digite o ID do produto para excluir: "))
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "DELETE FROM produtos WHERE id = %s"
            cursor.execute(comando_sql, (id_do_produto,))
            conexao.commit()
            print("Produto excluído com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao excluir produto: {erro}")
        cursor.close()
        fechar_conexao(conexao)


# VENDEDORES

def criar_vendedor():
    # Exercicio 5: cadastrar um novo vendedor na tabela vendedores.
    nome_do_vendedor = input("Digite o nome do vendedor: ")
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "INSERT INTO vendedores (nome) VALUES (%s)"
            cursor.execute(comando_sql, (nome_do_vendedor,))
            conexao.commit()
            print("Vendedor criado com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao criar vendedor: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def listar_vendedores():
    # Exercicio 6: listar todos os vendedores cadastrados.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "SELECT id, nome FROM vendedores"
            cursor.execute(comando_sql)
            lista_de_vendedores = cursor.fetchall()
            for vendedor in lista_de_vendedores:
                print(f"ID: {vendedor[0]} | Nome: {vendedor[1]}")
        except mysql.connector.Error as erro:
            print(f"Erro ao listar vendedores: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def atualizar_vendedor():
    # Exercicio 7: atualizar o nome de um vendedor existente por id.
    listar_vendedores()
    id_do_vendedor = int(input("Digite o ID do vendedor para atualizar: "))
    novo_nome = input("Digite o novo nome do vendedor: ")
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "UPDATE vendedores SET nome = %s WHERE id = %s"
            cursor.execute(comando_sql, (novo_nome, id_do_vendedor))
            conexao.commit()
            print("Vendedor atualizado com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao atualizar vendedor: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def excluir_vendedor():
    # Exercicio 8: excluir vendedor por id, validando se possui vendas vinculadas.
    listar_vendedores()
    id_do_vendedor = int(input("Digite o ID do vendedor para excluir: "))
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "DELETE FROM vendedores WHERE id = %s"
            cursor.execute(comando_sql, (id_do_vendedor,))
            conexao.commit()
            print("Vendedor excluído com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao excluir vendedor: {erro}")
        cursor.close()
        fechar_conexao(conexao)


# VENDAS

def criar_venda_com_itens():
    # Exercicio 9: criar uma venda e inserir itens na tabela vendas_produtos com quantidade e valores.
    listar_vendedores()
    id_do_vendedor = int(input("Digite o ID do vendedor para a venda: "))
    desconto_da_venda = float(input("Digite o valor do desconto: "))
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql_venda = "INSERT INTO vendas (id_vendedor, data_e_hora, desconto, valor_final) VALUES (%s, NOW(), %s, 0)"
            cursor.execute(comando_sql_venda, (id_do_vendedor, desconto_da_venda))
            id_da_venda = cursor.lastrowid
            listar_produtos()
            total_da_venda = 0
            while True:
                id_do_produto = int(input("Digite o ID do produto (ou 0 para terminar os itens): "))
                if id_do_produto == 0:
                    break
                quantidade_vendida = int(input("Digite a quantidade: "))
                cursor.execute("SELECT preco FROM produtos WHERE id = %s", (id_do_produto,))
                resultado_preco = cursor.fetchone()
                if resultado_preco:
                    valor_unitario = resultado_preco[0]
                    valor_total_item = valor_unitario * quantidade_vendida
                    total_da_venda = total_da_venda + valor_total_item
                    comando_sql_item = "INSERT INTO vendas_produtos (id_venda, id_produto, quantidade, valor_unitario, valor_total) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(comando_sql_item, (id_da_venda, id_do_produto, quantidade_vendida, valor_unitario, valor_total_item))
                else:
                    print("Produto não encontrado.")
            valor_final_calculado = total_da_venda - desconto_da_venda
            if valor_final_calculado < 0:
                valor_final_calculado = 0
            comando_sql_atualizar = "UPDATE vendas SET valor_final = %s WHERE id = %s"
            cursor.execute(comando_sql_atualizar, (valor_final_calculado, id_da_venda))
            conexao.commit()
            print("Venda e itens registrados com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao criar venda: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def listar_vendas_completas():
    # Exercicio 10: listar vendas com vendedor e itens (produto, quantidade, valor_unitario, valor_total).
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando_sql = "SELECT vendas.id, vendedores.nome, vendas.data_e_hora, vendas.desconto, vendas.valor_final, produtos.descricao, vendas_produtos.quantidade, vendas_produtos.valor_unitario, vendas_produtos.valor_total FROM vendas INNER JOIN vendedores ON vendas.id_vendedor = vendedores.id INNER JOIN vendas_produtos ON vendas.id = vendas_produtos.id_venda INNER JOIN produtos ON vendas_produtos.id_produto = produtos.id"
            cursor.execute(comando_sql)
            lista_de_vendas = cursor.fetchall()
            print("\n--- Relatório de Vendas Completas ---")
            for venda in lista_de_vendas:
                print(f"Venda ID: {venda[0]} | Vendedor: {venda[1]} | Data: {venda[2]} | Desconto: R$ {venda[3]:.2f} | Total: R$ {venda[4]:.2f} | Produto: {venda[5]} | Qtd: {venda[6]} | Unitário: R$ {venda[7]:.2f} | Total Item: R$ {venda[8]:.2f}")
        except mysql.connector.Error as erro:
            print(f"Erro ao listar vendas completas: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def atualizar_venda_e_itens():
    # Exercicio 11: atualizar dados de uma venda (desconto/valor_final) e seus itens.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT id, id_vendedor, valor_final FROM vendas")
            lista_de_vendas = cursor.fetchall()
            for venda in lista_de_vendas:
                print(f"ID Venda: {venda[0]} | ID Vendedor: {venda[1]} | Valor Final Atual: R$ {venda[2]:.2f}")
            id_da_venda = int(input("Digite o ID da venda que deseja atualizar: "))
            novo_desconto = float(input("Digite o novo valor do desconto: "))
            cursor.execute("SELECT SUM(valor_total) FROM vendas_produtos WHERE id_venda = %s", (id_da_venda,))
            resultado_soma = cursor.fetchone()
            if resultado_soma and resultado_soma[0] is not None:
                total_dos_itens = resultado_soma[0]
                novo_valor_final = total_dos_itens - novo_desconto
                if novo_valor_final < 0:
                    novo_valor_final = 0
                comando_sql = "UPDATE vendas SET desconto = %s, valor_final = %s WHERE id = %s"
                cursor.execute(comando_sql, (novo_desconto, novo_valor_final, id_da_venda))
                conexao.commit()
                print("Venda atualizada com sucesso!")
            else:
                print("Venda não encontrada ou não possui itens.")
        except mysql.connector.Error as erro:
            print(f"Erro ao atualizar venda: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def excluir_venda():
    # Exercicio 12: excluir uma venda por id removendo primeiro os itens de vendas_produtos.
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT id, valor_final FROM vendas")
            lista_de_vendas = cursor.fetchall()
            for venda in lista_de_vendas:
                print(f"ID Venda: {venda[0]} | Valor Final: R$ {venda[1]:.2f}")
            id_da_venda = int(input("Digite o ID da venda para excluir: "))
            comando_sql_itens = "DELETE FROM vendas_produtos WHERE id_venda = %s"
            cursor.execute(comando_sql_itens, (id_da_venda,))
            comando_sql_venda = "DELETE FROM vendas WHERE id = %s"
            cursor.execute(comando_sql_venda, (id_da_venda,))
            conexao.commit()
            print("Venda e seus itens excluídos com sucesso!")
        except mysql.connector.Error as erro:
            print(f"Erro ao excluir venda: {erro}")
        cursor.close()
        fechar_conexao(conexao)


def menu():
    opcoes = {
        "1": ("Criar produto", criar_produto),
        "2": ("Listar produtos", listar_produtos),
        "3": ("Atualizar produto", atualizar_produto),
        "4": ("Excluir produto", excluir_produto),
        "5": ("Criar vendedor", criar_vendedor),
        "6": ("Listar vendedores", listar_vendedores),
        "7": ("Atualizar vendedor", atualizar_vendedor),
        "8": ("Excluir vendedor", excluir_vendedor),
        "9": ("Criar venda com itens", criar_venda_com_itens),
        "10": ("Listar vendas completas", listar_vendas_completas),
        "11": ("Atualizar venda e itens", atualizar_venda_e_itens),
        "12": ("Excluir venda", excluir_venda),
    }

    while True:
        print("\n=== MENU AC4 - CRUD COMPLETO ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nSelecionado: {descricao}")
            funcao()
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    menu()
