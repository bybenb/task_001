import json
import os

DATA_FILE = 'data/estudantes.json'

class Interpreter:
    def __init__(self):
        self.load_data()

    def load_data(self):
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                self.estudantes = json.load(f)
            except json.JSONDecodeError:
                # File exists but is empty or invalid JSON; initialize empty list
                self.estudantes = []
                # Overwrite the file with a valid empty JSON array
                with open(DATA_FILE, 'w', encoding='utf-8') as fw:
                    json.dump(self.estudantes, fw, ensure_ascii=False, indent=2)

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.estudantes, f, ensure_ascii=False, indent=2)

    def executar(self, ast):
        resultados = []
        for comando in ast.get("comandos", []):
            resultado = self.executar_comando(comando)
            resultados.append(resultado)
        return resultados

    def executar_comando(self, cmd):
        if cmd["tipo"] == "CADASTRAR_ESTUDANTE":
            # Verificar se já existe
            for est in self.estudantes:
                if est["matricula"] == cmd["matricula"]:
                    return {"sucesso": False, "mensagem": f"Erro: Matrícula {cmd['matricula']} já existe!"}
            
            self.estudantes.append({
                "nome": cmd["nome"],
                "matricula": cmd["matricula"],
                "turma": cmd["turma"],
                "notas": []  # futuro
            })
            self.save_data()
            return {"sucesso": True, "mensagem": f"Estudante {cmd['nome']} cadastrado com sucesso!"}

        elif cmd["tipo"] == "CONSULTAR_NOTAS":
            for est in self.estudantes:
                if est["matricula"] == cmd["matricula"]:
                    return {"sucesso": True, "mensagem": f"Notas de {est['nome']}: {est.get('notas', 'Sem notas ainda')}"}
            return {"sucesso": False, "mensagem": f"Estudante com matrícula {cmd['matricula']} não encontrado."}

        elif cmd["tipo"] == "RELATORIO_TURMA":
            turma = cmd["turma"]
            alunos = [est for est in self.estudantes if est["turma"] == turma]
            if alunos:
                return {"sucesso": True, "mensagem": f"Relatório da turma {turma}: {len(alunos)} alunos encontrados.", "alunos": alunos}
            return {"sucesso": False, "mensagem": f"Nenhum aluno encontrado na turma {turma}."}

        elif cmd["tipo"] == "RELATORIO_GERAL":
            return {"sucesso": True, "mensagem": f"Total de estudantes: {len(self.estudantes)}", "alunos": self.estudantes}

        elif cmd["tipo"] == "SAIR":
            return {"sucesso": True, "mensagem": "Sistema encerrado."}

        return {"sucesso": False, "mensagem": "Comando não reconhecido."}