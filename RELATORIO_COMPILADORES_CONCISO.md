# COMPILADOR BRAVOН
## Relatório Académico Conciso

**Universidade Óscar Ribas** | Disciplina: Compiladores | Docente: Msc. Ermelinda Manuel | Data: 15 de Junho de 2026

---

## 1. INTRODUÇÃO

O BravON é um compilador educacional desenvolvido para a disciplina de Compiladores, implementando uma linguagem específica de domínio (DSL) destinada a operações de gestão académica. O projeto demonstra de forma prática e integrada os conceitos fundamentais de análise léxica, análise sintática e interpretação de linguagens de programação. A linguagem foi concebida com sintaxe simples e clara, permitindo aos estudantes compreender facilmente cada fase do processo de compilação sem se perderem em complexidades de linguagens industriais. O compilador está integrado numa aplicação web moderna, demonstrando que compiladores não se limitam a ferramentas de linha de comando, mas podem ser componentes centrais de sistemas interactivos e acessíveis em múltiplos dispositivos.

## 2. ESPECIFICAÇÃO DA LINGUAGEM

A linguagem BravON utiliza uma sintaxe declarativa e imperativa estruturada em comandos simples, sem necessidade de pontuação final nem chaves de delimitação. Cada instrução ocupa uma linha e termina com quebra de linha, seguindo um padrão sujeito-verbo-objectos que a torna intuitiva mesmo para utilizadores sem formação em programação.

O léxico da linguagem compreende 14 palavras-chave reservadas: CADASTRAR, ESTUDANTE, CONSULTAR, NOTAS, ADICIONAR, REMOVER, LISTAR, TODOS, PROMOVER, ESTATISTICAS, RELATORIO, TURMA, GERAL e SAIR. Os tipos de tokens incluem INTEGER (números inteiros para matrículas e notas), STRING (texto entre aspas duplas para nomes e turmas), IDENTIFIER (para potencial extensão), NEWLINE e EOF. A gramática formal em BNF define a estrutura de comandos válidos, garantindo que apenas sequências sintacticamente correctas sejam aceitas pelo parser.

**Exemplos de comandos válidos:**
- `CADASTRAR ESTUDANTE "João Silva" 20230145 "12º A"` – Registar novo estudante
- `ADICIONAR NOTAS 20230145 15 18 17` – Adicionar três notas
- `PROMOVER TURMA "11º A" "12º A"` – Promover todos da turma origem para destino
- `ESTATISTICAS` – Calcular e exibir estatísticas agregadas

## 3. ARQUITECTURA DO COMPILADOR

O BravON segue a arquitectura clássica de compiladores em três fases distintas: análise léxica, análise sintática e interpretação. Esta separação de responsabilidades permite modularidade clara, facilita manutenção e demonstra pedagogicamente cada etapa do processamento.

### 3.1 Análise Léxica (Lexer)

O módulo `lexer.py` implementa o analisador léxico, convertendo código-fonte em sequências de tokens. Utilizando expressões regulares, o lexer reconhece números inteiros (`\d+`), strings delimitadas por aspas (`"([^"]*)"`), e palavras-chave através de comparação com tabela de reservadas. Cada token armazena tipo, valor capturado e número de linha para rastreamento preciso de erros.

O algoritmo percorre o código sequencialmente, aplicando padrões regex na ordem: primeiramente tenta correspondências de palavras-chave, depois números, depois strings, ignorando espaços em branco. Quando um padrão corresponde, um objeto Token é criado e adicionado à lista. Quebras de linha são rastreadas para relatórios de erro informativo. O token especial EOF marca o fim do programa.

### 3.2 Análise Sintática (Parser)

O módulo `parser.py` implementa um parser descendente recursivo (LL(1)), particularmente apropriado para ensino pois cada regra gramatical corresponde a um método. A estrutura é top-down, iniciando do símbolo inicial (programa) e recursivamente expandindo não-terminais.

