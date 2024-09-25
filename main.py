from tkinter import *
from tkinter import Tk, ttk

# Importando Pillow
from PIL import Image, ImageTk

# Importando barra de progresso do Tkinter
from tkinter.ttk import Progressbar

# Importando MatPlotLib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Importando Calendário
from tkcalendar import Calendar, DateEntry
from datetime import date

# Importando MeesageBox
from tkinter import messagebox

# Importando funções da View
from view import inserir_categoria,inserir_gastos,inserir_receita,bar_valores, percentagem_valor
from view import ver_categoria,ver_gastos, tabela, deletar_gastos,deletar_receitas, pie_valores
# CORES
co0 = "#2e2d2b" # Preto
co1 = "#feffff" # Branco
co2 = "#4fa882" # Verde
co3 = "#38576b" # Valor
co4 = "#403d3d" # letra
co5 = "#e06636" # - profit
co6 = "#038cfc" # azul
co7 = "#3fbfb9" # Verde
co8 = "#263238" # 
co9 = "#e9edf5" # 

colors = ['#5588bb', '#66bbbb', '#99bb55', '#ee9944', '#444466', '#bb5555']

# Criando Janela
janela = Tk()
janela.title()
janela.geometry('900x650')
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")

# Criando os Frames para dividir a tela
frame_cima = Frame(janela, width=1043, height=50, bg=co1, relief='flat')
frame_cima.grid(row=0, column=0)

frame_meio = Frame(janela, width=1043, height=361, bg=co1, pady=20, relief='raised')
frame_meio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frame_baixo = Frame(janela, width=1043, height=300, bg=co1, relief='flat')
frame_baixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)



# Trabalhando no Frame de Cima
# Abrindo a imagem
app_img = Image.open('logo.jpeg')
app_img = app_img.resize((45,40))
app_img = ImageTk.PhotoImage(app_img)

# Criando Label
app_logo = Label(frame_cima, image=app_img, text=" Planejamento Financeiro", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co4)
app_logo.place(x=0,y=0)


# Definindo Função Global
global tree

# Função inserir categoria
def inserir_categoria_b():
    nome = e_n_categoria.get()

    lista_inserir = [nome]

    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
    inserir_categoria(lista_inserir)
    messagebox.showinfo('Sucesso!', 'Os valores foram incluídos com sucesso!') 

    e_n_categoria.delete(0, 'end')
    
    # Pegando os valores da categoria
    categorias_funcao = ver_categoria()
    categoria = []

    for i in categorias_funcao:
        categoria.append(i[1])

    # Atualizando a lista de categorias
    combo_categoria_despesa['value'] = (categoria)


def inserir_receitas_b():

    nome = 'Receita'
    data = e_cal_data.get()
    quantia = e_quantia_total.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
    # Chamando inserir receitas presentes em view
    inserir_receita(lista_inserir)
    messagebox.showinfo('Sucesso!', 'O dados foram incluídos com sucesso!')

    e_cal_data.delete(0, 'end')
    e_quantia_total.delete(0, 'end')


    # Atualizando dados
    mostrar_renda()
    percentagem()
    grafico_bar()
    resumo()
    grafico_pie()
    

def inserir_despesas_b():
    nome = combo_categoria_despesa.get()
    data = e_cal_despesas.get()
    quantia = e_valor_despesa.get()


    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
    # Chamando inserir receitas presentes em view
    inserir_gastos(lista_inserir)
    messagebox.showinfo('Sucesso!', 'O dados foram incluídos com sucesso!')

    combo_categoria_despesa.delete(0,'end')
    e_cal_despesas.delete(0,'end')
    e_valor_despesa.delete(0,'end')



    # Atualizando dados
    mostrar_renda()
    percentagem()
    grafico_bar()
    resumo()
    grafico_pie()

