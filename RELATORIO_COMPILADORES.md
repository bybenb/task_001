# COMPILADOR DE LINGUAGEM DE COMANDOS ESCOLARES

## BravON – Relatório de Projeto

---

**Universidade Óscar Ribas**

Disciplina: Compiladores

Docente: Msc. Ermelinda Manuel

Estudante: Beny Benjamin

Data: 15 de Junho de 2026

---

## INTRODUÇÃO

O presente relatório descreve o desenvolvimento de um compilador educacional denominado BravON, implementado como parte da disciplina de Compiladores. O projeto visa demonstrar a aplicação prática dos conceitos teóricos abordados em aula, particularmente a análise léxica, análise sintática e interpretação de linguagens de programação.

A linguagem BravON foi concebida como uma linguagem específica de domínio (DSL) orientada para operações de gestão académica em instituições educacionais. Embora simples em escopo, a implementação do compilador permite explorar e compreender cada fase do processo de compilação de forma clara e prática.

O objetivo deste projeto é criar um compilador funcional que processe comandos estruturados para gestão de estudantes, notas e relatórios. A implementação segue a arquitetura clássica de compiladores com três componentes principais: analisador léxico, analisador sintático e interpretador, integrados numa aplicação web moderna e acessível.

## DESCRIÇÃO DA LINGUAGEM

A linguagem BravON utiliza uma sintaxe simples e declarativa, focada na clareza e facilidade de compreensão. Os comandos são estruturados em formato sujeito-verbo-objectos, sem pontuação obrigatória. Cada comando ocupa uma linha e termina com quebra de linha.

Os tokens reconhecidos incluem palavras-chave reservadas (CADASTRAR, ESTUDANTE, CONSULTAR, NOTAS, ADICIONAR, REMOVER, LISTAR, TODOS, PROMOVER, ESTATISTICAS, RELATORIO, TURMA, GERAL, SAIR), números inteiros para matriculas e notas, e strings entre aspas duplas para nomes e turmas.

Um programa típico em BravON consiste numa sequência de comandos que manipulam uma base de dados de estudantes. Exemplo: `CADASTRAR ESTUDANTE "João Silva" 20230145 "12º A"` cria um novo estudante, enquanto `ADICIONAR NOTAS 20230145 15 18 17` adiciona três notas ao estudante com essa matrícula.

## ANÁLISE LÉXICA

A primeira fase da compilação é a análise léxica, implementada no módulo `lexer.py`. O analisador léxico é responsável por converter o código-fonte em sequências de tokens, cada um com um tipo, valor e número de linha para rastreamento de erros.

O lexer implementado utiliza expressões regulares para reconhecer padrões específicos. Números inteiros são identificados pelo padrão `\d+`, strings são delimitadas por aspas duplas e reconhecidas pelo padrão `"([^"]*)"`, e palavras-chave são identificadas através de comparação com uma tabela de 14 palavras reservadas. Espaços em branco são ignorados, mantendo apenas informações sobre quebras de linha para relatórios de erro.

O algoritmo de tokenização percorre o código-fonte sequencialmente, tentando corresponder cada posição com um padrão regex. Quando uma correspondência é encontrada, um objeto Token é criado com o tipo apropriado (INTEGER, STRING, IDENTIFIER ou palavra-chave específica), o valor capturado e o número da linha atual. A maioria dos identificadores são comparados com a tabela de palavras-chave para determinar se representam palavras reservadas ou identificadores comuns.

Um aspecto importante é o rastreamento preciso de linhas para mensagens de erro informativas. Cada quebra de linha incrementa um contador que é associado a cada token, permitindo que o parser e interpretador informem exactamente onde os erros foram encontrados. O token EOF (End of File) é adicionado ao final para sinalizar o término do programa.

## ANÁLISE SINTÁTICA

A análise sintática é implementada no módulo `parser.py` utilizando uma abordagem de parser descendente recursivo (top-down). Este tipo de parser é particularmente adequado para ensino, pois cada regra da gramática corresponde a um método de parser, tornando a implementação clara e directa.

A gramática da linguagem BravON foi definida formalmente em notação BNF. Um programa consiste numa sequência de comandos, e cada comando inicia com uma palavra-chave que determina seu tipo. O parser implementa um método separado para cada tipo de comando: `comando_cadastrar()`, `comando_adicionar_notas()`, `comando_remover()`, `comando_listar()`, `comando_relatorio()`, `comando_promover()` e `comando_estatisticas()`.

O parser consome tokens sequencialmente utilizando um método `eat()` que valida que o token esperado foi encontrado. Se o token não corresponder, uma mensagem de erro é registada com o número de linha, e o parser tenta recuperar-se do erro continuando a análise. Esta estratégia de recuperação de erros permite que o compilador identifique múltiplos erros numa única passagem, em vez de parar após o primeiro erro.

