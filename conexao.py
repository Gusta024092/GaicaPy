import pymysql.cursors

class Conexao:
    def __init__(self, endereco, usuario, senha, database='GBras'):
        self._endereco = endereco
        self._usuario = usuario
        self._senha = senha
        self._database = database
        self._conexao = None

    def conectar(self):
        try:
            self._conexao = pymysql.connect(host=self._endereco, user=self._usuario, passwd=self._senha, database=self._database, cursorclass=pymysql.cursors.Cursor )
            return 1
        except:
            pass

    def verificar_status(self):
        pass

    def destranca_sistema(self, siape):
        consulta = f"select * from DestrancaSistema where siape = '{siape}' order by dia asc"
        cursor = self._conexao.cursor()
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        return resultado

    def marcar_presenca(self, matricula, professor_consulta: list, data):
        consulta_aluno_valido = f"select * from Presenca where matricula = '{matricula}' and id_disciplina = '{professor_consulta[2]}'"
        cursor = self._conexao.cursor()
        cursor.execute(consulta_aluno_valido)
        resultado = cursor.fetchone()
        if not resultado:
            return f"Aluno inválido"
        else:
            nome_aluno_valido = f"Select nome from Aluno where matricula = '{matricula}'"
            cursor = self._conexao.cursor()
            cursor.execute(nome_aluno_valido)
            nome_resultado = cursor.fetchone()

            atualiza_presenca = f"update Presenca set presenca = presenca + 1 where matricula = '{matricula}' and id_disciplina = '{professor_consulta[2]}';"

            update_presenca = (f"update AtualizarPresenca set presenca = presenca + 1,"
                               f" horario_passado = NOW() where matricula = '{matricula}' and data = '{data}' and"
                               f" id_disciplina = '{professor_consulta[2]}';")
            cursor = self._conexao.cursor()
            cursor.execute(update_presenca)
            self._conexao.commit()
            return f"Presença atualizada, Sr. {nome_resultado[0]}"

    def ver_sobre_aluno(self, matricula, materia, data):
        consulta_aluno = f"select * from testex where id = '{materia}' and data = '{data}' and matricula = '{matricula}' order by horario_passado desc ;"
        cursor = self._conexao.cursor()
        cursor.execute(consulta_aluno)
        resultado = cursor.fetchone()
        return resultado

    def emitir_presenca(self):
        ...

    def fechar_conexao(self):
        if self._conexao:
            self._conexao.close()