# Função deletar
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]

        if nome == 'Receita':
            deletar_receitas([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso!')

            mostrar_renda()
            percentagem()
            grafico_bar()
            resumo()
            grafico_pie()

        else:
            deletar_gastos([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso!')

            mostrar_renda()
            percentagem()
            grafico_bar()
            resumo()
            grafico_pie()

    except IndexError:
        messagebox.showerror('Erro', 'Seleciona um dos dados na tabela')


    


# Porcentagem

def percentagem():
    l_nome = Label(frame_meio, text="Porcentagem da Receita Gasta", height=1, anchor=NW, font=("Verdana 12",), bg=co1, fg=co4)
    l_nome.place(x=10, y=0)
    #Estilizando barra de progresso
    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background=co6)
    style.configure("TProgressbar", tickness=25)

    bar = Progressbar(frame_meio, length=190, style="black.Horizontal.TProgressbar")
    bar.place(x=15, y=30)
    bar['value'] = percentagem_valor()[0]

    # Criando valor da porcentagem
    valor= percentagem_valor()[0]
    l_nome = Label(frame_meio, text=(f'{valor:,.2f}%'),anchor=CENTER, font=("Verdana 12 bold",), bg=co1, fg=co4)
    l_nome.place(x=215, y=28)


# Função para gráfico bars

def grafico_bar():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valores()
    
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    

    ax.bar(lista_categorias, lista_valores,  color=colors, width=0.9)
    

    c = 0
    
    for i in ax.patches:
        
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')
        c += 1

    ax.set_xticklabels(lista_categorias,fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frame_meio)
    canva.get_tk_widget().place(x=10, y=70)


# Função de Resumo total
def resumo():
    valor = bar_valores()
    # Criando linhas do valor total mensal
    l_linha = Label(frame_meio, text="", width=215, height=1, anchor=NW, font="Arial 1", bg='#545454')
    l_linha.place(x=309, y=52)
    l_sumario = Label(frame_meio, text="Renda Total Mensal               ".upper(), height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=306, y=35)
    l_sumario = Label(frame_meio, text='R${:,.2f}'.format(valor[1]), height=1,anchor=NW, font=('arial 17 '), bg=co1, fg='#545454')
    l_sumario.place(x=306, y=60)

    # Criando linhas do total de despesas mensais
    l_linha = Label(frame_meio, text="", width=220, height=1, anchor=NW, font="Arial 1", bg='#545454')
    l_linha.place(x=306, y=132)
    l_sumario = Label(frame_meio, text="Gasto Total Mensal      ".upper(), height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=306, y=115)
    l_sumario = Label(frame_meio, text='R${:,.2f}'.format(valor[1]), height=1,anchor=NW, font=('arial 17 '), bg=co1, fg='#545454')
    l_sumario.place(x=306, y=140)

    # Criando linhas do total de despesas mensais
    l_linha = Label(frame_meio, text="", width=215, height=1, anchor=NW, font="Arial 1", bg='#545454')
    l_linha.place(x=306, y=207)
    l_sumario = Label(frame_meio, text="Saldo Total                       ".upper(), height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=306, y=190)
    l_sumario = Label(frame_meio, text='R${:,.2f}'.format(valor[1]), height=1,anchor=NW, font=('arial 17 '), bg=co1, fg='#545454')
    l_sumario.place(x=306, y=215)


# Função do Gráfico em pizza

# Frame do Gráfico pie para alteração de posição
frame_gra_pie = Frame(frame_meio, width=580, height=250, bg=co2)
frame_gra_pie.place(x=415, y=5)

def grafico_pie():
    # faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)
    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    explode = []
    for i in lista_categorias:
        explode.append(0.05)
    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)

percentagem()
grafico_bar()
resumo()
grafico_pie()


#Criando Frames dentro do frame de baixo
frame_renda= Frame(frame_baixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0,column=0)

frame_operacoes= Frame(frame_baixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0,column=1, padx=5)

frame_configuracao = Frame(frame_baixo, width=200, height=250, bg=co1)
frame_configuracao.grid(row=0,column=2, padx=5)


# Tabela de Renda Mensal
label_tabela = Label(frame_meio, text="Tabela de Gastos", anchor=NW, font=('Verdana 15'), bg=co1, fg=co4)
label_tabela.place(x=5,y=300)

# funcao para mostrar_renda
def mostrar_renda():
    # Criando cabeçalhos
    tabela_head = ['#Id','Categoria','Data','Valor']

    lista_itens = tabela()

    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)

    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        # Ajusta a coluna de acordo com o tamanho do cabeçalho
        tree.column(col, width=h[n],anchor=hd[n])

        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)

mostrar_renda()

# Configuraões das despesas
l_info = Label(frame_operacoes, text='Insira novos gastos', height=1, anchor=NW,font='Verdana 10 bold', bg=co1, fg=co4)
l_info.place(x=10, y=10)

