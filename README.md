Sistema de Delivery (Console)

Descrição

Este projeto consiste em um sistema de tele-entrega de alimentos criado em Python, operando completamente em modo console. O sistema foi organizado utilizando Programação Orientada a Objetos (POO) e adota o padrão arquitetural MVC (Modelo-Visão-Controlador), assegurando organização, reutilização e fácil manutenção.

---

🎯 Funcionalidades

Para Clientes:
- Registro com nome, telefone, endereço, e-mail, CPF e senha.
- Acesso com verificação de senha.
- Visualização de restaurantes disponíveis.
- Seleção de pratos e efetuação de pedidos.
- Acompanhamento dos pedidos com status e horário previsto.
- Verificação de atrasos automáticos com base no tempo estimado de entrega.

Para Restaurantes:
- Registro com nome, telefone, endereço, e-mail e CNPJ.
- Acesso ao painel.
- Cadastro de pratos com nome, preço e descrição.
- Visualização de pedidos recebidos.
- Atualização do status do pedido: Em preparo → A caminho → Entregue.

Gerenciamento:
- Todos os dados (clientes, restaurantes, pratos, pedidos) são armazenados em um arquivo `delivery. data`.
- O sistema carrega os dados automaticamente ao iniciar e salva ao encerrar.
- Os pedidos possuem hora de criação e prazo estimado, utilizados para detectar atrasos automaticamente.

---

Tecnologias Utilizadas

- Python 3. 10+
- Módulos nativos:
- `json` (persistência de dados)
- `datetime` (controle de horários)
- `os` (verificação de arquivo)
- `abc` (classes abstratas)

---

Organização em Padrão MVC

- Modelo: Classes `Usuario`, `Cliente`, `Restaurante`, `Prato`, `Pedido`.
- Visão: Menus interativos com `print()` e `input()` no console.
- Controlador: Funções como `fazer_pedido()`, `ver_pedidos_cliente()`, `menu_principal()` manipulan dados e interações.

---

Autenticação

- Clientes acessam o sistema com nome e senha.
- Restaurantes acessam apenas pelo nome (pode ser expandido com senha no futuro).

---

Como Executar

1. Verifique se o Python está instalado.
2. Abra o terminal na pasta do projeto.
3. Execute o arquivo principal:

```bash
python nome_do_arquivo. py
```

4. Interaja via menus conforme o tipo de usuário.

---

Estrutura de Dados (delivery. data)

```json
{
"clientes": [],
"restaurantes": [],
"pedidos": []
}
```

- O sistema registra automaticamente todos os dados dos usuários, pratos e pedidos no arquivo JSON `delivery. data`.

---

Requisitos Atendidos

- [x] Programação orientada a objetos com herança e métodos abstratos.
- [x] Padrão MVC.
- [x] Registro de usuários e controle de acesso.
- [x] Registro e monitoramento de pedidos.
- [x] Verificação automática de pedidos atrasados.
- [x] Persistência em arquivo.
- [x] Interface funcional no console.

👤 Autor

Pedro Sonda