from json import loads

arquivo_json = open('data.json')
dados = loads(arquivo_json.read())

# Funções
def obter_total(empresa: dict) -> float:
    total = 0
    for p in empresa['produtos']:
        total += p['preco']
    return total


def mais_comum(lista: list) -> object:
    n_mais_comum = 0
    for elem in lista:
        if lista.count(elem) > n_mais_comum:
            n_mais_comum = lista.count(elem)

    for elem in lista:
        if lista.count(elem) == n_mais_comum:
            return elem


# Disponibilidade
pre_venda = em_estoque = em_operac = 0
val_pre_venda = val_em_estoq = val_em_oper = val_total = 0
for emp in dados['empresas']:
    for p in emp['produtos']:
        match p['disponibilidade']:
            case 'Pre-venda':
                pre_venda += 1
                val_pre_venda += p['preco']
            case 'Em estoque':
                em_estoque += 1
                val_em_estoq += p['preco']
            case 'Em operacao':
                em_operac += 1
                val_em_oper += p['preco']
        val_total += p['preco']

print(f"""- DISPONIBILIDADE DOS PRODUTOS:
Em Pre-venda: {pre_venda}
Em estoque: {em_estoque}
Em operacao: {em_operac}\n""")
print(f"""- VALOR CONCENTRADO EM PRODUTOS:
Pre-venda: {val_pre_venda}
Em estoque: {val_em_estoq}
Em operacao: {val_em_oper}\n""")

# Ranking das empresas
valores = []
for emp in dados['empresas']:
    valores.append(obter_total(emp))

print(f"""- RANKING DAS EMPRESAS:
Nome{' ' * 19}ID{' ' * 19}Valor total dos produtos""")
for valor in valores:
    for emp in dados['empresas']:
        if obter_total(emp) == valor:
            print(emp['nome'], end='')
            print(' ' * (23 - len(emp['nome'])), end='')
            print(emp['id'], end='')
            print(' ' * 20, end='')
            print(obter_total(emp))

# Funcionários
funcs = 0
max_funcs = min_funcs = int()
for emp in dados['empresas']:
    funcs += emp['funcionarios']
    if dados['empresas'].index(emp) == 0:
        max_funcs = min_funcs = emp['funcionarios']
    else:
        if emp['funcionarios'] < min_funcs:
            min_funcs = emp['funcionarios']
        if emp['funcionarios'] > max_funcs:
            max_funcs = emp['funcionarios']


print(f"""\n- FUNCIONÁRIOS:
Total de funcionários: {funcs}
A empresa com menos funcionários possui {min_funcs} funcionários
A empresa com mais funcionários possui {max_funcs} funcionários\n""")

# Categoria dos produtos
cats_prod_em_est = []
cats_prod_em_oper = []
cats_prod_pre_venda = []

for emp in dados['empresas']:
    for p in emp['produtos']:
        match p['disponibilidade']:
            case 'Pre-venda':
                cats_prod_pre_venda.append(p['categoria'])
            case 'Em estoque':
                cats_prod_em_est.append(p['categoria'])
            case 'Em operacao':
                cats_prod_em_oper.append(p['categoria'])

print(f'''- CATEGORIA DOS PRODUTOS:
A maior parte dos produtos em:
Pré-venda é da categoria "{mais_comum(cats_prod_pre_venda)}"
Estoque é da categoria "{mais_comum(cats_prod_em_est)}"
Operação é da categoria "{mais_comum(cats_prod_em_oper)}"\n''')

# Preço dos produtos
preco_pmc = preco_pmb = float()
id_prod_mc = id_prod_mb = 0
nome_pmc = nome_pmb = str()
for emp in dados['empresas']:
    for p in emp['produtos']:
        if dados['empresas'].index(emp) == emp['produtos'].index(p) == 0:
            id_prod_mc = id_prod_mb = p['id']
            preco_pmc = preco_pmb = p['preco']
            nome_pmc = nome_pmb = p['nome']
        else:
            if p['preco'] < preco_pmb:
                preco_pmb, id_prod_mb, nome_pmb = p['preco'], p['id'], p['nome']
            if p['preco'] > preco_pmb:
                preco_pmc, id_prod_mc, nome_pmc = p['preco'], p['id'], p['nome']

print(f"""- PREÇO DOS PRODUTOS:
Produto mais caro: {nome_pmc} (R${preco_pmc})
produto mais barato: {nome_pmb} (R${preco_pmb})""")

# Contatos
print('\n- CONTATOS')
for emp in dados['empresas']:
    print(emp['nome'])
    for elem in emp['contato'].values():
        print(f'{" " * 4}- {elem}')