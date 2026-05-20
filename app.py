from flask import Flask, render_template, request, jsonify
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

app = Flask(__name__)
interpreter = Interpreter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/executar', methods=['POST'])
def executar():
    codigo = request.json.get('codigo', '')
    
    if not codigo.strip():
        return jsonify({"sucesso": False, "mensagem": "Digite algum comando!"})
    
    # 1. Análise Léxica
    lexer = Lexer()
    tokens = lexer.tokenize(codigo)
    
    # 2. Análise Sintática
    parser = Parser(tokens)
    ast = parser.parse()
    
    resultados = []
    
    if ast["erros"]:
        for erro in ast["erros"]:
            resultados.append({
                "tipo": "erro",
                "mensagem": erro
            })
    else:
        # 3. Interpretação/Execução
        resultados_exec = interpreter.executar(ast)
        for res in resultados_exec:
            resultados.append({
                "tipo": "sucesso" if res["sucesso"] else "erro",
                "mensagem": res["mensagem"],
                "dados": res.get("alunos", None)
            })
    
    return jsonify({
        "sucesso": True,
        "resultados": resultados
    })

if __name__ == '__main__':
    app.run(debug=True)