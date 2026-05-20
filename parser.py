from lexer import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.erros = []

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, tipo_esperado):
        token = self.current_token()
        if token and token.tipo == tipo_esperado:
            self.pos += 1
            return token
        else:
            # Não avançar automaticamente se não houver token; deixe o chamador decidir como prosseguir
            self.erros.append(
                f"Erro sintático na linha {token.linha if token else '?'} - Esperado: {tipo_esperado}, Encontrado: {token.tipo if token else 'EOF'}"
            )
            if token:
                # tentar sincronizar pulando o token atual
                self.pos += 1
            return None

    def parse(self):
        comandos = []
        while self.current_token() and self.current_token().tipo != 'EOF':
            if self.current_token().tipo == 'SAIR':
                comandos.append({"tipo": "SAIR"})
                break
            
            cmd = self.comando()
            if cmd:
                comandos.append(cmd)
            else:
                # Pular token inválido
                self.pos += 1
        
        return {"comandos": comandos, "erros": self.erros}

    def comando(self):
        token = self.current_token()
        if not token:
            return None

        if token.tipo == 'CADASTRAR':
            return self.comando_cadastrar()
        elif token.tipo == 'CONSULTAR':
            return self.comando_consultar()
        elif token.tipo == 'ADICIONAR':
            return self.comando_adicionar_notas()
        elif token.tipo == 'REMOVER':
            return self.comando_remover()
        elif token.tipo == 'RELATORIO':
            return self.comando_relatorio()
        else:
            self.erros.append(f"Comando desconhecido: {token.valor} (linha {token.linha})")
            return None

    def comando_cadastrar(self):
        self.eat('CADASTRAR')
        self.eat('ESTUDANTE')
        
        nome = self.eat('STRING')
        matricula = self.eat('INTEGER')
        turma = self.eat('STRING')

        if nome and matricula and turma:
            return {
                "tipo": "CADASTRAR_ESTUDANTE",
                "nome": nome.valor,
                "matricula": int(matricula.valor),
                "turma": turma.valor
            }
        return None

    def comando_consultar(self):
        self.eat('CONSULTAR')
        self.eat('NOTAS')
        matricula = self.eat('INTEGER')
        
        if matricula:
            return {
                "tipo": "CONSULTAR_NOTAS",
                "matricula": int(matricula.valor)
            }
        return None

    def comando_relatorio(self):
        self.eat('RELATORIO')
        token = self.current_token()
        
        if token and token.tipo == 'TURMA':
            self.eat('TURMA')
            turma = self.eat('STRING')
            return {
                "tipo": "RELATORIO_TURMA",
                "turma": turma.valor if turma else ""
            }
        elif token and token.tipo == 'GERAL':
            self.eat('GERAL')
            return {"tipo": "RELATORIO_GERAL"}
        
        return None

    def comando_adicionar_notas(self):
        self.eat('ADICIONAR')
        self.eat('NOTAS')
        matricula = self.eat('INTEGER')
        nota1 = self.eat('INTEGER')
        nota2 = self.eat('INTEGER')
        nota3 = self.eat('INTEGER')

        if matricula and nota1 and nota2 and nota3:
            return {
                "tipo": "ADICIONAR_NOTAS",
                "matricula": int(matricula.valor),
                "notas": [int(nota1.valor), int(nota2.valor), int(nota3.valor)]
            }
        return None

    def comando_remover(self):
        self.eat('REMOVER')
        self.eat('ESTUDANTE')
        matricula = self.eat('INTEGER')

        if matricula:
            return {
                "tipo": "REMOVER_ESTUDANTE",
                "matricula": int(matricula.valor)
            }
        return None