from modulos import *
from io import BytesIO

class funcDb():
    def conecta_bd(self):
        self.conn = sqlite3.connect("cinemalocal.bd")
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()
class Filminho(funcDb):
    def __init__(self, id):
        self.id = id
        self.nome_filme = self.set_nome_filme()
        self.genero_filme = self.set_genero()
        self.idade_filme = self.set_idade()
        self.duracao_filme = self.set_duracao()
        self.poster_filme_bytes = self.set_poster()
        self.dublado = self.set_dublado()
        self.valor_ingresso = self.set_preco()
        self.poster_filme = ImageTk.PhotoImage(self.get_poster())
    def set_preco(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT valor_ingresso FROM filmes WHERE id=""" + str(self.id))
        preco = self.cursor.fetchone()
        self.desconecta_bd()
        return preco[0]
    def set_dublado(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT dublado FROM filmes WHERE id=""" + str(self.id))
        dublado = self.cursor.fetchone()
        self.desconecta_bd()
        return dublado[0]
    def set_nome_filme(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT nome_filme FROM filmes WHERE id=""" + str(self.id))
        nome = self.cursor.fetchone()
        self.desconecta_bd()
        return nome[0]
    def set_duracao(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT duracao_filme FROM filmes WHERE id=""" + str(self.id))
        duracao = self.cursor.fetchone()
        self.desconecta_bd()
        return duracao[0]
    def set_genero(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT genero_filme FROM filmes WHERE id=""" + str(self.id))
        genero = self.cursor.fetchone()
        self.desconecta_bd()
        return genero[0]
    def set_idade(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT idade_filme FROM filmes WHERE id=""" + str(self.id))
        idade = self.cursor.fetchone()
        self.desconecta_bd()
        return idade[0]
    def set_poster(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT poster_filme FROM filmes WHERE id=""" + str(self.id))
        posterdofilme = self.cursor.fetchone()
        self.desconecta_bd()
        return posterdofilme[0]
    def get_poster(self):
        render = Image.open(BytesIO(self.poster_filme_bytes))
        render = render.resize((222, 285), Image.ANTIALIAS)
        return render
class Reserva(funcDb):
    def __init__(self):
        self.cria_reserva()
        self.id = self.id_db()
        self.qtd_ticket = 0
        self.sessao = None
        self.alimento = None
        self.valorTotal = None
        self.poltronaNum = []
        self.horario = " "
        self.nome_cliente = " "
        self.cpf_cliente=" "
        self.nome_filme = " "
        self.tipo_filme = " "
    def finaliza_pedido(self):
        self.conecta_bd()
        print(self.id)
        self.cursor.execute(
            """UPDATE reserva SET secao_id = ? , total_preco = ?,nome_cliente = ?, cpf_cliente = ? WHERE order_id = ?""", (
                self.sessao, self.valorTotal, self.nome_cliente, self.cpf_cliente, self.id))
        self.conn.commit()
        self.desconecta_bd()
    def set_valor_total(self, valor):
        self.valorTotal = valor
    def set_cpf_cliente(self,cpf):
        self.cpf_cliente= cpf
    def set_nome_cliente(self, nome):
        self.nome_cliente = nome
    def cria_reserva(self):
        self.conecta_bd()
        self.cursor.execute(
            """INSERT INTO reserva DEFAULT VALUES;""")
        self.conn.commit()
        self.desconecta_bd()
    def id_db(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT order_id FROM reserva ORDER BY rowid DESC LIMIT 1;""")
        id = self.cursor.fetchone()
        self.desconecta_bd()
        return id[0]
    def deleta_reserva(self):
        self.conecta_bd()
        self.cursor.execute(
            """DELETE FROM reserva WHERE order_id="""+str(self.id))
        self.conn.commit()
        self.desconecta_bd()
        del self
    def add_ticket(self):
        self.qtd_ticket=self.qtd_ticket+1
    def remove_ticket(self):
        self.qtd_ticket = self.qtd_ticket-1
    def get_id(self):
        return self.id
    def set_sessao(self, sessao_id):
        self.sessao = sessao_id
    def get_sessao(self):
        return self.sessao
    def get_sala_poltrona(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT cod FROM sessoes WHERE cod="""+str(self.sessao))
        id = self.cursor.fetchone()
        self.desconecta_bd()
        return id[0]
    def get_valor_unitario(self):
        self.conecta_bd()
        self.cursor.execute("""SELECT filmes_id FROM sessoes WHERE cod="""+str(self.sessao))
        filme_id = self.cursor.fetchone()
        self.cursor.execute(
            """SELECT valor_ingresso FROM filmes WHERE id="""+str(filme_id[0]))
        preco = self.cursor.fetchone()
        self.desconecta_bd()
        return float(preco[0])
    def get_valor_total(self):
        return float(self.qtd_ticket*self.get_valor_unitario())
class sessoes(funcDb):
    def __init__(self):
        self.lista = self.busca_todas_secoes()
    def busca_todas_secoes(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT * FROM sessoes ORDER BY horario_secao;""")
        lista = self.cursor.fetchall()
        self.desconecta_bd()
        return lista
    def busca_horario_id(self,filme):
        self.lista_hr = []
        for i in range(len(self.lista)):
            if self.lista[i][2]==filme:
                self.lista_hr.append((self.lista[i][3],self.lista[i][0]))
        return list(set(self.lista_hr))
class alimentos(funcDb):
    def __init__(self):
        self.lista_pipocas = self.get_nome_pipocas()
        self.lista_bebidas = self.get_nome_bebidas()
    def get_nome_pipocas(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT nome_alimento FROM alimentos WHERE categoria_alimento='Pipoca'""")
        lista = self.cursor.fetchall()
        self.desconecta_bd()
        return self.filtra_lista(lista)

    def get_nome_bebidas(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT nome_alimento FROM alimentos WHERE categoria_alimento='Bebida'""")
        lista = self.cursor.fetchall()
        self.desconecta_bd()
        return self.filtra_lista(lista)

    def filtra_lista(self, lista):
        teste = []
        for i in range(len(lista)):
            teste.append(lista[i][0])
        return teste

    def get_valor_alimento(self, nome_alimento):
        self.conecta_bd()
        self.cursor.execute("""SELECT preco_alimento FROM alimentos WHERE nome_alimento=?""",[nome_alimento])
        valor = self.cursor.fetchone()
        self.desconecta_bd()
        return float(valor[0])
