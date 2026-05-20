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
            # Validações básicas
            nome = cmd.get("nome", "").strip()
            matricula = cmd.get("matricula")
            turma = cmd.get("turma", "").strip()

            if not nome:
                return {"sucesso": False, "mensagem": "Nome do estudante não pode ser vazio."}

            if not isinstance(matricula, int) or matricula <= 0:
                return {"sucesso": False, "mensagem": "Matrícula inválida."}

            if not turma:
                return {"sucesso": False, "mensagem": "Turma inválida."}

            for est in self.estudantes:
                if est["matricula"] == matricula:
                    return {"sucesso": False, "mensagem": f"Erro: Matrícula {matricula} já existe!"}

            self.estudantes.append({
                "nome": nome,
                "matricula": matricula,
                "turma": turma,
                "notas": []
            })
            self.save_data()
            return {"sucesso": True, "mensagem": f"Estudante {nome} cadastrado com sucesso!"}

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

        elif cmd["tipo"] == "ADICIONAR_NOTAS":
            matricula = cmd.get("matricula")
            notas = cmd.get("notas", [])

            # Encontrar estudante
            for est in self.estudantes:
                if est["matricula"] == matricula:
                    # Validação básica das notas (0-20)
                    for n in notas:
                        if not isinstance(n, int) and not isinstance(n, float):
                            return {"sucesso": False, "mensagem": "Notas inválidas (devem ser números)."}
                        if n < 0 or n > 20:
                            return {"sucesso": False, "mensagem": "Notas devem estar entre 0 e 20."}

                    # Garantir chave 'notas'
                    if "notas" not in est or not isinstance(est["notas"], list):
                        est["notas"] = []

                    # Adicionar as novas notas
                    est["notas"].extend(notas)
                    self.save_data()

                    media_adicionadas = sum(notas) / len(notas) if notas else 0
                    media_geral = sum(est["notas"]) / len(est["notas"]) if est["notas"] else 0

                    return {
                        "sucesso": True,
                        "mensagem": f"Notas adicionadas para {est['nome']}. Média das notas adicionadas: {media_adicionadas:.2f}. Média geral: {media_geral:.2f}.",
                        "aluno": est
                    }

            return {"sucesso": False, "mensagem": f"Estudante com matrícula {matricula} não encontrado."}
        elif cmd["tipo"] == "REMOVER_ESTUDANTE":
            matricula = cmd.get("matricula")
            for i, est in enumerate(self.estudantes):
                if est["matricula"] == matricula:
                    removed = self.estudantes.pop(i)
                    self.save_data()
                    return {"sucesso": True, "mensagem": f"Estudante {removed['nome']} (matrícula {matricula}) removido com sucesso.", "aluno": removed}
            return {"sucesso": False, "mensagem": f"Estudante com matrícula {matricula} não encontrado."}
        elif cmd["tipo"] == "SAIR":
            return {"sucesso": True, "mensagem": "Sistema encerrado."}

        return {"sucesso": False, "mensagem": "Comando não reconhecido."}