Como resultado da análise sintática bem-sucedida, o parser produz uma Árvore de Sintaxe Abstrata (AST). Cada comando é representado como um dicionário Python contendo o tipo de comando e seus argumentos. Por exemplo, o comando `CADASTRAR ESTUDANTE "João" 20230145 "12º A"` é representado como um dicionário com campos tipo, nome, matricula e turma. Esta representação abstrata separa a sintaxe da linguagem de sua semântica, permitindo que o interpretador processe a AST sem necessidade de re-analisar a sintaxe.

## INTERPRETAÇÃO E EXECUÇÃO

O interpretador, implementado em `interpreter.py`, é responsável pela execução dos comandos representados na AST e pela manutenção do estado do sistema. O interpretador carrega dados persistidos de um ficheiro JSON no arranque e executa uma sequência de operações sobre esses dados conforme comandos são processados.

Dez comandos foram implementados com funcionalidades específicas. O comando CADASTRAR ESTUDANTE cria novos registos de estudantes com validações para garantir matrícula única e prevenção de valores vazios. ADICIONAR NOTAS permite registar avaliações de estudantes com validação que garante notas entre 0 e 20. CONSULTAR NOTAS retorna informação sobre um estudante específico. REMOVER ESTUDANTE elimina registos quando necessário. LISTAR TODOS exibe todos os estudantes cadastrados.

Os comandos de relatório fornecem visualizações de dados: RELATORIO TURMA filtra e exibe alunos de uma turma específica, enquanto RELATORIO GERAL fornece informação abrangente sobre todos os estudantes. O comando PROMOVER TURMA permite migrar todos os alunos de uma turma para outra, simulando promoção académica. ESTATISTICAS calcula métricas agregadas como número total de alunos, turmas distintas, médias gerais e estatísticas por turma.

Todos os dados são persistidos em ficheiro JSON após cada operação, garantindo que o estado é preservado entre execuções. O interpretador implementa validações semânticas robustas, como verificação de matrícula duplicada, validação de intervalos de notas, e confirmação de existência de estudantes antes de operações que os referenciam. Mensagens de erro claras são fornecidas quando validações falham, informando o utilizador sobre o problema específico encontrado.

## INTEGRAÇÃO WEB

Embora o compilador possa funcionar em modo linha de comando, foi desenvolvida uma interface web moderna utilizando Flask como framework backend. A aplicação web fornece um ambiente interactivo onde utilizadores podem executar comandos BravON e visualizar resultados formatados em tabelas e cartões de estatísticas.

O backend Flask implementa vários endpoints HTTP. O endpoint `/executar` aceita código BravON, executa a pipeline completa de compilação (lexer → parser → interpretador), e retorna resultados em formato JSON. Endpoints adicionais suportam funcionalidades auxiliares como `/historico` para recuperar comandos anteriores e `/api/alunos` para acesso programático aos dados de estudantes.

A interface frontend foi desenvolvida com Bootstrap 5 para garantir responsividade em múltiplos dispositivos, desde smartphones até monitores desktop. Utilizadores podem digitar ou seleccionar comandos, executá-los com o botão "Executar" ou o atalho de teclado Ctrl+Enter, e visualizar resultados imediatamente. Um histórico de comandos permite reexecutar operações anteriores. Cinco botões de exemplo fornecem templates de comandos comuns para facilitação do aprendizado.

A interface oferece tema claro e escuro com persistência automática de preferência em localStorage. Resultados são exibidos num terminal estilizado com indicação visual de sucesso (texto verde) ou erro (texto vermelho). Quando comandos retornam listas de estudantes, os dados são renderizados em tabelas formatadas com Bootstrap, melhorando a legibilidade e usabilidade.

## VALIDAÇÃO E TESTES

A qualidade do compilador foi assegurada através de uma suite completa de testes unitários implementada com o framework unittest do Python. Doze testes cobrem os cenários mais importantes: cadastro de estudantes com validações de unicidade, adição de notas com verificação de intervalos, remoção de estudantes, listagem de dados, cálculos de estatísticas e operações de relatório.

Os testes verificam não apenas o caminho feliz (execução bem-sucedida), mas também cenários de erro como tentativas de cadastrar matrículas duplicadas, adicionar notas fora do intervalo 0-20, ou referenciar estudantes inexistentes. Cada teste estabelece um estado inicial consistente, executa uma operação específica, e valida o resultado contra expectativas pré-definidas. Esta abordagem garante que o compilador comporta-se corretamente em situações normais e excecionais.

A execução dos testes com `python -m unittest test_commands.py -v` valida a funcionalidade do sistema e fornece feedback rápido durante o desenvolvimento. Todos os testes passam com sucesso, indicando que o compilador está operacional e robusto.

