from modulos import *
import janelas
import reserva

class funcDb():
    def conecta_bd(self):
        self.conn = sqlite3.connect("cinemalocal.bd")
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()


class Store:
    def __init__(self, window, carrinho, obj, janelaDestroi):
        self.win = Toplevel(window)
        # window.destroy()
        # self.win = window
        self.principalobj = obj
        self.carrinho = carrinho
        self.destruirJan = janelaDestroi
        # self.win = Tk()
        self.win.geometry("900x685")

        # centraliza janela
        self.win.geometry(
            f"+{int((self.win.winfo_screenwidth() / 2) - (900 / 2))}+"f"{int((self.win.winfo_screenheight() / 2) - (685 / 2))}")
        self.win.grab_set()
        # produtos
        self.categories = ["Ingresso", "Pipoca", "Bebida"]

        self.Ingresso = ["INGRESSO 2D - Intei.", "INGRESSO 2D - Meia  ", "INGRESSO 3D - Intei.", "INGRESSO 3D - Meia  "]
        self.Pipoca = reserva.alimentos().lista_pipocas
        self.Bebida = reserva.alimentos().lista_bebidas

        # Variaveis
        self.cname = StringVar()
        self.cmob = StringVar()
        self.cbill = StringVar()

        self.price = DoubleVar()
        self.qty = IntVar()
        self.qty.set(self.carrinho.qtd_ticket)
        self.tlist = []

        self.win.resizable(False, False)
        space = " "
        self.win.title(space * 200 + "Tela de pagamento")

        self.img = PhotoImage(file=r"Imagens/barra.png")
        heading = Label(self.win, text="Tela de pagamento", image=self.img)
        heading.pack()

        main_frame = Frame(self.win, background="white")
        main_frame.pack(fill="both", expand=1)

        customer_frame = LabelFrame(main_frame, pady=10, height=100, text="Informações do Cliente",
                                    font=("Elephant", 15))
        customer_frame.place(x=0, y=0, width=1200)

        form_frame = LabelFrame(main_frame, height=280, pady=20, padx=20, width=410, text="Produtos",
                                font=("Elephant", 15))
        form_frame.place(x=0, y=100)

        table_frame = LabelFrame(main_frame, height=500, width=500, text="Detalhes da compra", font=("Elephant", 15))
        table_frame.place(x=400, y=100)

        ticket_frame = LabelFrame(main_frame, height=100, width=100, text="Ingresso", font=("Elephant", 15))
        #table_frame.place(x=900, y=900)

        button_frame = LabelFrame(main_frame, height=500, width=400, text="Nota de pagamento", font=("Elephant", 15))
        button_frame.place(x=0, y=380)

        # botoesmenu_frame=LabelFrame(main_frame,height=30,width=900, borderwidth=0)
        # botoesmenu_frame.place(x=0,y=0)

        # campo detalhes da compra
        Customer_Name_lbl = Label(customer_frame, text="Nome", font=("Arial", 14))
        Customer_Name_lbl.place(x=5, y=0, width=80)
        Customer_Name_txt = Entry(customer_frame, font=("Arial", 14), textvariable=self.cname)
        Customer_Name_txt.place(x=95, y=0)

        Customer_Mob_lbl = Label(customer_frame, text="CPF", font=("Arial", 14))
        Customer_Mob_lbl.place(x=340, y=0, width=80)
        Customer_Mob_txt = Entry(customer_frame, font=("times new roman", 15), textvariable=self.cmob)
        Customer_Mob_txt.place(x=430, y=0)

        # campo produtos
        Product_Cat = Label(form_frame, text="Categoria", font=("Arial", 15))
        Product_Cat.place(x=0, y=1, width=130)
        self.categories.insert(0, "Selecione categoria")
        self.Product_Cat_List = ttk.Combobox(form_frame, font=("Arial", 15), values=self.categories)
        self.Product_Cat_List.current(0)
        self.Product_Cat_List.place(x=160, y=10, width=200)

        self.Product_Cat_List.bind('<<ComboboxSelected>>', self.cat)

        Product_Sub = Label(form_frame, text="Sub Categoria", font=("Arial", 14))
        Product_Sub.place(x=0, y=60, width=130)
        self.Product_Sub_List = ttk.Combobox(form_frame, font=("Arial", 14))
        self.Product_Sub_List.place(x=160, y=60, width=200)
        self.Product_Sub_List.bind('<<ComboboxSelected>>', self.cat2)

        Product_Rate_lbl = Label(form_frame, text="Preço", font=("Arial", 14))
        Product_Rate_lbl.place(x=0, y=110, width=130)
        self.Product_Rate_txt = Entry(form_frame, font=("Arial", 14), textvariable=self.price)
        self.Product_Rate_txt.place(x=160, y=110, width=200)

        Product_Qty_lbl = Label(form_frame, text="Qtd.", font=("Arial", 14))
        Product_Qty_lbl.place(x=0, y=160, width=130)
        self.Product_Qty_txt = Entry(form_frame, font=("times new roman", 15), textvariable=self.qty)
        self.Product_Qty_txt.place(x=160, y=160, width=200)

        # campo da nota de pagamento

        scrolly = Scrollbar(table_frame, orient=VERTICAL)
        self.billarea = Text(table_frame, yscrollcommand=scrolly.set, font=("arial", 15), fg="black", height=21.5,
                             width=52)
        self.ticketarea = Text(ticket_frame, yscrollcommand=scrolly.set, font=("arial", 15), fg="black", height=21.5,
                             width=52)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.billarea.yview)
        self.billarea.pack(fill=BOTH, expand=1)

        # Button TA COMENTADO ALGUNS BOTOES PORQUE ELES NAO SERAO USADOS NA APRESENTACAO
        # self.Add_Item_Btn=Button(form_frame,text="Adicionar",font=("times new roman",15),command=self.addItem)
        # self.Add_Item_Btn.place(x=30,y=200,width=100)

        self.confirmar_Btn = Button(button_frame, text="Confirmar compra", font=("Arial", 15), command=self.print_bill)
        self.confirmar_Btn.place(x=76, y=36, width=250)

        self.Exit_Btn = Button(button_frame, text="Cancelar compra", font=("Arial", 15), command=self.quit)
        self.Exit_Btn.place(x=76, y=96, width=250)

        self.voltar_Btn = Button(button_frame, text="Voltar", font=("Arial", 15), command=self.voltar)
        self.voltar_Btn.place(x=76, y=156, width=250)

        # self.Calc_Bill_Btn=Button(form_frame,text="Total",font=("times new roman",15),command=self.makeBill)
        # self.Calc_Bill_Btn.place(x=150,y=200,width=70)

        # self.Save_Bill_Btn=Button(button_frame,text="Salvar nota",font=("times new roman",15),command=self.save_bill)
        # self.Save_Bill_Btn.place(x=30,y=25,width=100)

        # self.Print_Btn=Button(button_frame,text="Imprimir",font=("times new roman",15),command=self.print_bill)
        # self.Print_Btn.place(x=150,y=25,width=90)

        # self.Reset_Btn=Button(form_frame,text="Limpar",font=("times new roman",15),command=self.reset)
        # self.Reset_Btn.place(x=240,y=200,width=80)

        # self.voltar_Btn=Button(botoesmenu_frame,text="Voltar",font=("times new roman",10),command=self.voltar)
        # self.voltar_Btn.place(x=0,y=5,width=80)

        self.heading()

    def ativaEntrada(self):
        self.Product_Rate_txt.config(state='normal')
        self.Product_Qty_txt.config(state='normal')
        self.Product_Qty_txt.delete(0, 'end')
        self.Product_Rate_txt.delete(0, 'end')

    def cat(self, e=' '):
        self.Product_Qty_txt.delete(0, 'end')
        if self.Product_Cat_List.get() == "Ingresso":
            self.Product_Sub_List.config(values=self.Ingresso)
            self.Product_Qty_txt.insert(END, self.carrinho.qtd_ticket)
            self.Product_Qty_txt.config(state='disabled')
            self.Product_Sub_List.current(0)

        elif self.Product_Cat_List.get() == "Pipoca":
            self.ativaEntrada()
            self.Product_Sub_List.config(values=self.Pipoca)
            self.Product_Sub_List.current(0)
        elif self.Product_Cat_List.get() == "Bebida":
            self.ativaEntrada()
            self.Product_Sub_List.config(values=self.Bebida)
            self.Product_Sub_List.current(0)

    def cat2(self, e=' '):
        temp = reserva.alimentos()
        if (self.Product_Rate_txt['state'] == 'disabled'):
            self.Product_Rate_txt.config(state='normal')
        self.Product_Rate_txt.delete(0, 'end')

        if self.Product_Sub_List.get() in self.Ingresso:
            if self.Product_Sub_List.get() == "INGRESSO 2D - Intei.":
                self.Product_Rate_txt.insert(END, self.carrinho.get_valor_unitario())
            elif self.Product_Sub_List.get() == "INGRESSO 2D - Meia  ":
                self.Product_Rate_txt.insert(END, self.carrinho.get_valor_unitario() / 2)
            elif self.Product_Sub_List.get() == "INGRESSO 3D - Intei.":
                self.Product_Rate_txt.insert(END, self.carrinho.get_valor_unitario() * 1.2)
            elif self.Product_Sub_List.get() == "INGRESSO 3D - Meia  ":
                self.Product_Rate_txt.insert(END, (self.carrinho.get_valor_unitario() * 1.2 / 2))

        # deve ter como juntar esses elses, mas falta tempo
        elif self.Product_Sub_List.get() in self.Pipoca:
            for i in self.Pipoca:
                if self.Product_Sub_List.get() == i:
                    self.Product_Rate_txt.insert(END, temp.get_valor_alimento(i))

        elif self.Product_Sub_List.get() in self.Bebida:
            for i in self.Bebida:
                if self.Product_Sub_List.get() == i:
                    self.Product_Rate_txt.insert(END, temp.get_valor_alimento(i))
        else:
            print('erro')
        self.Product_Rate_txt.config(state='disabled')
        self.Product_Qty_txt.insert(END, '1')
        self.Product_Qty_txt.config(state='disabled')
        self.addItem()

    def addItem(self):
        if self.Product_Cat_List.get() != "Selecione categoria" and self.qty != 0 and self.qty != "" and self.price.get() != 0 and self.price.get() != "":
            r = float(self.price.get())
            q = self.qty.get()
            t = r * q
            self.tlist.append(t)
            print(self.tlist)
            self.billarea.insert(END,
                                 f'\n       {q}\t       {self.Product_Sub_List.get()}       {r:05.2f}\t\t  {t:05.2f}')

    def makeBill(self):
        # if len(self.cname.get())==0 and len(self.cmob.get())==0 and len(self.cbill.get())==0:
        #    messagebox.showinfo("info","Informe os dados do cliente")

        if self.Product_Cat_List.get() == "Selecione categoria":
            messagebox.showinfo("info", "Nenhum produto selecionado!")
        elif self.price.get() == 0 or self.price.get() == "":
            messagebox.showinfo("info", "Informe o preço do produto")
        elif self.qty.get() == 0 or self.qty.get() == "":
            messagebox.showinfo("info", "Informe a quantidade do produto")
        else:
            space = " "
            total = sum(self.tlist)
            self.salva_bd_pedido()
            self.billarea.insert(3.16, self.cname.get())
            self.billarea.insert(4.16, self.cmob.get())
            self.billarea.insert(END, "\n-----------------------------------------------------------------------")
            self.billarea.insert(END, f'\n Total={space * 55} {total}')
            q = self.billarea.get(1.0, 'end-1c')
            filename = tempfile.mktemp('.txt')
            open(filename, 'w').write(q)
            os.startfile(filename, "print")
           # f = open("ingresso.txt", "w+")
           # f.write(f' ingresso=toral : {total}')
            for i in range(self.carrinho.qtd_ticket):
                self.ticketarea.insert(END, "-----------------------------------------\n")
                self.ticketarea.insert(END, "INGRESSO CINEMALOCAL      \n")
                self.ticketarea.insert(END, f'Filme: {self.carrinho.nome_filme} {self.carrinho.tipo_filme}\n')
                self.ticketarea.insert(END, f'Horario: {self.carrinho.horario}\n')
                self.ticketarea.insert(END, f'Sessao: {self.carrinho.sessao}\n')
                self.ticketarea.insert(END, f'Poltrona: {self.carrinho.poltronaNum[i]}\n')
                self.ticketarea.insert(END, "-----------------------------------------\n")
            q = self.ticketarea.get(1.0, 'end-1c')
            filename2 = tempfile.mktemp('.txt')
            open(filename2, 'w').write(q)
            os.startfile(filename2, "print")

           # f.close()
            janelas.Filme.btn_confirma(self.principalobj)
            self.quit()
    def salva_bd_pedido(self):
        total = sum(self.tlist)
        self.carrinho.set_nome_cliente(self.cname.get())
        self.carrinho.set_cpf_cliente(self.cmob.get())
        self.carrinho.set_valor_total(total)
        self.carrinho.finaliza_pedido()
    def save_bill(self):
        opt = messagebox.askyesno("Bill", "Deseja salvar conta?")
        if opt == True:
            self.bill_data = self.billarea.get(1.0, END)
            fh = open("bill/" + self.cbill.get() + ".txt", 'w')
            fh.write(self.bill_data)
            fh.close()

    def print_bill(self):
        # self.addItem()
        self.makeBill()

    def reset(self):
        self.billarea.delete(1.0, END)
        self.heading()

    def quit(self):
        self.win.destroy()
        self.destruirJan.destroy()
        janelas.Filme.voltar(self.principalobj)
        self.window = self.win

    def heading(self):
        self.billarea.delete(1.0, END)
        self.billarea.insert(END, " CINEMALOCAL NOTA ")
        self.billarea.insert(END, "\n-----------------------------------------------------------------------")
        self.billarea.insert(END, f'\nNome:\t')
        self.billarea.insert(END, f'\nCPF :\t')
        self.billarea.insert(END, "\n-----------------------------------------------------------------------")
        self.billarea.insert(END, f'\nQuantidade\t             Produto\t                 Preço \t\t  Total')

    def voltar(self):
        self.win.destroy()


"""if __name__=='__main__':
    win=Tk()
    carrinho = reserva.Reserva()
    carrinho.add_ticket()
    carrinho.add_ticket()
    carrinho.set_sessao(1)
    app=Store(win,carrinho)
    win.mainloop()"""
