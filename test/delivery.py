import json
import os
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# Classes de Negócio
class Usuario(ABC):
    def __init__(self, nome, telefone, endereco, email, cpf):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.cpf = cpf

    @abstractmethod
    def exibir_menu(self):
        pass

class Cliente(Usuario):
    def __init__(self, nome, telefone, endereco, email, cpf, senha):
        super().__init__(nome, telefone, endereco, email, cpf)
        self.senha = senha

    def exibir_menu(self):
        print(f"\nBem-vindo, {self.nome}!")
        while True:
            print("\n1 - Fazer Pedido\n2 - Ver Pedidos\n0 - Sair")
            escolha = input("Escolha uma opção: ")
            if escolha == "1":
                fazer_pedido(self)
            elif escolha == "2":
                ver_pedidos_cliente(self)
            elif escolha == "0":
                break

class Restaurante(Usuario):
    def __init__(self, nome, telefone, endereco, email, cnpj):
        super().__init__(nome, telefone, endereco, email, cnpj)
        self.cardapio = []

    def exibir_menu(self):
        print(f"\nRestaurante: {self.nome}")
        while True:
            print("\n1 - Cadastrar Prato\n2 - Ver Pedidos\n0 - Sair")
            escolha = input("Escolha uma opção: ")
            if escolha == "1":
                cadastrar_prato(self)
            elif escolha == "2":
                ver_pedidos_restaurante(self)
            elif escolha == "0":
                break

class Prato:
    def __init__(self, nome, preco, descricao, imagem=None):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.imagem = imagem

class Pedido:
    def __init__(self, cliente, restaurante, pratos):
        self.cliente = cliente
        self.restaurante = restaurante
        self.pratos = pratos
        self.hora_pedido = datetime.now()
        self.status = 'Em preparo'

    def to_dict(self):
        return {
            'cliente': self.cliente.nome,
            'restaurante': self.restaurante.nome,
            'pratos': [prato.nome for prato in self.pratos],
            'hora_pedido': self.hora_pedido.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status
        }

class Sistema:
    def __init__(self):
        self.clientes = []
        self.restaurantes = []
        self.pedidos = []
        self.carregar_dados()

    def salvar_dados(self):
        dados = {
            'clientes': [cliente.__dict__ for cliente in self.clientes],
            'restaurantes': [{**restaurante.__dict__, 'cardapio': [prato.__dict__ for prato in restaurante.cardapio]} for restaurante in self.restaurantes],
            'pedidos': [pedido.to_dict() for pedido in self.pedidos]
        }
        with open('delivery.data', 'w') as f:
            json.dump(dados, f, indent=4)

    def carregar_dados(self):
        if os.path.exists('delivery.data'):
            with open('delivery.data', 'r') as f:
                dados = json.load(f)
                for c in dados['clientes']:
                    self.clientes.append(Cliente(c['nome'], c['telefone'], c['endereco'], c['email'], c['cpf'], c.get('senha', '')))
                for r in dados['restaurantes']:
                    restaurante = Restaurante(r['nome'], r['telefone'], r['endereco'], r['email'], r['cpf'])
                    restaurante.cardapio = [Prato(**p) for p in r['cardapio']]
                    self.restaurantes.append(restaurante)
                for p in dados['pedidos']:
                    cliente = next(c for c in self.clientes if c.nome == p['cliente'])
                    restaurante = next(r for r in self.restaurantes if r.nome == p['restaurante'])
                    pratos = [next(pr for pr in restaurante.cardapio if pr.nome == nome) for nome in p['pratos']]
                    pedido = Pedido(cliente, restaurante, pratos)
                    pedido.hora_pedido = datetime.strptime(p['hora_pedido'], '%Y-%m-%d %H:%M:%S')
                    pedido.status = p['status']
                    self.pedidos.append(pedido)

def cadastrar_prato(restaurante):
    nome = input("Nome do prato: ")
    preco = float(input("Preço: R$ "))
    descricao = input("Descrição: ")
    prato = Prato(nome, preco, descricao)
    restaurante.cardapio.append(prato)
    sistema.salvar_dados()
    print("Prato cadastrado com sucesso!")

