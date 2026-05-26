# Manual Completo da Linguagem BravON

## Índice
1. [Introdução](#introdução)
2. [Primeiros Passos](#primeiros-passos)
3. [Comandos Básicos](#comandos-básicos)
4. [Comandos Avançados](#comandos-avançados)
5. [Exemplos Práticos](#exemplos-práticos)
6. [Referência Rápida](#referência-rápida)
7. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## Introdução

**BravON** é uma linguagem de programação educacional projetada para gerenciamento de turmas e estudantes em instituições de ensino. Ela fornece uma sintaxe simples e intuitiva para realizar operações comuns no contexto académico.

### Características Principais
-  Sintaxe em português (fácil aprendizado)
-  Gerenciamento de estudantes e turmas
-  Geração de relatórios automáticos
-  Cálculo de médias e estatísticas
-  Persistência de dados em JSON
-  Validações automáticas

### Requisitos Mínimos
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexão com internet (se usando versão online)
- Conhecimento básico de conceitos académicos

---

## Primeiros Passos

### 1. Acessar o Editor
Acesse a página do Editor através do menu principal. O editor oferece:
- **Área de Código** (lado esquerdo): Digite seus comandos aqui
- **Botões de Atalho**: 10 comandos comuns pré-configurados
- **Terminal** (lado direito): Exibe resultados e mensagens
- **Tecla Ctrl+Enter**: Executa o código instantaneamente

### 2. Estrutura Básica
Todo programa BravON segue este padrão:

```
COMANDO parametro1 parametro2 ...
COMANDO2 parametro1 ...
```

Não há ponto-e-vírgula ou símbolos especiais. Cada linha é um comando.

### 3. Primeiro Programa
```
CADASTRAR 101 "Edjany Cremilda" "10º A"
CONSULTAR 101
```

Salve, clique em "Executar" e veja o resultado no terminal!

---

## Comandos Básicos

### 1. CADASTRAR
**Propósito:** Adicionar um novo estudante ao sistema

**Sintaxe:**
```
CADASTRAR <matrícula> "<nome>" "<turma>"
```

**Parâmetros:**
| Parâmetro | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| matrícula | número | ID único do estudante | 101, 20050624 |
| nome | texto | Nome completo | "Aldo Silva" |
| turma | texto | Código da turma | "3º A", "3 Ano Tarde" |






**Exemplos:**
```
CADASTRAR 101 "Aldo Silva" "10º A"
CADASTRAR 102 "Zulmira Milagre" "10º A"
CADASTRAR 201 "Jo Cabando" "11º B"
```

**Mensagens de Erro:**
-  "Estudante com matrícula XXX já existe" → Matrícula duplicada
-  "Campos obrigatórios faltando" → Faltam parâmetros

---

### 2. REMOVER
**Propósito:** Deletar um estudante do sistema

**Sintaxe:**
```
REMOVER ESTUDANTE <matrícula>
```

**Exemplo:**
```
REMOVER ESTUDANTE  101
```

**Resultado:**
```
✓ Estudante Aldo Silva (matrícula 101) removido com sucesso
```

---

### 3. CONSULTAR
**Propósito:** Ver informações de um estudante específico. eSTE COMANDO POSSUI PARAMETRO. Veja abaixo:

**xe:**
```
CONSULTAR <matrícula> 
CONSULTAR NOTAS <matrícula> 
```

**Exemplo:**
```
CONSULTAR 101
```

**Resultado:**
```
┌─────────────────────────┐
│ Detalhes do Estudante   │
├─────────────────────────┤
│ Matrícula: 101          │
│ Nome: Aldo Silva        │
│ Turma: 10º A            │
│ Média: 8.5              │
│ Notas: [8.5, 8.0, 9.0]  │
└─────────────────────────┘
```

 

### 4. LISTAR TODOS
**Propósito:** Ver todos os estudantes ou (não importa a turma)

**Sintaxe:**
```
LISTAR TODOS

```

**Resultado:**
Uma Tabela com todos os estudantes (ou apenas da turma especificada)

---

### 5. ADICIONAR NOTAS
**Propósito:** Registrar notas para um estudante

**Sintaxe:**
```
ADICIONAR NOTAS <matrícula> <nota1> <nota2> <nota3> ...
```

**Parâmetros:**
- **matrícula**: ID do estudante
- **notas**: Valores entre 0 e 20 (separados por espaço)

**Exemplo:**
```
ADICIONAR_NOTAS 101 8.5 9.0 7.5
```

**Validações:**
- ⚠️ Notas devem estar entre 0 e 20
- ⚠️ Máximo de 10 notas por estudante

---

## Comandos Avançados

### 1. PROMOVER TURMA
**Propósito:** Mover todos os estudantes de uma turma para outra

**Sintaxe:**
```
PROMOVER TURMA "<turma_origem>" "<turma_destino>"
```

**Exemplo:**
```
PROMOVER TURMA "10º A" "11º A"
```

**Resultado:**
```
✓ 25 estudantes promovidos de 10º A para 11º A.
```

---

### 2. PROMOVER ESTUDANTE ⭐ NOVO
**Propósito:** Mover um estudante específico para outra turma

**Sintaxe:**
```
PROMOVER ESTUDANTE <matrícula> "<turma_destino>"
```

**Exemplo:**
```
PROMOVER ESTUDANTE 101 "11º A"
```

**Resultado:**
```
✓ Estudante Aldo Silva promovido de 10º A para 11º A.
```

---

### 3. RELATORIO
**Propósito:** Gerar relatório completo com estatísticas

**Sintaxe:**
```
RELATORIO GERAL 
RELATORIO TURMA "<Nome da Turma>"
RELATORIO EXPO 

```

**Exemplos:**
```
RELATORIO TURMA "10º C"
```

**Informações mo Relatório:**
- Total de estudantes
- Média geral (ou da turma)
- Melhor desempenho
- Pior desempenho
- Distribuição por turma
- Lista detalhada de estudantes

---

## Exemplos Práticos

### Exemplo 1: Criar uma Turma
```
CADASTRAR 101 "Aldo Silva" "10º A"
CADASTRAR 102 "Zulmira Milagre" "10º A"
CADASTRAR 103 "Jo Cabando" "10º A"
RELATORIO TURMA  "10º A"
```

### Exemplo 2: Adicionar Notas e Consultar
```
CADASTRAR 201 "Ana Costa" "11º B"
ADICIONAR_NOTAS 201 9.5 8.0 10.0
CONSULTAR 201
RELATORIO
```

### Exemplo 3: Promover Estudantes
```
PROMOVER TURMA "10º A" "11º A"
PROMOVER ESTUDANTE 102 "11º B"
LISTAR TODOS
```

### Exemplo 4: Gerar Relatório Completo
```
RELATORIO GERAL 
RELATORIO EXPO 
RELATORIO TURMA "11º B" 
```

---

## Referência Rápida

| Comando | Uso | Resultado |
|---------|-----|-----------|
| `CADASTRAR <mat> "<nom>" "<tur>"` | Adicionar estudante | SIM  ou não  |
| `REMOVER <mat>` | Deletar estudante | SIM  ou não  |
| `CONSULTAR <mat>` | Ver detalhes | Tabela/Erro |
| `LISTAR` | Ver todos | Tabela |
| `LISTAR "<tur>"` | Ver turma | Tabela |
| `ADICIONAR_NOTAS <mat> <n1> <n2>...` | Registrar notas | SIM  ou não  |
| `PROMOVER TURMA "<ori>" "<des>"` | Mover turma | SIM  ou não  |
| `PROMOVER ESTUDANTE <mat> "<tur>"` | Mover estudante | SIM  ou não  |
| `RELATORIO` | Gerar relatório | Documento |
| `RELATORIO "<tur>"` | Relatório de turma | Documento |
| `LIMPEZA` | Limpar dados | ✓ (irreversível) |

---

## Regras de Sintaxe

### Strings (Texto)
- Sempre entre **aspas duplas** `"texto"`
- Podem conter espaços
- Exemplos: `"Aldo Silva"`, `"10º A"`

### Números
- Sem aspas
- Matrículas: inteiros positivos
- Notas: 0 a 20 (decimais permitidos)
- Exemplos: `101`, `9.5`, `20`

### Identificadores
- Letras maiúsculas
- Sem espaços
- Exemplos: `CADASTRAR`, `LISTAR`, `PROMOVER`

### Sensibilidade a Maiúsculas/Minúsculas
- Comandos são **insensíveis** (CADASTRAR = cadastrar)
- Strings são **sensíveis** ("João" ≠ "joão")

---

## FAQ & Troubleshooting

### ❓ 1P: O que significa "Sintaxe inválida"?
**R:** Verifique se:
- Os comandos estão escritos corretamente
- Os strings estão entre aspas duplas
- Os números não têm aspas
- Não há espaços extras no início/fim das linhas

### ❓ 2P: Posso usar acentos nos nomes?
**R:** Sim! BravON suporta caracteres acentuados: ã, é, ö, etc.

### ❓ 3P: Quanto tempo demora a execução?
**R:** Instantânea para até 1000 estudantes. Para datasets maiores, pode levar alguns segundos.

### ❓ 4P: Os dados são salvos automaticamente?
**R:** Sim! Todo comando que modifica dados (CADASTRAR, REMOVER, ADICIONAR_NOTAS, PROMOVER, LIMPEZA) salva automaticamente em JSON.

### ❓ 5P: Posso desfazer uma operação?
**R:** Não há undo integrado. Recomenda-se fazer backups periódicos dos dados.

### ❓ 6P: Qual é a matrícula máxima permitida?
**R:** Qualquer número inteiro positivo até 2.147.483.647 (limite de 32-bit).

### ❓ 7P: Posso ter estudantes com a mesma matrícula?
**R:** Não. O sistema rejeita matrículas duplicadas.

### ❓ 8P: Os nomes podem ter números?
**R:** Sim. Exemplo: `CADASTRAR 101 "João 2º Silva" "10º A"`

---

## Dicas & Boas Práticas

### Dicas
1. **Use Ctrl+Enter** para executar rapidamente
2. **Clique nos botões de atalho** para preencher comandos automáticamente
3. **Copie e cole** blocos de código para reutilização
4. **Verifique erros** no terminal antes de prosseguir

### Boas Práticas
1. Mantenha matrículas **únicas e sequenciais** (101, 102, 103...)
2. Use **nomes de turmas consistentes** (10º A, 11º B, etc.)
3. **Faça backups** antes de operações em massa
4. Teste comandos em **ambientes de testes** primeiro

---

## Contato & Suporte

- Email: itsbenyreis@gmail.com
-  Reportar bugs: https://github.com/bybenb/task_001/issues
- Documentação: https://bravon.unitic.site/help



**Última atualização:** Maio 2026  **Versão:** 1.0.0 | 

**Powered    by <a href="https://unitic.site" target="_blank">UNITIC</a></strong></p>** 