l_cat = Label(frame_operacoes, text='Categoria', height=1, anchor=NW,font='Ivy 10', bg=co1, fg=co4)
l_cat.place(x=10, y=40)

# Criando Categorias
categoria_funcao = [ver_categoria]
categoria = []

for i in categoria:
    categoria.append(i[1])

combo_categoria_despesa = ttk.Combobox(frame_operacoes, width=12, font='Ivy 10')
combo_categoria_despesa['values'] = (categoria)
combo_categoria_despesa.place(x=110, y=45)

# Label de DATA
l_cal_despesas = Label(frame_operacoes, text='Data', height=1, anchor=NW,font='Ivy 10', bg=co1, fg=co4)
l_cal_despesas.place(x=10, y=71)

# ComboBox Calendário
e_cal_despesas = DateEntry(frame_operacoes, width=10, background='gray', anchor=CENTER, foreground='white', borderwidth=2, year=2024)
e_cal_despesas.place(x=110, y=71)

# Label de DATA
l_cal_despesas = Label(frame_operacoes, text='Quantia Total', height=1, anchor=NW,font='Ivy 10', bg=co1, fg=co4)
l_cal_despesas.place(x=10, y=101)        

# Valor das despesas
e_valor_despesa = Entry(frame_operacoes, width=14, justify='left', relief=SOLID)
e_valor_despesa.place(x=110, y=101)


# Abrindo a imagem do botão adicionar
img_addd = Image.open('addd.png')
img_addd = img_addd.resize((17,17))
img_addd = ImageTk.PhotoImage(img_addd)
botao_inserir_receitas = Button(frame_operacoes, command=inserir_despesas_b, image=img_addd, compound=LEFT, anchor=NW, text=" Adicionar".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_inserir_receitas.place(x=110, y=130)


# operacao Excluir -----------------------
l_excluir = Label(frame_operacoes, text="Excluir Ação", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_excluir.place(x=10, y=190)

# Botao Deletar
img_delete  = Image.open('delete.png')
img_delete = img_delete.resize((20, 20))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frame_operacoes, command=deletar_dados, image=img_delete, compound=LEFT, anchor=NW, text="   Deletar".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_deletar.place(x=110, y=190)

# Textos e Caixas do FRAME DESCRIÇÃO
l_descricao = Label(frame_configuracao, text="Insira novos ganhos", height=1,anchor=NW,relief="flat", font=('Verdana 10 bold'), bg=co1, fg=co4)
l_descricao.place(x=10, y=10)

l_cal_data = Label(frame_configuracao, text="Data", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_cal_data.place(x=10, y=40)
e_cal_data = DateEntry(frame_configuracao, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024)
e_cal_data.place(x=110, y=41)

l_quantia = Label(frame_configuracao, text="Quantia Total", height=1,anchor=NW, font=('Ivy 10 '), bg=co1, fg=co4)
l_quantia.place(x=10, y=70)
e_quantia_total = Entry(frame_configuracao, width=14, justify='left',relief="solid")
e_quantia_total.place(x=110, y=71)

# Abrindo a imagem do botão adicionar
img_add_qtt = Image.open('add.png')
img_add_qtt = img_add_qtt.resize((17,17))
img_add_qtt = ImageTk.PhotoImage(img_add_qtt)
botao_inserir_receitas = Button(frame_configuracao,command=inserir_receitas_b, image=img_add_qtt, compound=LEFT, anchor=NW, text=" Adicionar".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_inserir_receitas.place(x=110, y=95)

# operacao Nova Categoria
l_descricao = Label(frame_configuracao, text="Inserir Nova Categoria", height=1,anchor=NW,relief="flat", font=('Verdana 10 bold'), bg=co1, fg=co4)
l_descricao.place(x=10, y=130)
l_n_categoria = Label(frame_configuracao, text="Categoria", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_n_categoria.place(x=10, y=160)
e_n_categoria = Entry(frame_configuracao, width=14, justify='left',relief="solid")
e_n_categoria.place(x=110, y=160)

# Botao Inserir
img_add_categoria  = Image.open('add.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
botao_inserir_categoria = Button(frame_configuracao,command=inserir_categoria_b, image=img_add_categoria, compound=LEFT, anchor=NW, text=" Adicionar".upper(), width=80, overrelief=RIDGE,  font=('ivy 7 bold'),bg=co1, fg=co0 )
botao_inserir_categoria.place(x=110, y=190)

janela.mainloop()