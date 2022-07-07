from modulos import *
from tkinter import filedialog

class funcDb():
    def conecta_bd(self):
        self.conn = sqlite3.connect("cinemalocal.bd")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):
        self.conn.close()

    # CRUD
    def insertButton(self):
        self.conecta_bd()

        if(type(self).__name__=='alimentosGui'):
            self.cursor.execute(
                """ INSERT INTO alimentos (nome_alimento,preco_alimento,categoria_alimento) VALUES(?,?,?)""",
                (self.nome_entry.get(), self.preco_entry.get(), self.user_input.get()))
        elif(type(self).__name__=='filmesGui'):
            self.cursor.execute(
                """ INSERT INTO filmes(nome_filme,genero_filme,idade_filme,duracao_filme, valor_ingresso, poster_filme, dublado) VALUES(?,?,?,?,?,?,?)""",
                (self.nome_entry.get(), self.genero_entry.get(), self.idade_entry.get(), self.duracao_entry.get(),
                 self.user_input.get(), self.poster_entry, self.entry_dub.get()))
            # para imagem nao ficar salva nos proximos aperto de botao
            self.poster_entry = 0
        elif(type(self).__name__=='sessoesGui'):
                # quebrando a string
                user_filme = self.user_input_filme.get().partition(",")
                self.cursor.execute(
                    """ INSERT INTO sessoes(filmes_id, horario_secao) VALUES(?,?)""",
                    (user_filme[0][1:], self.user_input_horario.get()))
        elif(type(self).__name__=='usuarioGui'):
            self.cursor.execute(
                """ INSERT INTO login(username,password,categoria) VALUES(?,?,?)""",
                (self.nome_entry.get(), self.password_entry.get(), self.user_input.get()))
        else:
            print('ERRO!')

        self.conn.commit()
        self.desconecta_bd()
        self.selectButton()
    def buttonDelete(self):
            self.conecta_bd()
            codigo = self.codigo_entry.get()
            nome_tabela = type(self).__name__.split("Gui")[0] if type(self).__name__.split("Gui")[0] != 'usuario' else 'login'
            #cagada que fiz aqui, tem tabela que coloquei a chave primaria como cod e outras com id
            codOrId = 'cod' if type(self).__name__.split("Gui")[0]!='filmes' else 'id'
            query = 'DELETE FROM '+nome_tabela+' WHERE '+codOrId+'='+codigo
            print(query)
            self.cursor.execute(query)
            self.conn.commit()

            if(type(self).__name__.split("Gui")[0]=='filmes'):
                self.cursor.execute('UPDATE filmes SET id=id-1 WHERE id > ?', [self.codigo_entry.get()])
                self.conn.commit()

            self.desconecta_bd()
            self.buttonClear()
            self.selectButton()
    def selectButton(self):
        if(type(self).__name__=='alimentosGui'):
            query = "SELECT cod, nome_alimento, preco_alimento, categoria_alimento FROM alimentos ORDER BY nome_alimento ASC;"
        elif (type(self).__name__ == 'filmesGui'):
            query = "SELECT id, nome_filme, genero_filme, valor_ingresso ,dublado  FROM filmes ORDER BY nome_filme ASC;"
        elif (type(self).__name__ == 'sessoesGui'):
            query = "SELECT sessoes.cod, filmes.nome_filme,horario_secao FROM sessoes, filmes WHERE filmes.id = sessoes.filmes_id;"
        elif (type(self).__name__ == 'usuarioGui'):
            query = "SELECT cod, username, password, categoria FROM login ORDER BY username ASC;"
        self.lista_tree.delete(*self.lista_tree.get_children())
        self.conecta_bd()
        # armazena na variavel lista os campos do banco de dados
        lista = self.cursor.execute(query)

        for i in lista:
            # insere na treeview
            self.lista_tree.insert("", END, values=i)

        self.buttonClear()
        self.desconecta_bd()
    def buttonSearch(self):
        self.conecta_bd()
        self.lista_tree.delete(*self.lista_tree.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()

        if (type(self).__name__ == 'alimentosGui'):
            query = """SELECT cod, nome_alimento,preco_alimento,categoria_alimento
                    FROM alimentos WHERE nome_alimento LIKE '%s' ORDER BY nome_alimento ASC""" % nome
        elif (type(self).__name__ == 'filmesGui'):
            query = """SELECT id, nome_filme,genero_filme,valor_ingresso, dublado
                FROM filmes WHERE nome_filme LIKE '%s' ORDER BY nome_filme ASC""" % nome
        elif (type(self).__name__ == 'sessoesGui'):
            query = """SELECT sessoes.cod, filmes.nome_filme,horario_secao 
            FROM sessoes, filmes WHERE filmes.id = sessoes.filmes_id AND sessoes.cod LIKE '%s'""" % nome
        elif (type(self).__name__ == 'usuarioGui'):
            query = """SELECT cod, username,password,categoria
                FROM login WHERE username LIKE '%s' ORDER BY username ASC""" % nome

        self.cursor.execute(query)
        verifica_nome = self.cursor.fetchall()
        for i in verifica_nome:
            self.lista_tree.insert("", END, values=i)
            self.buttonClear()
        self.desconecta_bd()

    #outros
    def buttonClear(self):
        children_widgets = self.frame_data_body.winfo_children()
        children_widgets = children_widgets + self.frame_data_top.winfo_children()
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                child_widget.delete(0, END)

class adminGui():
    def __init__(self):
        adminGui= Tk()
        self.adminGui = adminGui
        self.createGui()
        adminGui.mainloop()
    def createGui(self):
        self.adminGui.title('Pagina do administrador')
        self.adminGui.geometry("900x600")
        self.adminGui.resizable(True, True)
        self.adminGui.minsize(900, 600)
        self.frame_content = Frame(self.adminGui, bg='yellow')
        self.frame_content.place(relx=0.25, rely=0, relwidth=1, relheight=1)
        self.framesAdmin()
    def framesAdmin(self):
        self.frame_left_btn=Frame(self.adminGui, bg='red')
        self.frame_left_btn.place(relx=0, rely=0, relwidth=0.25, relheight=1)


        btn_add_user = Button(self.frame_left_btn,text='Gerenciar usuarios', command = lambda: self.intanciaProximaTela('login'))
        btn_add_user.place(relx=0, rely=0, relwidth=1, relheight=0.15)

        btn_admin = Button(self.frame_left_btn, text='Gerenciar sessoes',command=lambda: self.intanciaProximaTela('sessoes'))
        btn_admin.place(relx=0, rely=0.15, relwidth=1, relheight=0.15)

        btn_film = Button(self.frame_left_btn, text='Gerenciar filmes',command=lambda: self.intanciaProximaTela('filmes'))
        btn_film.place(relx=0, rely=0.3, relwidth=1, relheight=0.15)

        btn_food = Button(self.frame_left_btn, text='Gerenciar alimentos', command = lambda: self.intanciaProximaTela('alimentos'))
        btn_food.place(relx=0, rely=0.45, relwidth=1, relheight=0.15)
    def intanciaProximaTela(self, classe):
        self.frame_content.destroy()
        self.frame_content = Frame(self.adminGui)
        self.frame_content.place(relx=0.25, rely=0, relwidth=1, relheight=1)
        if classe == 'alimentos':
            alimentosGui(self.frame_content)
        elif classe == 'login':
            usuarioGui(self.frame_content)
        elif classe == 'filmes':
            filmesGui(self.frame_content)
        elif classe == 'sessoes':
            sessoesGui(self.frame_content)

class alimentosGui(funcDb):
    def __init__(self, frame):
        self.frame_content=frame
        self.framesData()
        self.selectButton()

    def framesData(self):
        #frame conteudo topo
        self.frame_data_top = Frame(self.frame_content, bg='#e5ffff')
        self.frame_data_top.place(relx=0, rely=0, relwidth=0.75, relheight=0.1)
        #frame conteudo do meio
        self.frame_data_body = Frame(self.frame_content, bg='pink')
        self.frame_data_body.place(relx=0, rely=0.1, relwidth=1, relheight=0.4)
        #frame lista
        self.frame_treeList = Frame(self.frame_content)
        self.frame_treeList.place(relx=0, rely=0.5, relwidth=0.8, relheight=0.8)

        self.frameDataTop()
        self.frameDataBody()
        self.frameTreeList()
    def frameDataTop(self):

        self.btn_limpar = Button(self.frame_data_top, text="Limpar", command=self.buttonClear)
        self.btn_limpar.place(relx=0.15, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_buscar = Button(self.frame_data_top, text="Buscar", command=self.buttonSearch)
        self.btn_buscar.place(relx=0.25, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_novo = Button(self.frame_data_top, text="Novo", command=self.insertButton)
        self.btn_novo.place(relx=0.5, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_delete = Button(self.frame_data_top, text="Apagar", command=self.buttonDelete)
        self.btn_delete.place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.6)

        """self.btn_fechar = Button(self.frame_data_top, text="Fechar")
        self.btn_fechar.place(relx=0.85, rely=0.2, relwidth=0.1, relheight=0.6)"""
        # texto e nome entrada codigo
        self.lb_codigo = Label(self.frame_data_top, text="Código")
        self.lb_codigo.place(relx=0.05, rely=0.2, relwidth=0.08, relheight=0.3)
        self.codigo_entry = Entry(self.frame_data_top)
        self.codigo_entry.place(relx=0.05, rely=0.5, relwidth=0.08, relheight=0.3)
    def frameDataBody(self):

        # texto nome e entrada nome
        self.lb_nome = Label(self.frame_data_body, text="Nome do produto")
        self.lb_nome.place(relx=0.03, rely=0.05, relwidth=0.5, relheight=0.1)
        self.nome_entry = Entry(self.frame_data_body)
        self.nome_entry.place(relx=0.03, rely=0.15, relwidth=0.5, relheight=0.1)
        # texto preço e entrada para preço
        self.lb_preco = Label(self.frame_data_body, text="Preço em reais(float)")
        self.lb_preco.place(relx=0.25, rely=0.25, relwidth=0.2, relheight=0.1)
        self.preco_entry = Entry(self.frame_data_body)
        self.preco_entry.place(relx=0.25, rely=0.35, relwidth=0.2, relheight=0.1)
        # botao drop down para categorias de alimentos separados em "pipoca, bebida e doce"
        self.lb_categorias = Label(self.frame_data_body, text="Selecione a categoria")
        self.lb_categorias.place(relx=0.03, rely=0.25, relwidth=0.15, relheight=0.1)
        self.user_input = StringVar(self.frame_data_body)
        self.categorias = ("Pipoca", "Bebida", "Doce")
        self.user_input.set("Pipoca")
        self.popup_menu = OptionMenu(self.frame_data_body, self.user_input, *self.categorias)
        self.popup_menu.place(relx=0.03, rely=0.35, relwidth=0.15, relheight=0.1)
    def frameTreeList(self):
        self.lista_tree = ttk.Treeview(self.frame_treeList, height=3, column=("col1", "col2", "col3", "col4"))
        self.lista_tree.heading("#0", text="")
        self.lista_tree.heading("#1", text="Código")
        self.lista_tree.heading("#2", text="Nome")
        self.lista_tree.heading("#3", text="Preço")
        self.lista_tree.heading("#4", text="Categoria")

        self.lista_tree.column("#0", width=1, stretch=NO)
        self.lista_tree.column("#1", width=50)
        self.lista_tree.column("#2", width=200)
        self.lista_tree.column("#3", width=125)
        self.lista_tree.column("#4", width=125)

        self.lista_tree.place(relx=0, rely=0, relwidth=0.90, relheight=0.5)

        style = ttk.Style()
        style.configure("Treeview",
                        background="silver",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver")
        style.map('Treeview',
                  background=[('selected', 'blue')])
        self.scrool_list = Scrollbar(self.frame_treeList, orient='vertical')
        self.lista_tree.configure(yscroll=self.scrool_list.set)
        self.scrool_list.place(relx=0.90, rely=0, relwidth=0.04, relheight=0.5)
        # chamada pra funcao de evento doubleclick
        self.lista_tree.bind('<Double-1>', self.doubleClick)

    def doubleClick(self, event):
        self.buttonClear()
        # gambiarra, casting pra Entry
        self.entry = Entry(self.frame_data_top)
        entry = self.user_input.get()

        self.lista_tree.selection()

        for i in self.lista_tree.selection():
            col1, col2, col3, col4 = self.lista_tree.item(i, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.preco_entry.insert(END, col3)
            self.entry.insert(END, col4)

        ##BOTAO LOGIN e loginDb
    def buttonClearLogin(self, entry1, entry2):
            entry1.delete(0, END)
            entry2.delete(0, END)
    def buttonDestroyLogin(self):
            self.login_screen.destroy()

class filmesGui(funcDb):
    def __init__(self, frame):
        self.frame_content=frame
        self.framesData()
        self.selectButton()

    def framesData(self):
        #frame conteudo topo
        self.frame_data_top = Frame(self.frame_content, bg='#e5ffff')
        self.frame_data_top.place(relx=0, rely=0, relwidth=0.75, relheight=0.1)
        #frame conteudo do meio
        self.frame_data_body = Frame(self.frame_content, bg='pink')
        self.frame_data_body.place(relx=0, rely=0.1, relwidth=1, relheight=0.4)
        #frame lista
        self.frame_treeList = Frame(self.frame_content)
        self.frame_treeList.place(relx=0, rely=0.5, relwidth=0.8, relheight=0.8)

        self.frameDataTop()
        self.frameDataBody()
        self.frameTreeList()
    def frameDataTop(self):

        self.btn_limpar = Button(self.frame_data_top, text="Limpar", command=self.buttonClear)
        self.btn_limpar.place(relx=0.15, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_buscar = Button(self.frame_data_top, text="Buscar", command=self.buttonSearch)
        self.btn_buscar.place(relx=0.25, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_novo = Button(self.frame_data_top, text="Novo", command=self.insertButton)
        self.btn_novo.place(relx=0.5, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_delete = Button(self.frame_data_top, text="Apagar", command=self.buttonDelete)
        self.btn_delete.place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.6)

        # texto e nome entrada codigo
        self.lb_codigo = Label(self.frame_data_top, text="Código")
        self.lb_codigo.place(relx=0.05, rely=0.2, relwidth=0.08, relheight=0.3)
        self.codigo_entry = Entry(self.frame_data_top)
        self.codigo_entry.place(relx=0.05, rely=0.5, relwidth=0.08, relheight=0.3)
    def frameDataBody(self):
        # texto nome e entrada nome
        self.lb_nome = Label(self.frame_data_body, text="Nome do filme")
        self.lb_nome.place(relx=0.03, rely=0.05, relwidth=0.25, relheight=0.1)
        self.nome_entry = Entry(self.frame_data_body)
        self.nome_entry.place(relx=0.03, rely=0.15, relwidth=0.25, relheight=0.1)
        # texto preço e entrada para preço
        self.lb_genero = Label(self.frame_data_body, text="Genero")
        self.lb_genero.place(relx=0.03, rely=0.3, relwidth=0.2, relheight=0.1)
        self.genero_entry = Entry(self.frame_data_body)
        self.genero_entry.place(relx=0.03, rely=0.4, relwidth=0.2, relheight=0.1)

        self.lb_idade = Label(self.frame_data_body, text="Idade")
        self.lb_idade.place(relx=0.3, rely=0.05, relwidth=0.2, relheight=0.1)
        self.idade_entry = Entry(self.frame_data_body)
        self.idade_entry.place(relx=0.3, rely=0.15, relwidth=0.2, relheight=0.1)

        self.lb_duracao = Label(self.frame_data_body, text="Duracao(INT) em minutos")
        self.lb_duracao.place(relx=0.53, rely=0.05, relwidth=0.2, relheight=0.1)
        self.duracao_entry = Entry(self.frame_data_body)
        self.duracao_entry.place(relx=0.53, rely=0.15, relwidth=0.2, relheight=0.1)

        # botao drop down para categorias de alimentos separados em "pipoca, bebida e doce"
        self.lb_horario = Label(self.frame_data_body, text="Selecione o valor do ingresso em reais")
        self.lb_horario.place(relx=0.03, rely=0.55, relwidth=0.25, relheight=0.1)
        self.user_input = StringVar(self.frame_data_body)
        self.categorias = ("39,99", "49,99", "60,00")
        self.user_input.set("39,99")
        self.popup_menu = OptionMenu(self.frame_data_body, self.user_input, *self.categorias)
        self.popup_menu.place(relx=0.03, rely=0.65, relwidth=0.25, relheight=0.1)

        self.entry_dub = StringVar()
        self.dub = Radiobutton(self.frame_data_body, text='Dublado', variable=self.entry_dub, value='Dublado')
        self.dub.place(relx=0.3, rely=0.3, relwidth=0.2, relheight=0.1)
        self.leg = Radiobutton(self.frame_data_body, text='Legendado', variable=self.entry_dub, value='Legendado')
        self.leg.place(relx=0.3, rely=0.4, relwidth=0.2, relheight=0.1)

        self.lb_poster = Label(self.frame_data_body, text="Selecione um poster abaixo")
        self.lb_poster.place(relx=0.40, rely=0.55, relwidth=0.25, relheight=0.1)
        self.btn_poster = Button(self.frame_data_body, text="Abrir imagem", command=self.buttonUploadImage)
        self.btn_poster.place(relx=0.40, rely=0.65, relwidth=0.25, relheight=0.1)
        self.poster_entry = Entry()
        self.poster_entry=0
    def frameTreeList(self):
        self.lista_tree = ttk.Treeview(self.frame_treeList, height=3, column=("col1", "col2", "col3","col4","col5"))
        self.lista_tree.heading("#0", text="")
        self.lista_tree.heading("#1", text="Código")
        self.lista_tree.heading("#2", text="Nome")
        self.lista_tree.heading("#3", text="Genero")
        self.lista_tree.heading("#4", text="Valor ingresso")
        self.lista_tree.heading("#5", text="Dublado/Legendado")


        self.lista_tree.column("#0", width=1, stretch=NO)
        self.lista_tree.column("#1", width=20)
        self.lista_tree.column("#2", width=200)
        self.lista_tree.column("#3", width=100)
        self.lista_tree.column("#4", width=50)
        self.lista_tree.column("#5", width=100)

        self.lista_tree.place(relx=0, rely=0, relwidth=0.90, relheight=0.5)

        style = ttk.Style()
        style.configure("Treeview",
                        background="silver",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver")
        style.map('Treeview',
                  background=[('selected', 'blue')])
        self.scrool_list = Scrollbar(self.frame_treeList, orient='vertical')
        self.lista_tree.configure(yscroll=self.scrool_list.set)
        self.scrool_list.place(relx=0.90, rely=0, relwidth=0.04, relheight=0.5)
        # chamada pra funcao de evento doubleclick
        self.lista_tree.bind('<Double-1>', self.doubleClick)

    def buttonUploadImage(self):
        self.get_imageFilename = filedialog.askopenfilename(title="select image",initialdir="Imagens", filetypes=(("png", "*.png"),("jpg", "*.jpg"), ("Allfile", "*.*")))
        #caso o danado só abra a telinha de upload e feche em seguida
        if self.get_imageFilename=="":
            self.poster_entry = 0
        else:
            self.poster_entry = self.convertToBinaryData(self.get_imageFilename)
    def convertToBinaryData(self, filename):
        # precisa converter pra binario para armazenar no banco de dados
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def doubleClick(self, event):
        self.buttonClear()
        # gambiarra, casting pra Entry
        self.entry = Entry(self.frame_data_top)
        entry = self.user_input.get()
        self.entry2 = Entry()
        entry2=self.entry_dub


        self.lista_tree.selection()

        for i in self.lista_tree.selection():
            col1, col2, col3, col4,col5 = self.lista_tree.item(i, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.genero_entry.insert(END, col3)
            self.entry.insert(END, col4)
            self.entry2.insert(END,col5)

class sessoesGui(funcDb):
    def __init__(self, frame):
        self.frame_content=frame
        self.framesData()
        self.selectButton()

    def framesData(self):
        #frame conteudo topo
        self.frame_data_top = Frame(self.frame_content, bg='#e5ffff')
        self.frame_data_top.place(relx=0, rely=0, relwidth=0.75, relheight=0.1)
        #frame conteudo do meio
        self.frame_data_body = Frame(self.frame_content, bg='pink')
        self.frame_data_body.place(relx=0, rely=0.1, relwidth=1, relheight=0.4)
        #frame lista
        self.frame_treeList = Frame(self.frame_content)
        self.frame_treeList.place(relx=0, rely=0.5, relwidth=0.8, relheight=0.8)

        self.frameDataTop()
        self.frameDataBody()
        self.frameTreeList()
    def frameDataTop(self):

        self.btn_limpar = Button(self.frame_data_top, text="Limpar", command=self.buttonClear)
        self.btn_limpar.place(relx=0.15, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_buscar = Button(self.frame_data_top, text="Buscar", command=self.buttonSearch)
        self.btn_buscar.place(relx=0.25, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_novo = Button(self.frame_data_top, text="Novo", command=self.insertButton)
        self.btn_novo.place(relx=0.5, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_delete = Button(self.frame_data_top, text="Apagar", command=self.buttonDelete)
        self.btn_delete.place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.6)

        # texto e nome entrada codigo
        self.lb_codigo = Label(self.frame_data_top, text="Código")
        self.lb_codigo.place(relx=0.05, rely=0.2, relwidth=0.08, relheight=0.3)
        self.codigo_entry = Entry(self.frame_data_top)
        self.codigo_entry.place(relx=0.05, rely=0.5, relwidth=0.08, relheight=0.3)
    def frameDataBody(self):
        # texto preço e entrada para preço
        self.lb_horario = Label(self.frame_data_body, text="Selecione o horário")
        self.lb_horario.place(relx=0.3, rely=0.25, relwidth=0.2, relheight=0.1)
        self.user_input_horario = StringVar(self.frame_data_body)
        self.categorias_horario = ("14:30","18:00", "20:00")
        self.user_input_horario.set("14:30")
        self.popup_menu2 = OptionMenu(self.frame_data_body, self.user_input_horario, *self.categorias_horario)
        self.popup_menu2.place(relx=0.3, rely=0.35, relwidth=0.2, relheight=0.1)

        self.lb_categorias = Label(self.frame_data_body, text="Selecione o filme")
        self.lb_categorias.place(relx=0.3, rely=0.65, relwidth=0.2, relheight=0.1)

        self.user_input_filme = StringVar(self.frame_data_body)
        todos_filmes = self.listaFilmes()
        self.categorias = todos_filmes
        self.user_input_filme.set(todos_filmes[0])

        self.popup_menu = OptionMenu(self.frame_data_body, self.user_input_filme, *self.categorias)
        self.popup_menu.place(relx=0.3, rely=0.75, relwidth=0.2, relheight=0.1)
    def frameTreeList(self):
        self.lista_tree = ttk.Treeview(self.frame_treeList, height=3, column=("col1", "col2", "col3"))
        self.lista_tree.heading("#0", text="")
        self.lista_tree.heading("#1", text="Código da sessão")
        self.lista_tree.heading("#2", text="Filme")
        self.lista_tree.heading("#3", text="Horario sessão")


        self.lista_tree.column("#0", width=1, stretch=NO)
        self.lista_tree.column("#1", width=30)
        self.lista_tree.column("#2", width=200)
        self.lista_tree.column("#3", width=100)

        self.lista_tree.place(relx=0, rely=0, relwidth=0.90, relheight=0.5)

        style = ttk.Style()
        style.configure("Treeview",
                        background="silver",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver")
        style.map('Treeview',
                  background=[('selected', 'blue')])
        self.scrool_list = Scrollbar(self.frame_treeList, orient='vertical')
        self.lista_tree.configure(yscroll=self.scrool_list.set)
        self.scrool_list.place(relx=0.90, rely=0, relwidth=0.04, relheight=0.5)
        # chamada pra funcao de evento doubleclick
        self.lista_tree.bind('<Double-1>', self.doubleClick)

    def listaFilmes(self):
        self.conecta_bd()
        self.cursor.execute(
            """SELECT id,filmes.nome_filme FROM filmes ORDER BY id""")
        lista = self.cursor.fetchall()
        self.desconecta_bd()
        return lista
    def doubleClick(self, event):
        # gambiarra, casting pra Entry
        self.entry = Entry(self.frame_data_top)
        entry = self.user_input_filme.get()
        self.entry2 = Entry(self.frame_data_top)
        entry2 = self.user_input_horario.get()
        self.buttonClear()
        self.lista_tree.selection()

        for i in self.lista_tree.selection():
            col1, col2, col3= self.lista_tree.item(i, 'values')
            self.codigo_entry.insert(END, col1)
            self.entry2.insert(END, col2)
            self.entry.insert(END, col2)

class usuarioGui(funcDb):
    def __init__(self, frame):
        self.frame_content=frame
        self.framesData()
        self.selectButton()

    def framesData(self):
        #frame conteudo topo
        self.frame_data_top = Frame(self.frame_content, bg='#e5ffff')
        self.frame_data_top.place(relx=0, rely=0, relwidth=0.75, relheight=0.1)
        #frame conteudo do meio
        self.frame_data_body = Frame(self.frame_content, bg='pink')
        self.frame_data_body.place(relx=0, rely=0.1, relwidth=1, relheight=0.4)
        #frame lista
        self.frame_treeList = Frame(self.frame_content)
        self.frame_treeList.place(relx=0, rely=0.5, relwidth=0.8, relheight=0.8)

        self.frameDataTop()
        self.frameDataBody()
        self.frameTreeList()
    def frameDataTop(self):

        self.btn_limpar = Button(self.frame_data_top, text="Limpar", command=self.buttonClear)
        self.btn_limpar.place(relx=0.15, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_buscar = Button(self.frame_data_top, text="Buscar", command=self.buttonSearch)
        self.btn_buscar.place(relx=0.25, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_novo = Button(self.frame_data_top, text="Novo", command=self.insertButton)
        self.btn_novo.place(relx=0.5, rely=0.2, relwidth=0.1, relheight=0.6)

        self.btn_delete = Button(self.frame_data_top, text="Apagar", command=self.buttonDelete)
        self.btn_delete.place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.6)

        # texto e nome entrada codigo
        self.lb_codigo = Label(self.frame_data_top, text="Código")
        self.lb_codigo.place(relx=0.05, rely=0.2, relwidth=0.08, relheight=0.3)
        self.codigo_entry = Entry(self.frame_data_top)
        self.codigo_entry.place(relx=0.05, rely=0.5, relwidth=0.08, relheight=0.3)
    def frameDataBody(self):

        # texto nome e entrada nome
        self.lb_user = Label(self.frame_data_body, text="Usuario")
        self.lb_user.place(relx=0.03, rely=0.05, relwidth=0.7, relheight=0.1)
        self.nome_entry = Entry(self.frame_data_body)
        self.nome_entry.place(relx=0.03, rely=0.15, relwidth=0.7, relheight=0.1)
        # texto preço e entrada para preço
        self.lb_password = Label(self.frame_data_body, text="Senha")
        self.lb_password.place(relx=0.3, rely=0.25, relwidth=0.2, relheight=0.1)
        self.password_entry = Entry(self.frame_data_body)
        self.password_entry.place(relx=0.3, rely=0.35, relwidth=0.2, relheight=0.1)
        # botao drop down para categorias de alimentos separados em "pipoca, bebida e doce"
        self.lb_categorias = Label(self.frame_data_body, text="Selecione a categoria")
        self.lb_categorias.place(relx=0.3, rely=0.65, relwidth=0.2, relheight=0.1)
        self.user_input = StringVar(self.frame_data_body)
        self.categorias = ("Usuario", "Administrador")
        self.user_input.set("Usuario")
        self.popup_menu = OptionMenu(self.frame_data_body, self.user_input, *self.categorias)
        self.popup_menu.place(relx=0.3, rely=0.75, relwidth=0.2, relheight=0.1)
    def frameTreeList(self):
        self.lista_tree = ttk.Treeview(self.frame_treeList, height=3, column=("col1", "col2", "col3","col4"))
        self.lista_tree.heading("#0", text="")
        self.lista_tree.heading("#1", text="Código")
        self.lista_tree.heading("#2", text="Usuario")
        self.lista_tree.heading("#3", text="Senha")
        self.lista_tree.heading("#4", text="Categoria")


        self.lista_tree.column("#0", width=1, stretch=NO)
        self.lista_tree.column("#1", width=30)
        self.lista_tree.column("#2", width=200)
        self.lista_tree.column("#3", width=100)
        self.lista_tree.column("#4", width=100)

        self.lista_tree.place(relx=0, rely=0, relwidth=0.90, relheight=0.5)

        style = ttk.Style()
        style.configure("Treeview",
                        background="silver",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver")
        style.map('Treeview',
                  background=[('selected', 'blue')])
        self.scrool_list = Scrollbar(self.frame_treeList, orient='vertical')
        self.lista_tree.configure(yscroll=self.scrool_list.set)
        self.scrool_list.place(relx=0.90, rely=0, relwidth=0.04, relheight=0.5)
        # chamada pra funcao de evento doubleclick
        self.lista_tree.bind('<Double-1>', self.doubleClick)

    def doubleClick(self, event):
        self.buttonClear()
        # gambiarra, casting pra Entry
        self.entry = Entry(self.frame_data_top)
        entry = self.user_input.get()

        self.lista_tree.selection()

        for i in self.lista_tree.selection():
            col1, col2, col3, col4 = self.lista_tree.item(i, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.password_entry.insert(END, col3)
            self.entry.insert(END, col4)