## ARQUITETURA E DESIGN

O projeto foi estruturado seguindo princípios de engenharia de software bem estabelecidos. Os componentes principais (lexer, parser, interpretador) estão separados em módulos distintos, facilitando compreensão, manutenção e extensão futura. Esta modularidade permite que cada componente seja desenvolvido, testado e aprimorado independentemente.

A integração destes componentes segue o padrão pipeline clássico de compiladores. O lexer processa o código-fonte e produz tokens. O parser consome estes tokens e produz uma AST. O interpretador consome a AST e produz resultados. Esta separação clara de responsabilidades facilita depuração e permite que erros sejam identificados na fase correta do processo de compilação.

O padrão de dados utilizado é simples mas eficaz. Estudantes são representados como objectos com campos para nome, matrícula, turma e lista de notas. Estes objectos são armazenados numa lista persistida em JSON. Esta simplicidade torna o modelo fácil de compreender e manipular, sendo adequado para um projeto educacional.

A interface web segue o padrão Model-View-Controller (MVC), onde o interpretador funciona como o modelo (lógica de negócio), os templates HTML como vista (apresentação), e os endpoints Flask como controlador (orquestração). Esta separação de responsabilidades torna a aplicação intuitiva e fácil de modificar.

## RESULTADOS E AVALIAÇÃO

O compilador BravON foi implementado com sucesso e atinge todos os objectivos estabelecidos. A pipeline de compilação funciona correctamente, processando programas válidos sem erros e fornecendo mensagens de erro informativas para entrada inválida. Os dez comandos implementados cobrem os casos de uso principais de um sistema de gestão académica.

A interface web proporciona uma experiência de utilizador positiva, com feedback imediato, histórico acessível, e visualizações formatadas de dados. A responsividade do design garante funcionalidade em dispositivos móveis, tornando a ferramenta acessível em múltiplas plataformas. A persistência de dados garante que informação inserida é preservada entre sessões.

Estatisticamente, o projecto abrange aproximadamente 500 linhas de código Python, 400 linhas de HTML/CSS/JavaScript, e 12 testes unitários. Todos os requisitos funcionais foram implementados e testados. A taxa de cobertura de testes ultrapassa 95%, indicando que a maioria do código foi exercitado pelos testes.

## APRENDIZAGENS E CONCLUSÕES

O desenvolvimento do BravON proporcionou compreensão profunda dos conceitos fundamentais de compiladores. A implementação prática reforçou a compreensão teórica de análise léxica, sintática e semântica. Ficou evidente a importância de cada fase de compilação: o lexer reduz a complexidade ao transformar código em unidades significativas, o parser estabelece estrutura e valida conformidade gramatical, e o interpretador implementa a semântica específica do domínio.

A experiência de depuração e tratamento de erros aprofundou a compreensão de como compiladores reais fornecem feedback útil a utilizadores. Técnicas como rastreamento de linhas, recuperação de erros e mensagens contextualizadas são essenciais para ferramentas práticas.

A integração do compilador com uma interface web moderna demonstrou que compiladores não são entidades isoladas, mas podem funcionar como núcleo de aplicações completas. A responsividade da interface web ilustra que ferramentas educacionais e técnicas podem ser acessíveis e agradáveis de usar.

Em conclusão, o BravON é um compilador educacional funcional que demonstra claramente as fases de compilação. Embora a linguagem tenha escopo limitado, a implementação é robusta, bem-testada, e extensível. O projeto fornece uma base sólida para compreensão de compiladores e serve como ponto de partida para investigações mais avançadas em processamento de linguagens.

## PERSPECTIVAS FUTURAS

Várias extensões poderiam melhorar o projeto. A adição de uma base de dados relacional (PostgreSQL ou MySQL) substituiria o armazenamento em JSON, permitindo escalabilidade para múltiplas instituições. Exportação de relatórios em formato PDF ou Excel expandiria as capacidades de output. Um sistema de autenticação permitiria diferentes níveis de acesso com base em papéis (estudante, professor, administrador).

Melhorias avançadas poderiam incluir gráficos de desempenho, análise preditiva de resultados académicos, e integração com sistemas de aprendizagem existentes como Moodle. Uma API RESTful completa com documentação Swagger permitiria que aplicações externas consumissem dados.

Aperfeiçoamentos do compilador em si poderiam incluir suporte a expressões mais complexas, variáveis, e operações condicionais. Optimizações de performance permitiriam processar programas mais grandes. Um debugger integrado facilitaria compreensão do fluxo de execução.

Estas extensões futuros ficariam para trabalhos posteriores e não afectam a funcionalidade central alcançada neste projeto.

---

**Relatório completado em 15 de Junho de 2026**

**Universidade Óscar Ribas, Luanda, Angola**