O parser implementa um método para cada tipo de comando. O método `eat(tipo_esperado)` valida e consome o token actual, avançando para o próximo, com validação defensiva para evitar excesso de avanço em caso de erro. A saída é uma Árvore de Sintaxe Abstrata (AST) representada como estrutura de dicionários Python, onde cada nó contém tipo de comando e seus argumentos parseados.

**Estrutura AST para exemplo:** `{tipo: "CADASTRAR_ESTUDANTE", nome: "João", matricula: 20230145, turma: "12º A"}`

### 3.3 Interpretação e Execução (Interpreter)

O módulo `interpreter.py` executa a AST, transformando directivas abstractas em operações concretas sobre dados. Implementa um padrão visitor implícito com métodos específicos para cada tipo de comando. A persistência de dados é realizada em ficheiro JSON (`data/estudantes.json`), permitindo que dados sobrevivam entre execuções.

Para cada comando, o interpretador valida dados (matrícula única, notas 0-20, campos obrigatórios), executa operações (insert, update, delete, consulta), calcula valores derivados (médias, máximos, mínimos) e persiste estado. Mensagens de resultado informam sucesso ou descrevem erro específico, permitindo feedback útil ao utilizador.

## 4. REQUISITOS FUNCIONAIS IMPLEMENTADOS

O compilador BravON implementa 10 comandos principais cobrindo operações essenciais de um sistema de gestão académica:

**1. CADASTRAR ESTUDANTE** – Registar novo estudante com nome, matrícula e turma, com validação de unicidade de matrícula.

**2. REMOVER ESTUDANTE** – Deletar estudante por matrícula, com confirmação.

**3. LISTAR TODOS** – Exibir tabela formatada de todos os estudantes.

**4. ADICIONAR NOTAS** – Adicionar três notas a estudante existente, validando intervalo 0-20.

**5. CONSULTAR NOTAS** – Retornar notas específicas de um estudante e calcular média.

**6. RELATORIO TURMA** – Filtrar e exibir alunos de uma turma específica com médias.

**7. RELATORIO GERAL** – Apresentar lista completa de estudantes com estatísticas.

**8. ESTATISTICAS** – Calcular agregações: total alunos, turmas, média geral, máximo, mínimo, estatísticas por turma.

**9. PROMOVER TURMA** – Transferir todos os estudantes de turma origem para turma destino.

**10. SAIR** – Encerrar execução.

Adicionalmente, o sistema valida campos obrigatórios, rejeita operações inválidas com mensagens claras e persiste dados automaticamente em JSON.

## 5. VALIDAÇÕES SEMÂNTICAS

O interpretador implementa múltiplas camadas de validação para garantir integridade de dados. A validação de matrícula verifica unicidade, prevenindo duplicatas. Notas são validadas para estar no intervalo [0, 20]. Campos de texto (nome, turma) são verificados para não estar vazios. Estudantes devem existir antes de operações que os referenciam.

Tipos de dados são validados – matrículas e notas devem ser inteiros válidos, nomes e turmas devem ser strings. Operações que referenciam estudantes inexistentes retornam erro descritivo. Esta validação semântica implementada na camada de interpretação garante que a base de dados mantém estado consistente.

## 6. INTERFACE WEB E INTEGRAÇÃO

O servidor Flask (`app.py`) fornece endpoints HTTP para integração com frontend web. A rota POST `/executar` recebe código BravON, executa a pipeline lexer→parser→interpreter e retorna resultados em JSON. A rota GET `/api/alunos` fornece acesso directo aos dados. Um endpoint `/historico` mantém histórico dos últimos 50 comandos executados.

A interface (`templates/index.html`) é desenvolvida em HTML5, CSS3 com Bootstrap 5 e JavaScript vanilla, proporciona responsividade completa (funciona em smartphones, tablets e desktops). Características incluem editor de código textarea, terminal de saída com cores (verde para sucesso, vermelho para erro), tabelas formatadas de resultados, cinco botões com exemplos rápidos, histórico clicável e alternância tema claro/escuro com persistência em localStorage. Um atalho de teclado (Ctrl+Enter) permite execução rápida.

## 7. ETAPAS DE DESENVOLVIMENTO

