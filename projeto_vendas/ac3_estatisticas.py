# Avaliação Continuada 3 - 1 ponto
# PROJETO DE VENDAS - parte 1
# Exercicios de estatisticas de vendas.
# Entrega - dia 17/05/2026

from banco_de_dados.conexao import conectar, fechar_conexao

def total_vendas_periodo():
    # Exercicio 1: calcular o valor total vendido em um periodo usando vendas.valor_final.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT SUM(valor_final) FROM vendas")
        resultado = cursor.fetchone()
        fechar_conexao(conexao)
        
        if resultado[0] != None:
            return f"Total vendido: R$ {resultado[0]:.2f}"
        else:
            return "Nenhuma venda encontrada."
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def qtd_vendas_por_vendedor():
    # Exercicio 2: contar quantas vendas cada vendedor realizou usando vendas.id_vendedor.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = '''
            SELECT vendedores.nome, COUNT(vendas.id) 
            FROM vendas 
            INNER JOIN vendedores ON vendas.id_vendedor = vendedores.id 
            GROUP BY vendedores.id
        '''
        cursor.execute(sql)
        resultados = cursor.fetchall()
        fechar_conexao(conexao)
        
        texto = ""
        for linha in resultados:
            texto = texto + f"Vendedor {linha[0]}: {linha[1]} venda(s)\n"
        return texto
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def ticket_medio_geral():
    # Exercicio 3: calcular o ticket medio geral a partir de vendas.valor_final.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT AVG(valor_final) FROM vendas")
        resultado = cursor.fetchone()
        fechar_conexao(conexao)
        
        if resultado[0] != None:
            return f"O ticket médio geral é de R$ {resultado[0]:.2f}"
        else:
            return "Não tem vendas para fazer a média."
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def ticket_medio_por_vendedor():
    # Exercicio 4: calcular o ticket medio de cada vendedor cruzando vendas e vendedores.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = '''
            SELECT vendedores.nome, AVG(vendas.valor_final) 
            FROM vendas 
            INNER JOIN vendedores ON vendas.id_vendedor = vendedores.id 
            GROUP BY vendedores.id
        '''
        cursor.execute(sql)
        resultados = cursor.fetchall()
        fechar_conexao(conexao)
        
        texto = ""
        for linha in resultados:
            texto = texto + f"Vendedor {linha[0]}: Média de R$ {linha[1]:.2f}\n"
        return texto
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def produto_mais_vendido_qtd():
    # Exercicio 5: identificar o produto mais vendido por quantidade em vendas_produtos.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = '''
            SELECT produtos.descricao, SUM(vendas_produtos.quantidade)
            FROM vendas_produtos
            INNER JOIN produtos ON vendas_produtos.id_produto = produtos.id
            GROUP BY produtos.id
            ORDER BY SUM(vendas_produtos.quantidade) DESC
            LIMIT 1
        '''
        cursor.execute(sql)
        resultado = cursor.fetchone()
        fechar_conexao(conexao)
        
        if resultado != None:
            return f"Produto mais vendido: {resultado[0]} com {resultado[1]} unidades."
        else:
            return "Nenhum produto foi vendido."
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def produto_mais_rentavel_valor():
    # Exercicio 6: identificar o produto que gerou maior faturamento somando vendas_produtos.valor_total.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = '''
            SELECT produtos.descricao, SUM(vendas_produtos.valor_total)
            FROM vendas_produtos
            INNER JOIN produtos ON vendas_produtos.id_produto = produtos.id
            GROUP BY produtos.id
            ORDER BY SUM(vendas_produtos.valor_total) DESC
            LIMIT 1
        '''
        cursor.execute(sql)
        resultado = cursor.fetchone()
        fechar_conexao(conexao)
        
        if resultado != None:
            return f"Produto que deu mais lucro: {resultado[0]} (R$ {resultado[1]:.2f})"
        else:
            return "Nenhum dado encontrado."
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def total_descontos_aplicados():
    # Exercicio 7: somar todos os descontos concedidos usando vendas.desconto.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT SUM(desconto) FROM vendas")
        resultado = cursor.fetchone()
        fechar_conexao(conexao)
        
        if resultado[0] != None:
            return f"Total de descontos dados: R$ {resultado[0]:.2f}"
        else:
            return "Nenhum desconto aplicado."
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def percentual_desconto_medio():
    # Exercicio 8: calcular o percentual medio de desconto comparando desconto e valor_final das vendas.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT SUM(desconto), SUM(valor_final) FROM vendas")
        resultado = cursor.fetchone()
        fechar_conexao(conexao)
        
        if resultado[0] != None and resultado[1] != None:
            desconto = float(resultado[0])
            valor_final = float(resultado[1])
            valor_bruto = desconto + valor_final
            
            if valor_bruto > 0:
                percentual = (desconto / valor_bruto) * 100
                return f"Percentual médio de desconto: {percentual:.2f}%"
            
        return "Sem dados para calcular a porcentagem."
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def faturamento_por_dia():
    # Exercicio 9: agrupar o faturamento por dia com base em vendas.data_e_hora e vendas.valor_final.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = '''
            SELECT DATE(data_e_hora), SUM(valor_final)
            FROM vendas
            GROUP BY DATE(data_e_hora)
            ORDER BY DATE(data_e_hora)
        '''
        cursor.execute(sql)
        resultados = cursor.fetchall()
        fechar_conexao(conexao)
        
        texto = ""
        for linha in resultados:
            texto = texto + f"No dia {linha[0]} vendeu R$ {linha[1]:.2f}\n"
        return texto
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def top_3_vendedores_faturamento():
    # Exercicio 10: listar os 3 vendedores com maior faturamento total no periodo.
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = '''
            SELECT vendedores.nome, SUM(vendas.valor_final)
            FROM vendas
            INNER JOIN vendedores ON vendas.id_vendedor = vendedores.id
            GROUP BY vendedores.id
            ORDER BY SUM(vendas.valor_final) DESC
            LIMIT 3
        '''
        cursor.execute(sql)
        resultados = cursor.fetchall()
        fechar_conexao(conexao)
        
        texto = "=== TOP 3 VENDEDORES ===\n"
        posicao = 1
        for linha in resultados:
            texto = texto + f"{posicao}º lugar: {linha[0]} com R$ {linha[1]:.2f}\n"
            posicao = posicao + 1
            
        return texto
    except Exception as erro:
        return f"Deu erro no banco: {erro}"

def menu_relatorios():
    opcoes = {
        "1": ("Total de vendas por periodo", total_vendas_periodo),
        "2": ("Quantidade de vendas por vendedor", qtd_vendas_por_vendedor),
        "3": ("Ticket medio geral", ticket_medio_geral),
        "4": ("Ticket medio por vendedor", ticket_medio_por_vendedor),
        "5": ("Produto mais vendido por quantidade", produto_mais_vendido_qtd),
        "6": ("Produto mais rentavel por faturamento", produto_mais_rentavel_valor),
        "7": ("Total de descontos aplicados", total_descontos_aplicados),
        "8": ("Percentual medio de desconto", percentual_desconto_medio),
        "9": ("Faturamento por dia", faturamento_por_dia),
        "10": ("Top 3 vendedores por faturamento", top_3_vendedores_faturamento),
    }

    while True:
        print("\n=== MENU AC3 - RELATORIOS ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nGerando relatorio: {descricao}")
            resultado = funcao()

            if resultado == None:
                print("Relatorio em estrutura base (return vazio).")
            else:
                print(resultado)
        else:
            print("Opcao invalida. Tente novamente.")