import unittest
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import json
import os


class TestCommands(unittest.TestCase):
    """Testes unitários para os comandos do compilador BravON"""

    def setUp(self):
        """Preparar para cada teste"""
        self.lexer = Lexer()
        self.interpreter = Interpreter()
        self.interpreter.estudantes = []  # Limpar dados para cada teste

    def tokenize_and_parse(self, codigo):
        """Auxiliar: tokenizar e fazer parsing"""
        tokens = self.lexer.tokenize(codigo)
        parser = Parser(tokens)
        return parser.parse()

    def test_cadastrar_estudante(self):
        """Teste: Cadastrar um estudante"""
        codigo = 'CADASTRAR ESTUDANTE "Aldo Silva" 20230001 "12º A"'
        ast = self.tokenize_and_parse(codigo)
        resultado = self.interpreter.executar(ast)
        
        self.assertEqual(len(resultado), 1)
        self.assertTrue(resultado[0]["sucesso"])
        self.assertIn("cadastrado", resultado[0]["mensagem"].lower())

    def test_cadastrar_duplicado(self):
        """Teste: Não permitir matrícula duplicada"""
        codigo1 = 'CADASTRAR ESTUDANTE "Aldo Silva" 20230001 "12º A"'
        codigo2 = 'CADASTRAR ESTUDANTE "Maria Silva" 20230001 "12º B"'
        
        ast1 = self.tokenize_and_parse(codigo1)
        self.interpreter.executar(ast1)
        
        ast2 = self.tokenize_and_parse(codigo2)
        resultado2 = self.interpreter.executar(ast2)
        
        self.assertFalse(resultado2[0]["sucesso"])
        self.assertIn("já existe", resultado2[0]["mensagem"].lower())

    def test_adicionar_notas(self):
        """Teste: Adicionar notas a um estudante"""
        # Primeiro cadastrar
        codigo1 = 'CADASTRAR ESTUDANTE "Nelma Bravo" 20230145 "12º A"'
        ast1 = self.tokenize_and_parse(codigo1)
        self.interpreter.executar(ast1)
        
        # Depois adicionar notas
        codigo2 = 'ADICIONAR NOTAS 20230145 15 18 17'
        ast2 = self.tokenize_and_parse(codigo2)
        resultado2 = self.interpreter.executar(ast2)
        
        self.assertTrue(resultado2[0]["sucesso"])
        self.assertIn("notas adicionadas", resultado2[0]["mensagem"].lower())
        self.assertEqual(self.interpreter.estudantes[0]["notas"], [15, 18, 17])

    def test_adicionar_notas_fora_intervalo(self):
        """Teste: Validar que notas devem estar entre 0 e 20"""
        # Cadastrar
        codigo1 = 'CADASTRAR ESTUDANTE "Test Student" 20230099 "12º A"'
        ast1 = self.tokenize_and_parse(codigo1)
        self.interpreter.executar(ast1)
        
        # Tentar adicionar nota inválida (25 > 20)
        codigo2 = 'ADICIONAR NOTAS 20230099 25 15 10'
        ast2 = self.tokenize_and_parse(codigo2)
        resultado2 = self.interpreter.executar(ast2)
        
        self.assertFalse(resultado2[0]["sucesso"])
        self.assertIn("entre 0 e 20", resultado2[0]["mensagem"].lower())

    def test_remover_estudante(self):
        """Teste: Remover um estudante"""
        # Cadastrar
        codigo1 = 'CADASTRAR ESTUDANTE "Remove Test" 20230050 "12º A"'
        ast1 = self.tokenize_and_parse(codigo1)
        self.interpreter.executar(ast1)
        self.assertEqual(len(self.interpreter.estudantes), 1)
        
        # Remover
        codigo2 = 'REMOVER ESTUDANTE 20230050'
        ast2 = self.tokenize_and_parse(codigo2)
        resultado2 = self.interpreter.executar(ast2)
        
        self.assertTrue(resultado2[0]["sucesso"])
        self.assertEqual(len(self.interpreter.estudantes), 0)

    def test_listar_todos(self):
        """Teste: Listar todos os estudantes"""
        # Cadastrar dois estudantes
        codigo1 = 'CADASTRAR ESTUDANTE "Student 1" 20230001 "12º A"'
        codigo2 = 'CADASTRAR ESTUDANTE "Student 2" 20230002 "12º B"'
        
        ast1 = self.tokenize_and_parse(codigo1)
        ast2 = self.tokenize_and_parse(codigo2)
        self.interpreter.executar(ast1)
        self.interpreter.executar(ast2)
        
        # Listar
        codigo3 = 'LISTAR TODOS'
        ast3 = self.tokenize_and_parse(codigo3)
        resultado3 = self.interpreter.executar(ast3)
        
        self.assertTrue(resultado3[0]["sucesso"])
        self.assertEqual(len(resultado3[0]["alunos"]), 2)

    def test_promover_turma(self):
        """Teste: Promover alunos de uma turma para outra"""
        # Cadastrar alunos
        codigo1 = 'CADASTRAR ESTUDANTE "Promote 1" 20230010 "11º A"'
        codigo2 = 'CADASTRAR ESTUDANTE "Promote 2" 20230011 "11º A"'
        
        ast1 = self.tokenize_and_parse(codigo1)
        ast2 = self.tokenize_and_parse(codigo2)
        self.interpreter.executar(ast1)
        self.interpreter.executar(ast2)
        
        # Promover
        codigo3 = 'PROMOVER TURMA "11º A" "12º A"'
        ast3 = self.tokenize_and_parse(codigo3)
        resultado3 = self.interpreter.executar(ast3)
        
        self.assertTrue(resultado3[0]["sucesso"])
        self.assertEqual(self.interpreter.estudantes[0]["turma"], "12º A")
        self.assertEqual(self.interpreter.estudantes[1]["turma"], "12º A")

    def test_estatisticas(self):
        """Teste: Gerar estatísticas"""
        # Cadastrar e adicionar notas
        codigo1 = 'CADASTRAR ESTUDANTE "Stats 1" 20230020 "12º A"'
        codigo2 = 'ADICIONAR NOTAS 20230020 10 15 20'
        
        ast1 = self.tokenize_and_parse(codigo1)
        ast2 = self.tokenize_and_parse(codigo2)
        self.interpreter.executar(ast1)
        self.interpreter.executar(ast2)
        
        # Estatísticas
        codigo3 = 'ESTATISTICAS'
        ast3 = self.tokenize_and_parse(codigo3)
        resultado3 = self.interpreter.executar(ast3)
        
        self.assertTrue(resultado3[0]["sucesso"])
        self.assertIn("estatisticas", resultado3[0])
        stats = resultado3[0]["estatisticas"]
        self.assertEqual(stats["total_alunos"], 1)
        self.assertAlmostEqual(stats["media_geral"], 15.0, places=1)

    def test_consultar_notas(self):
        """Teste: Consultar notas de um estudante"""
        # Cadastrar e adicionar notas
        codigo1 = 'CADASTRAR ESTUDANTE "Query Test" 20230030 "12º A"'
        codigo2 = 'ADICIONAR NOTAS 20230030 12 14 16'
        
        ast1 = self.tokenize_and_parse(codigo1)
        ast2 = self.tokenize_and_parse(codigo2)
        self.interpreter.executar(ast1)
        self.interpreter.executar(ast2)
        
        # Consultar
        codigo3 = 'CONSULTAR NOTAS 20230030'
        ast3 = self.tokenize_and_parse(codigo3)
        resultado3 = self.interpreter.executar(ast3)
        
        self.assertTrue(resultado3[0]["sucesso"])
        self.assertIn("[12, 14, 16]", resultado3[0]["mensagem"])

    def test_relatorio_geral(self):
        """Teste: Relatório geral"""
        # Cadastrar
        codigo1 = 'CADASTRAR ESTUDANTE "Report 1" 20230040 "12º A"'
        codigo2 = 'CADASTRAR ESTUDANTE "Report 2" 20230041 "12º B"'
        
        ast1 = self.tokenize_and_parse(codigo1)
        ast2 = self.tokenize_and_parse(codigo2)
        self.interpreter.executar(ast1)
        self.interpreter.executar(ast2)
        
        # Relatório
        codigo3 = 'RELATORIO GERAL'
        ast3 = self.tokenize_and_parse(codigo3)
        resultado3 = self.interpreter.executar(ast3)
        
        self.assertTrue(resultado3[0]["sucesso"])
        self.assertEqual(len(resultado3[0]["alunos"]), 2)

    def test_relatorio_turma(self):
        """Teste: Relatório de uma turma específica"""
        # Cadastrar
        codigo1 = 'CADASTRAR ESTUDANTE "Turma A 1" 20230060 "12º A"'
        codigo2 = 'CADASTRAR ESTUDANTE "Turma A 2" 20230061 "12º A"'
        codigo3 = 'CADASTRAR ESTUDANTE "Turma B" 20230062 "12º B"'
        
        ast1 = self.tokenize_and_parse(codigo1)
        ast2 = self.tokenize_and_parse(codigo2)
        ast3 = self.tokenize_and_parse(codigo3)
        self.interpreter.executar(ast1)
        self.interpreter.executar(ast2)
        self.interpreter.executar(ast3)
        
        # Relatório da turma A
        codigo4 = 'RELATORIO TURMA "12º A"'
        ast4 = self.tokenize_and_parse(codigo4)
        resultado4 = self.interpreter.executar(ast4)
        
        self.assertTrue(resultado4[0]["sucesso"])
        self.assertEqual(len(resultado4[0]["alunos"]), 2)


if __name__ == '__main__':
    unittest.main()