O desenvolvimento progrediu sequencialmente através de fases lógicas. Inicialmente, foram definidos requisitos e gramática formal em BNF. O analisador léxico foi implementado utilizando expressões regulares. O parser descendente recursivo foi construído seguindo a gramática, produzindo AST como saída. O interpretador executou a AST com validações semânticas e persistência JSON.

Testes unitários foram criados cobrindo todos os 10 comandos, validações e casos de erro. A interface web foi desenvolvida com Bootstrap responsivo e JavaScript para interactividade. Após cada fase principal, testes de integração verificaram funcionamento da pipeline completa. Iterações finais focaram em melhorias de UX (tema, histórico, exemplos) e otimização de mensagens de erro.

## 8. FLUXO DE COMPILAÇÃO

O fluxo de um programa BravON inicia quando o utilizador escreve código e pressiona "Executar" na interface web. O servidor recebe o código como JSON POST, transmitindo-o para o Lexer. O Lexer percorre sequencialmente produzindo tokens com tipos (INTEGER, STRING, KEYWORD, EOF). A lista de tokens passa para o Parser, que percorre descendentemente produzindo AST de dicionários representando comandos validados sintaticamente.

A AST passa para o Interpretador que carrega dados persistidos (JSON), executa cada comando da AST (inserção, actualização, deleção, consulta), valida dados semánticamente, executa lógica de negócio (cálculos de média), persiste mudanças em JSON e retorna resultados com mensagens. O servidor serializa resultados como JSON e envia para o cliente. A interface renderiza tabelas, cartões de estatísticas e mensagens de feedback, actualizando histórico.

## 9. TECNOLOGIAS UTILIZADAS

**Backend:** Python 3.13 como linguagem base, Flask 2.3+ como micro framework web, JSON para serialização e persistência de dados.

**Frontend:** HTML5 semântico, CSS3 com Bootstrap 5 para design responsivo, JavaScript ES6+ vanilla (sem dependências externas além Bootstrap para CSS).

**Desenvolvimento:** Git para controlo de versão, unittest framework Python para testes.

**Arquitetura:** Parser descendente recursivo (LL(1)), padrão MVC implícito (interpretador como model, interface como view, Flask como controller).

## 10. TESTES E VALIDAÇÃO

Foram implementados 12 testes unitários cobrindo: cadastro e remoção de estudantes, validação de matrícula duplicada, adição de notas com validação de intervalo, cálculo de médias, operações de listagem, promoção de turmas, cálculo de estatísticas. Os testes executam em framework unittest Python e validam comportamento correcto em casos normais e casos de erro.

Testes de integração verificaram o fluxo completo lexer→parser→interpreter→persistência. Testes de UI verificaram responsividade em múltiplos tamanhos de ecrã (320px até 2560px) e navegadores diferentes. Todos os requisitos funcionais foram validados como operacionais.

## 11. CONCLUSÕES E APRENDIZAGENS

O projecto BravON demonstra com sucesso a implementação prática de um compilador completo seguindo arquitectura clássica. Os componentes léxico, sintático e de interpretação funcionam integrados, processando corretamente programa BravON em código executável com validação robusta e feedback ao utilizador.

As principais aprendizagens incluem compreensão profunda de análise léxica utilizando expressões regulares, design e implementação de parsers descendentes recursivos, construção de representações intermediárias (AST) que facilitam separação entre parsing e execução, e técnicas de validação semântica. A integração com interface web moderna demonstra que compiladores são ferramentas vivas integradas em sistemas complexos, não apenas processadores de texto.

Dificuldades encontradas e resolvidas incluíram sincronização cuidadosa de parser após erros, tratamento de ficheiros JSON vazios, e design de interface responsiva. Melhorias futuras possíveis incluem tipos de dados mais complexos, variáveis e expressões, base de dados relacional em vez de JSON, e gráficos de visualização de estatísticas.

O BravON estabelece base sólida para exploração adicional em linguagens específicas de domínio, compiladores mais sofisticados e aplicações educacionais integradas.

---

**Fim do Relatório**

Data: 15 de Junho de 2026 | Universidade Óscar Ribas | Disciplina: Compiladores