def fazer_pedido(cliente):
    if not sistema.restaurantes:
        print("Nenhum restaurante disponível.")
        return

    print("\nRestaurantes disponíveis:")
    for i, r in enumerate(sistema.restaurantes):
        print(f"{i + 1} - {r.nome}")
    escolha = int(input("Escolha um restaurante pelo número: ")) - 1

    if escolha < 0 or escolha >= len(sistema.restaurantes):
        print("Escolha inválida.")
        return

    restaurante = sistema.restaurantes[escolha]
    pratos = []
    while True:
        print("\nCardápio:")
        for i, prato in enumerate(restaurante.cardapio):
            print(f"{i + 1} - {prato.nome} (R$ {prato.preco:.2f}) - {prato.descricao}")

        op = input("Digite o número do prato para adicionar ao pedido (ou 'fim' para finalizar): ")
        if op.lower() == 'fim':
            break

        try:
            index = int(op) - 1
            if 0 <= index < len(restaurante.cardapio):
                pratos.append(restaurante.cardapio[index])
                print(f"{restaurante.cardapio[index].nome} adicionado ao pedido.")
            else:
                print("Prato inválido.")
        except ValueError:
            print("Entrada inválida.")

    if pratos:
        pedido = Pedido(cliente, restaurante, pratos)
        sistema.pedidos.append(pedido)
        sistema.salvar_dados()
        print("Pedido realizado com sucesso!")
    else:
        print("Nenhum prato foi selecionado.")

def ver_pedidos_cliente(cliente):
    print("\nPedidos do Cliente:")
    pedidos = [p for p in sistema.pedidos if p.cliente.nome == cliente.nome]
    if not pedidos:
        print("Nenhum pedido encontrado.")
        return

    for p in pedidos:
        tempo = datetime.now() - p.hora_pedido
        status = p.status
        if tempo > timedelta(minutes=30) and status == 'Em preparo':
            status = 'Atrasado'
        pratos_str = ', '.join(pr.nome for pr in p.pratos)
        print(f"Restaurante: {p.restaurante.nome} | Pratos: {pratos_str} | Status: {status} | Hora: {p.hora_pedido.strftime('%H:%M')}")

def ver_pedidos_restaurante(restaurante):
    print("\nPedidos do Restaurante:")
    pedidos = [p for p in sistema.pedidos if p.restaurante.nome == restaurante.nome]
    if not pedidos:
        print("Nenhum pedido encontrado.")
        return

    for i, p in enumerate(pedidos):
        pratos_str = ', '.join(pr.nome for pr in p.pratos)
        print(f"\nPedido {i+1} | Cliente: {p.cliente.nome} | Pratos: {pratos_str} | Status: {p.status} | Hora: {p.hora_pedido.strftime('%H:%M')}")
        if p.status == 'Em preparo':
            print("1 - Marcar como A Caminho")
        elif p.status == 'A caminho':
            print("2 - Marcar como Entregue")
        print("0 - Pular")

        op = input("Escolha uma opção para este pedido: ")
        if op == "1" and p.status == 'Em preparo':
            p.status = 'A caminho'
        elif op == "2" and p.status == 'A caminho':
            p.status = 'Entregue'

    sistema.salvar_dados()
    print("Atualizações concluídas.")

def menu_principal():
    while True:
        print("\n--- Sistema de Entregas (Console) ---")
        print("1 - Login Cliente\n2 - Login Restaurante\n3 - Cadastrar Cliente\n4 - Cadastrar Restaurante\n0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            senha = input("Senha: ")
            cliente = next((c for c in sistema.clientes if c.nome == nome and c.senha == senha), None)
            if cliente:
                cliente.exibir_menu()
            else:
                print("Cliente não encontrado ou senha incorreta.")

        elif opcao == "2":
            nome = input("Nome do Restaurante: ")
            restaurante = next((r for r in sistema.restaurantes if r.nome == nome), None)
            if restaurante:
                restaurante.exibir_menu()
            else:
                print("Restaurante não encontrado.")

        elif opcao == "3":
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            email = input("Email: ")
            cpf = input("CPF: ")
            senha = input("Senha: ")
            cliente = Cliente(nome, telefone, endereco, email, cpf, senha)
            sistema.clientes.append(cliente)
            sistema.salvar_dados()
            print("Cliente cadastrado com sucesso!")

        elif opcao == "4":
            nome = input("Nome do Restaurante: ")
            telefone = input("Telefone: ")
            endereco = input("Endereço: ")
            email = input("Email: ")
            cnpj = input("CNPJ: ")
            restaurante = Restaurante(nome, telefone, endereco, email, cnpj)
            sistema.restaurantes.append(restaurante)
            sistema.salvar_dados()
            print("Restaurante cadastrado com sucesso!")

        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

sistema = Sistema()
menu_principal()