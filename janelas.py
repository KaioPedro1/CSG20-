from modulos import *
from reserva import Reserva
from reserva import Filminho
from reserva import sessoes
import time
#import itens
import pagamento
import loginGui
# Logo: 170x40
# Filmes em cartaz: 170x300
# Botões laterais: 175x105
# Ambos os banners: 725x100

class funcDb():
    def conecta_bd(self):
        self.conn = sqlite3.connect("cinemalocal.bd")
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

class Principal(funcDb):
    def __init__(self):
        self.window = Tk()
        self.window.geometry('1025x600')
        self.window.resizable(False, False)
        # self.window.overrideredirect(True)  # Desativa os botoes padroes da janela
        self.centraliza_janela()

        #self.descricao = itens.Filme() 

        self.frame1 = Frame(self.window, width=175, height=600, borderwidth=0, relief="solid")  # Barra Lateral
        self.frame2 = Frame(self.window, width=840, height=50, borderwidth=1, relief="solid")  # Nome do cinema
        self.frame3 = Frame(self.window, width=840, height=100, borderwidth=1, relief="solid")  # Banner 1
        self.frame4 = LabelFrame(self.window, width=840, height=340, borderwidth=1, relief="solid", text="Mais Vendidos", font=("Elephant", 15))  # Filmes em cartaz
        self.frame5 = Frame(self.window, width=840, height=100, borderwidth=1, relief="solid")  # Banner 2

        self.frame1.pack(side=LEFT)
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()
        self.frame5.pack()

        self.frame1.grid_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame3.grid_propagate(False)  # O grid não se ajusta automaticamente e sim as medidas impostas acima
        self.frame4.grid_propagate(False)
        self.frame5.grid_propagate(False)
        # self.frame6.grid_propagate(False)

        my_img1 = ImageTk.PhotoImage(Image.open("Imagens/filme1.png"))
        my_img2 = ImageTk.PhotoImage(Image.open("Imagens/filme2.png"))
        my_img3 = ImageTk.PhotoImage(Image.open("Imagens/filme3.png"))
        my_img4 = ImageTk.PhotoImage(Image.open("Imagens/filme4.png"))
        my_img5 = ImageTk.PhotoImage(Image.open("Imagens/filme5.png"))
        my_img6 = ImageTk.PhotoImage(Image.open("Imagens/filme6.png"))
        my_img7 = ImageTk.PhotoImage(Image.open("Imagens/filme7.png"))
        my_img8 = ImageTk.PhotoImage(Image.open("Imagens/filme8.png"))
        #self.my_img9 = ImageTk.PhotoImage(Image.open("Imagens/icon_comidas.png"))

        self.image_list = [my_img1, my_img2, my_img3, my_img4, my_img5, my_img6, my_img7, my_img8]
        # Adicionando os elementos aos frames

        # Frame 1
        self.imag2 = PhotoImage(file=r"Imagens/lego2.png")
        self.nome_cine = Label(self.frame1, text="teste3", image=self.imag2)
        self.nome_cine.grid(column=0, row=0)

        self.imag3 = PhotoImage(file=r"Imagens/175x105-00000000.png")

        self.imag7 = PhotoImage(file=r"Imagens/btn_filmes.png")
        self.my_img10 = ImageTk.PhotoImage(Image.open("Imagens/icon_retirar.png"))
        self.my_img11 = ImageTk.PhotoImage(Image.open("Imagens/icon_carrinho.png"))
        self.imag12 = PhotoImage(file=r"Imagens/icon_login.png")
        self.imag13 = PhotoImage(file=r"Imagens/icon_pedidos.png")

        self.btn_filmes = Button(self.frame1, image=self.imag7, command=lambda: self.abrir_janela())
        self.btn_filmes.grid()

        #self.btn_comidas = Button(self.frame1, image=self.my_img9)
        #self.btn_comidas.grid()
        self.btn_pedidos = Button(self.frame1, image=self.imag13, command = self.janela_historico)
        self.btn_pedidos.grid()

        self.btn_retirar = Button(self.frame1, image=self.my_img10, command = self.janela_resgate_codigo)
        self.btn_retirar.grid()

        self.btn_adm = Button(self.frame1, image=self.imag12, command=lambda: loginGui.LoginScreen.inicia_btn_func(self.window))
        self.btn_adm.grid()

        # Frame 2
        self.logo = Label(self.frame2, text="Cinema Local", font=("Arial", 20), padx=282.5)
        self.logo.grid()

        # Frame 3
        self.imag = PhotoImage(file=r"Imagens/banner.png")
        self.nome_cine = Label(self.frame3, image=self.imag)
        self.nome_cine.grid()

        # Frame 4
        self.imag4 = PhotoImage(file=r"Imagens/film2.png")

        self.imag4 = PhotoImage(file=r"Imagens/filme1.png")
        
        #novo

                                                                            #novo
        self.film1 = Button(self.frame4, pady=25, image=self.image_list[0], command=lambda:(self.window.destroy(), self.abriCoiso(), self.testeFilme.janela_horarios(Filminho(4))))
        self.film1.grid(column=1, row=0, pady=18, padx=2)

        self.film2 = Button(self.frame4, pady=25, image=self.image_list[1], command=lambda:(self.window.destroy(), self.abriCoiso(), self.testeFilme.janela_horarios(Filminho(5))))
        self.film2.grid(column=2, row=0, pady=18, padx=2)

        self.film3 = Button(self.frame4, pady=25, image=self.image_list[2], command=lambda:(self.window.destroy(), self.abriCoiso(), self.testeFilme.janela_horarios(Filminho(3))))
        self.film3.grid(column=3, row=0, pady=18, padx=2)

        self.film4 = Button(self.frame4, pady=25, image=self.image_list[3], command=lambda:(self.window.destroy(), self.abriCoiso(), self.testeFilme.janela_horarios(Filminho(7))))
        self.film4.grid(column=4, row=0, pady=18, padx=2)

        
        self.avanca = 1 
        self.volta = 0
        self.button_forward = Button(self.frame4, text=">", command=lambda: self.avancar())
        self.button_forward.grid(column=5, row=0)

        self.button_back = Button(self.frame4, text="<", command=lambda: self.voltar())
        self.button_back.grid(column=0, row=0)
        

        # Frame 5
        self.logo = Label(self.frame5)
        self.logo.grid()

        #variavel usada na tela pedidos
        self.infoPedidos = []

    def abriCoiso(self):
        self.testeFilme = Filme()
    
    def avancar(self):
        global button_forward
        global button_back
        # global button_back
        self.imag4 = PhotoImage(file=r"Imagens/filme2.png")
        self.film1 = Button(self.frame4, pady=25, image=self.image_list[0 + self.avanca])
        self.film1.grid(column=1, row=0, pady=18, padx=2)

        self.film2 = Button(self.frame4, pady=25, image=self.image_list[1 + self.avanca])
        self.film2.grid(column=2, row=0, pady=18, padx=2)

        self.film3 = Button(self.frame4, pady=25, image=self.image_list[2 + self.avanca])
        self.film3.grid(column=3, row=0, pady=18, padx=2)

        self.film4 = Button(self.frame4, pady=25, image=self.image_list[3 + self.avanca])
        self.film4.grid(column=4, row=0, pady=18, padx=2)
        print(self.avanca)
        self.avanca = self.avanca + 1

        if self.avanca > 4:
            self.avanca = 4

    def voltar(self):
        global button_forward
        global button_back

        if self.avanca > 1:
            self.volta = self.avanca - (2 * (self.avanca - 1))
            self.imag4 = PhotoImage(file=r"Imagens/filme2.png")
            self.film1 = Button(self.frame4, pady=25, image=self.image_list[0 - self.volta])
            self.film1.grid(column=1, row=0, pady=18, padx=2)

            self.film2 = Button(self.frame4, pady=25, image=self.image_list[1 - self.volta])
            self.film2.grid(column=2, row=0, pady=18, padx=2)

            self.film3 = Button(self.frame4, pady=25, image=self.image_list[2 - self.volta])
            self.film3.grid(column=3, row=0, pady=18, padx=2)

            self.film4 = Button(self.frame4, pady=25, image=self.image_list[3 - self.volta])
            self.film4.grid(column=4, row=0, pady=18, padx=2)

            print("volta ", self.avanca)
            self.avanca = self.avanca - 1
        else:
            self.avanca = 2
    
    def janela_historico(self):
        j_historico = tkinter.Toplevel()
        j_historico.geometry("900x600")
        j_historico.geometry(f"+{int((j_historico.winfo_screenwidth() / 2) - (900 / 2))}+"
                         f"{int((j_historico.winfo_screenheight() / 2) - (600 / 2))}")
        j_historico.resizable(False, False)

        frame_logo = Frame(j_historico)
        frame_logo.place(relx = 0, rely=0.02, width=900, height=49)
        label_logo = Label(frame_logo, image=self.imag2)
        label_logo.place(relx=0, rely=0)
        self.frame_lista = Frame(j_historico)
        self.frame_lista.place(x=0, y=60, width=900, height=500)
        self.frameTreeList()
        btn_voltar = Button(frame_logo, text="Voltar", bg="green",
                           command=j_historico.destroy)
        btn_voltar.place(x=760, y=0, width=130, height=49)
        btn_imprimir = Button(frame_logo, text="Imprimir", bg="#abdbe3",
                            command=lambda: (j_historico.destroy, self.imprimirSelecao()))
        btn_imprimir.place(x=450, y=0, width=130, height=49)
        self.entry_id = Entry(frame_logo)
        self.entry_id.insert(0,'ID')
        self.entry_id.config(state='disabled')
        self.entry_id.place(x=420, y=0, width=30, height=49)
        j_historico.grab_set()

    def janela_resgate_codigo(self):
        j_codigo = tkinter.Toplevel()
        j_codigo.geometry("900x600")
        j_codigo.geometry(f"+{int((j_codigo.winfo_screenwidth() / 2) - (900 / 2))}+"
                          f"{int((j_codigo.winfo_screenheight() / 2) - (600 / 2))}")
        j_codigo.resizable(False, False)
        j_codigo.grab_set()
        frame_title = Frame(j_codigo)
        frame_title.place(relx=0, rely=0, relwidth=1, relheight=0.10)
        label_title = Label(frame_title, text='RESGATE DE CÓDIGO PROMOCIONAL', font=('verdana', 25))
        label_title.place(relx=0, rely=0, relwidth=1, relheight=1)
        frame_body = Frame(j_codigo)
        frame_body.place(relx=0.25, rely=0.2, relwidth=0.5, relheight=0.6)

        label_login_text = Label(frame_body, text='Código:', font=('verdana', 15))
        label_login_text.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.1)
        entry_cod = Entry(frame_body, font=('verdana', 15))
        entry_cod.place(relx=0.35, rely=0.1, relwidth=0.6, relheight=0.1)

        frame_buttons = Frame(j_codigo)
        frame_buttons.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=0.10)
        button_login = Button(frame_buttons, text='Verifica', command=lambda: self.verificaCodigo(entry_cod.get()))
        button_login.place(relx=0.15, rely=0, relwidth=0.25, relheight=0.8)
        button_clear = Button(frame_buttons, text='Limpar',
                              command=lambda: (entry_cod.delete(0, END)))
        button_clear.place(relx=0.4, rely=0, relwidth=0.25, relheight=0.8)
        button_destroy = Button(frame_buttons, text='Fechar Janela',
                                command=j_codigo.destroy)
        button_destroy.place(relx=0.65, rely=0, relwidth=0.25, relheight=0.8)

    def verificaCodigo(self, entry_cod):
        self.conecta_bd()
        # self.cursor.execute("""SELECT filmes.nome_filme FROM filmes, codigo_promocional
        #                   WHERE codigo_promocional.codigo = ? AND codigo_promocional.codigo = filmes.id""", (entry_cod,))
        self.cursor.execute("""SELECT * FROM codigo_promocional 
                                     WHERE codigo = ?""",
                            (entry_cod,))
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute("SELECT nome_filme FROM filmes WHERE id =?", str(row[2]))
            nomeF = self.cursor.fetchone()
            print(nomeF)
            messagebox.showinfo(title="Validado com sucesso", message="Código promocional válido")
            self.imprimirSelecao(nomeF)
        else:
            messagebox.showinfo(title="Código inválido", message="Por favor, insira um código válido")
    def imprimirSelecao(self, vale_ingresso=None):
        if vale_ingresso == None:
            ticket_frame = LabelFrame(self.window, height=1, width=1, text="Ingresso", font=("Elephant", 15))
            self.ticketareaImp = Text(ticket_frame, font=("arial", 15), fg="black", height=21.5, width=52)
            self.ticketareaImp.insert(END, "-----------------------------------------\n")
            self.ticketareaImp.insert(END, "INGRESSO CINEMALOCAL      \n")
            self.ticketareaImp.insert(END, f'Filme: {self.infoPedidos[3]}\n')
            self.ticketareaImp.insert(END, f'Horario: 14:00\n')
            self.ticketareaImp.insert(END, f'Sessao: {self.infoPedidos[4]}\n')
            self.ticketareaImp.insert(END, "-----------------------------------------\n")
            file = self.ticketareaImp.get(1.0, 'end-1c')
            filename1 = tempfile.mktemp('.txt')
            open(filename1, 'w').write(file)
            os.startfile(filename1, "print")

            self.billareaImp = Text(ticket_frame, font=("arial", 15), fg="black", height=21.5, width=52)
            self.billareaImp.insert(END, " CINEMALOCAL NOTA ")
            self.billareaImp.insert(END, "\n-----------------------------------------------------------------------")
            self.billareaImp.insert(END, f'\nNome:{self.infoPedidos[1]}\t')
            self.billareaImp.insert(END, f'\nCPF :{self.infoPedidos[2]}\t')
            self.billareaImp.insert(END, "\n-----------------------------------------------------------------------")
            self.billareaImp.insert(END, f'\nQuantidade: 1     Produto: ingresso filme {self.infoPedidos[3]}   Valor pago: {self.infoPedidos[5]}\n')
            file1 = self.billareaImp.get(1.0, 'end-1c')
            filename2 = tempfile.mktemp('.txt')
            open(filename2, 'w').write(file1)
            os.startfile(filename2, "print")
        else:
            ticket_frame = LabelFrame(self.window, height=1, width=1, text="Ingresso", font=("Elephant", 15))
            self.ticketareaImp = Text(ticket_frame, font=("arial", 15), fg="black", height=21.5, width=52)
            self.ticketareaImp.insert(END, "-----------------------------------------\n")
            self.ticketareaImp.insert(END, "INGRESSO CINEMALOCAL      \n")
            self.ticketareaImp.insert(END, f'Filme: {vale_ingresso}\n')
            self.ticketareaImp.insert(END, f'Horario: ----\n')
            self.ticketareaImp.insert(END, f'Sessao: ---------------\n')
            self.ticketareaImp.insert(END, "-----------------------------------------\n")
            file = self.ticketareaImp.get(1.0, 'end-1c')
            filename1 = tempfile.mktemp('.txt')
            open(filename1, 'w').write(file)
            os.startfile(filename1, "print")

            self.billareaImp = Text(ticket_frame, font=("arial", 15), fg="black", height=21.5, width=52)
            self.billareaImp.insert(END, " CINEMALOCAL NOTA ")
            self.billareaImp.insert(END, "\n-----------------------------------------------------------------------")
            self.billareaImp.insert(END, f'\nNome: VALE INGRESSO')
            self.billareaImp.insert(END, f'\nCPF : -------------\t')
            self.billareaImp.insert(END, "\n-----------------------------------------------------------------------")
            self.billareaImp.insert(END,
                                    f'\nQuantidade: 1     Produto: ingresso filme {vale_ingresso}   Valor pago: 0\n')
            file1 = self.billareaImp.get(1.0, 'end-1c')
            filename2 = tempfile.mktemp('.txt')
            open(filename2, 'w').write(file1)
            os.startfile(filename2, "print")

    def frameTreeList(self):
        self.lista_tree = ttk.Treeview(self.frame_lista, height=3, column=("col1", "col2", "col3", "col4", "col5","col6"))
        self.lista_tree.heading("#0", text="")
        self.lista_tree.heading("#1", text="ID")
        self.lista_tree.heading("#2", text="Nome")
        self.lista_tree.heading("#3", text="CPF")
        self.lista_tree.heading("#4", text="Filme")
        self.lista_tree.heading("#5", text="Sessão")
        self.lista_tree.heading("#6", text="Valor Pago")

        self.lista_tree.column("#0", width=1, stretch=NO)
        self.lista_tree.column("#1", width=20)
        self.lista_tree.column("#2", width=200)
        self.lista_tree.column("#3", width=100)
        self.lista_tree.column("#4", width=150)
        self.lista_tree.column("#5", width=50)
        self.lista_tree.column("#6", width=50)

        self.lista_tree.place(relx=0, rely=0, relwidth=0.96, relheight=1)

        style = ttk.Style()
        style.configure("Treeview",
                        background="silver",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver")
        style.map('Treeview',
                  background=[('selected', 'blue')])
        self.scrool_list = Scrollbar(self.frame_lista, orient='vertical')
        self.lista_tree.configure(yscroll=self.scrool_list.set)
        self.scrool_list.place(relx=0.96, rely=0, relwidth=0.04, relheight=1)
        self.lista_tree.bind('<Double-1>', self.doubleClick)
        self.insere_historico()

    def doubleClick(self, event):
        self.entry_id.config(state='normal')
        self.entry_id.delete(0, END)
        for i in self.lista_tree.selection():
            self.col1= self.lista_tree.item(i, 'values')
        self.entry_id.insert(END, self.col1[0])
        print(self.col1)
        self.infoPedidos = self.col1
        self.entry_id.config(state='disabled')

    def insere_historico(self):
        self.conecta_bd()
        lista = self.cursor.execute(
            """ SELECT reserva.order_id, reserva.nome_cliente, reserva.cpf_cliente, filmes.nome_filme, reserva.secao_id ,reserva.total_preco FROM reserva, filmes, sessoes
            WHERE secao_id = sessoes.cod AND sessoes.filmes_id = filmes.id ORDER BY order_id;""")
        for i in lista:
            # insere na treeview
            self.lista_tree.insert("", END, values=i)
        self.desconecta_bd()

    def janela_filme(self):
        j_filme = tkinter.Toplevel()
        j_filme.geometry("900x600")
        j_filme.geometry(f"+{int((j_filme.winfo_screenwidth() / 2) - (900 / 2))}+"
                         f"{int((j_filme.winfo_screenheight() / 2) - (600 / 2))}")
        j_filme.resizable(False, False)

        frame1 = Frame(j_filme)
        frame1.pack()

        self.imag2 = PhotoImage(file=r"Imagens/film2.png")
        nome_cine = Label(frame1, text="teste3", image=self.imag2)
        nome_cine.pack()

        j_filme.grab_set()

    def abrir_janela(self):
        self.window.destroy()
        janela_filme = Filme()
        janela_filme.run()

    def centraliza_janela(self):
        self.window.geometry(f"+{int((self.window.winfo_screenwidth() / 2) - (900 / 2))}+"
                             f"{int((self.window.winfo_screenheight() / 2) - (600 / 2))}")
    def run(self):
        self.window.mainloop()

class Filme(funcDb):
    def __init__(self):
        self.window = Tk()
        self.window.geometry('900x600')
        self.window.resizable(False, False)
        # self.window.overrideredirect(True)
        self.centraliza_janela()
        # cria novo pedido
        self.reserva = Reserva()
        # self.carrinho = carrinho
        self.salva_cadeira = []

        self.frame1 = Frame(self.window, borderwidth=0, relief="solid")  # Barra Lateral
        self.frame2 = Frame(self.window, borderwidth=0, relief="solid")  # Nome do cinema

        self.frame1.grid(column=0, row=0, sticky="N,S,E,W")
        self.frame2.grid(column=0, row=1, sticky="N,S,E,W", padx=1)

        # Imagem do filme 222 x 285

        self.btn1 = Button(self.frame1, text="Voltar", bg="green",
                           command=lambda: (self.deleta_coisas(), self.voltar()), width=130)
        self.btn1.grid(column=0, row=0)
        self.filmes_catalogo = []
        self.lista_label = []
        # LOOP PARA PREENCHER OS OITO FILMES DA TELA DE SELEÇÃO
        for i in range(0, 2):
            for j in range(0, 4):
                index = (i * 4) + j + 1
                self.filmes_catalogo.append(Filminho(index))
                self.lista_label.append(
                    Button(self.frame2, image=self.filmes_catalogo[index - 1].poster_filme, borderwidth=0,
                           command=lambda x=((i * 4) + j + 1): (self.janela_horarios(self.filmes_catalogo[x - 1]))))
                self.lista_label[index - 1].grid(column=j, row=i)

    def deleta_coisas(self):
        self.reserva.deleta_reserva()
        del self.filmes_catalogo
        del self.lista_label

    def janela_horarios(self, filme):
        newWindow = tkinter.Toplevel()
        self.filmeInfo = filme
        newWindow.resizable(False, False)
        newWindow.geometry(f"600x450+"
                           f"{int((newWindow.winfo_screenwidth() / 2) - (600 / 2))}+"
                           f"{int((newWindow.winfo_screenheight() / 2) - (450 / 2))}")

        frame1 = Frame(newWindow)
        frame2 = Frame(newWindow)
        frame3 = Frame(newWindow)

        frame1.grid(column=0, row=0)
        frame2.grid(column=0, row=1, sticky="w")
        frame3.grid(column=0, row=2, pady=40)

        bt1 = Button(frame1, text="Voltar", bg="green", width=87, command=lambda: (newWindow.destroy()))
        bt1.grid()
        # Imagem
        self.imag_info = ImageTk.PhotoImage(self.filmeInfo.get_poster())
        label1 = Button(frame2, image=self.imag_info)
        label1.grid(column=0, row=0)
        
        # Descricao
        label2 = Label(frame2, text=f"{self.filmeInfo.nome_filme}\n\n"
                                    f"{self.filmeInfo.genero_filme}\n\n"
                                    f"{self.filmeInfo.idade_filme}\n\n"
                                    f"{self.filmeInfo.duracao_filme}min\n\n"
                                    f"{self.filmeInfo.dublado}", font=("Arial", 20))

        label2.grid(column=1, row=0, ipadx=120)

        # Horarios       |Azul = dublado | amarelo = legendado|
        # não consegui deixar essa parte automatico
        self.bgF = "Pink"
        if filme.dublado == 'Legendado':
            self.bgF = "Yellow"
        else:
            self.bgF = "LightBlue"
        #se der tempo eu melhoro essa parte de horario
        seco = sessoes()
        horarios_disp = seco.busca_horario_id(self.filmeInfo.id)
        lista_bt = []
        for i in range(len(horarios_disp)):
            lista_bt.append(Button(frame3, text='Sessão ' + str(horarios_disp[i][1]) + '\n' + horarios_disp[i][0],
                                   font=("Arial", 15), bg=self.bgF,
                                   command=lambda x=i: (
                                   self.reserva.set_sessao(horarios_disp[x][1]), self.janela_poltrona(), self.preencheInfoReservaHora(horarios_disp[x][0]),
                                   newWindow.destroy())))
            lista_bt[i].grid(column=i, row=0, padx=50)

        newWindow.grab_set()  # Impede acessar a janela de fundo até sair da atual


    def centraliza_janela(self):
        self.window.geometry(f"+{int((self.window.winfo_screenwidth() / 2) - (900 / 2))}+"
                             f"{int((self.window.winfo_screenheight() / 2) - (600 / 2))}")

    def voltar(self):
        self.window.destroy()
        janela = Principal()
        janela.run()
    def run(self):
        self.window.mainloop()


    def janela_poltrona(self):
        # garbage collector estava me ferrando no loop, por isso tem que ser global
        global imgPoltrona
        self.sala_poltrona = self.reserva.get_sala_poltrona()
        self.conecta_bd()
        self.atualiza_dados_db()
        self.btn_poltrona = []

        self.newWindow = tkinter.Toplevel()
        self.newWindow.resizable(False, False)
        self.newWindow.geometry(f"600x550+"
                                f"{int((self.newWindow.winfo_screenwidth() / 2) - (600 / 2))}+"
                                f"{int((self.newWindow.winfo_screenheight() / 2) - (550 / 2))}")
        frame1 = Frame(self.newWindow)
        frame2 = Frame(self.newWindow)
        self.frame3 = Frame(self.newWindow)
        frame4 = Frame(self.newWindow)


        frame1.grid(column=0, row=0)
        frame2.grid(column=0, row=1)
        self.frame3.grid(column=0, row=2)
        frame4.grid(column=0, row=3, pady=10)

        # Frame 1
        bt1 = Button(frame1, text="Voltar", bg="green", width=87,
                     command=lambda: (self.newWindow.destroy()))
        bt1.grid()

        # Frame 2
        label = Label(frame2, text="Escolha a Poltrona ", font=("Arial", 20))
        label.grid()

        listaPoltrona = []

        self.img1 = PhotoImage(file=r"Imagens/Filmes/pol2.png")
        self.img2 = PhotoImage(file=r"Imagens/Filmes/pol.png")
        self.img3 = PhotoImage(file=r"Imagens/Filmes/pol3.png")
        # Frame 3
        self.reserva.qtd_ticket = 0

        for i in range(0, 5):
            for j in range(0, 5):
                # tentei separar em função essas condicionais, mas garbage collector não deixa
                index = (i * 5) + j + 1
                if (self.dados[index-1] == 1):
                    imgPoltrona = self.img1
                elif (self.dados[index-1] == 2):
                    imgPoltrona = self.img3
                    self.reserva.qtd_ticket = self.reserva.qtd_ticket + 1
                else:
                    imgPoltrona = self.img2
                self.btn_poltrona.append(Button(self.frame3, image=imgPoltrona, compound=BOTTOM, text=26-index,
                                                command=lambda x=((i * 5) + j + 1): (self.escolhe_poltrona(x),self.contaQtdPoltrona(x, listaPoltrona))))
                self.btn_poltrona[index - 1].grid(column=j, row=i)

        # Frame 4
        #btn_confirma = Button(frame4, text="Avançar", font=("Arial", 20), fg="White", background="Black", command=self.btn_confirma)
        btn_tela = Button(frame4, text="TELA", font=("Arial", 20), fg="White", background="Black")
        btn_tela.grid(ipadx=110)
        btn_confirma = Button(frame4, text="AVANÇAR", font=("Arial", 18), fg="White", background="Red", command=lambda:(self.verificaRN002(), self.preencheInfoReserva()))
        btn_confirma.grid(ipadx=30)
        self.newWindow.grab_set()

    def verificaRN002(self):
        if self.reserva.qtd_ticket < 1:
            messagebox.showinfo("info", "Nenhuma poltrona selecionada!")
        else:
            pagamento.Store(self.window, self.reserva, self, self.newWindow)

    def contaQtdPoltrona(self, numPoltrona, listaPoltrona):
        if numPoltrona in listaPoltrona and self.reserva.qtd_ticket != 0:
            self.reserva.qtd_ticket = self.reserva.qtd_ticket - 1
            listaPoltrona.remove(numPoltrona)
        else:
            self.reserva.qtd_ticket = self.reserva.qtd_ticket + 1
            if numPoltrona not in listaPoltrona:
                listaPoltrona.append(numPoltrona)
        self.reserva.poltronaNum = listaPoltrona
    def btn_confirma(self):
        if (2 in self.dados):
            for i in range(len(self.dados)):
                if self.dados[i] == 2:
                    self.reserva.add_ticket()
                    self.altera_status_poltrona(i+1, 1)
            #pagamento.Store(self.window, self.reserva, self)
        else:
            messagebox.showinfo(title="Poltrona invalida", message="Selecione uma poltrona vazia")

    def atualiza_dados_db(self):
        self.cursor.execute("SELECT * FROM poltronas WHERE poltrona_id=" + str(self.reserva.get_sala_poltrona()))
        self.dados = self.cursor.fetchone()
        #seleciona todas poltronas menos o id, que esta no indice 0
        self.dados = self.dados[1:]

    def escolhe_poltrona(self, poltrona):
        if (self.dados[poltrona-1] == 1):
            messagebox.showinfo(title="Erro", message="Selecione uma poltrona vazia")
        elif (self.dados[poltrona-1] == 2):
            imgPoltrona = self.img2
            self.altera_status_poltrona(poltrona, 0)
            self.btn_poltrona[poltrona - 1].configure(image=imgPoltrona)
        else:
            imgPoltrona = self.img3
            self.altera_status_poltrona(poltrona, 2)
            self.btn_poltrona[poltrona - 1].configure(image=imgPoltrona)

    def altera_status_poltrona(self, poltrona, status):
        self.conecta_bd()
        # gambiarra pra selecionar a coluna pela query, não é possivel inserir variavel na busca direta na query de coluna,ex SET "p"+poltrona
        poltronaString = "p" + str(poltrona)
        query = """ UPDATE poltronas SET {coluna} = {stat} WHERE poltrona_id = {id}""".format(coluna=poltronaString,
                                                                                              stat=str(status), id=str(
                self.reserva.get_sala_poltrona()))
        self.cursor.execute(query)
        self.conn.commit()
        self.atualiza_dados_db()

    def preencheInfoReserva(self):
        print(self.filmeInfo.nome_filme)
        self.reserva.nome_filme = self.filmeInfo.nome_filme + self.reserva.nome_filme
        self.reserva.tipo_filme = self.filmeInfo.dublado + self.reserva.tipo_filme

    def preencheInfoReservaHora(self, horas):
            self.reserva.horario = horas
            print(self.reserva.horario)