import re

class Token:
    def __init__(self, tipo, valor, linha):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha

class Lexer:
    def __init__(self):
        self.tokens = []
        self.linha = 1

    def tokenize(self, codigo):
        self.tokens = []
        self.linha = 1
        
        # Palavras reservadas
        palavras_reservadas = {
            'CADASTRAR': 'CADASTRAR',
            'ESTUDANTE': 'ESTUDANTE',
            'CONSULTAR': 'CONSULTAR',
            'NOTAS': 'NOTAS',
            'ADICIONAR': 'ADICIONAR',
            'RELATORIO': 'RELATORIO',
            'TURMA': 'TURMA',
            'GERAL': 'GERAL',
            'SAIR': 'SAIR'
        }

        # Regex para tokens
        padroes = [
            (r'\d+', 'INTEGER'),
            (r'"([^"]*)"', 'STRING'),
            (r'[A-Za-z_][A-Za-z0-9_]*', 'IDENTIFIER'),
            (r'\n', 'NEWLINE'),
            (r'[ \t]+', None),  # ignorar espaços
        ]

        i = 0
        while i < len(codigo):
            match = None
            for padrao, tipo in padroes:
                regex = re.compile(padrao)
                match = regex.match(codigo, i)
                if match:
                    valor = match.group(0)
                    
                    if tipo == 'NEWLINE':
                        self.linha += 1
                    elif tipo == 'IDENTIFIER':
                        valor_upper = valor.upper()
                        if valor_upper in palavras_reservadas:
                            self.tokens.append(Token(palavras_reservadas[valor_upper], valor_upper, self.linha))
                        else:
                            self.tokens.append(Token('IDENTIFIER', valor, self.linha))
                    elif tipo:
                        self.tokens.append(Token(tipo, valor, self.linha))
                    break
            
            if match:
                i = match.end()
            else:
                # Caractere inválido
                self.tokens.append(Token('ERROR', codigo[i], self.linha))
                i += 1

        self.tokens.append(Token('EOF', 'EOF', self.linha))
        return self.tokens