# ***
> Simulador de Compilador de Linguagem de Comandos Escolares


Compilador web para uma linguagem simples de gestão escolar, desenvolvido em Python com Flask para a disciplina de ***Compiladores***. Ainda não batizei-a, ainda estou pensando num nome daóra :) ... 



## Funcionalidades Implementadas

Análise Léxica (Lexer)  
Análise Sintática (Parser com AST)  
Interpretação e Execução  
Persistência em JSON  
Interface Web responsiva  
Histórico de comandos  


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


## FInd Me
Sabias que somos a geração mais conectada da história e ao mesmo tempo a mais solitária? Olha, eu gosto mesmo muito de baterpapo com gente desconhecida,  então me puxa lá na DM, o nome é "[@bkapa8](https://www.instagram.com/bkapa8)"
