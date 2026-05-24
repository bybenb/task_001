# BravON - Compilador de Linguagem Escolar

Um compilador educacional completo para gerenciar dados escolares com análise léxica, sintática e interpretação.

## Funcionalidades Implementadas

Análise Léxica (Lexer)  
Análise Sintática (Parser com AST)  
Interpretação e Execução  
Persistência em JSON  
Interface Web responsiva  
Tema claro/escuro  
Histórico de comandos  
Botões de exemplo  
Validação completa  
Testes unitários  

## Comandos Suportados

```
CADASTRAR ESTUDANTE "Nome" matricula "Turma"
CONSULTAR NOTAS matricula
ADICIONAR NOTAS matricula n1 n2 n3
REMOVER ESTUDANTE matricula
LISTAR TODOS
PROMOVER TURMA "Turma Origem" "Turma Destino"
ESTATISTICAS
RELATORIO TURMA "Nome da Turma"
RELATORIO GERAL
SAIR
```

##  Instalação e Execução

```bash

python -m venv dep
dep\Scripts\activate
pip install -r requirements.txt

python app.py

# Acessar em: http://localhost:5000

# Testes
python -m unittest test_commands.py -v
```

## Exemplos

```
CADASTRAR ESTUDANTE "João Silva" 20230145 "12º A"
ADICIONAR NOTAS 20230145 15 18 17
LISTAR TODOS
ESTATISTICAS
```

##  Arquitetura

- `lexer.py` - Análise léxica
- `parser.py` - Análise sintática  
- `interpreter.py` - Execução
- `app.py` - Servidor Flask
- `test_commands.py` - Testes
- `templates/index.html` - Interface
- `data/estudantes.json` - Dados

## Validações

- Matrícula única
- Notas 0-20
- Nome não vazio
- Turma válida
- Erro handling

## Autor e Créditos

- [@bkapa8](https://www.instagram.com/bkapa8)
- [@nelma_bravo3](https://www.instagram.com/nelma_bravo3)

