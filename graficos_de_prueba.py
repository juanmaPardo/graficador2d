from graficador import Graficador
import numpy as np
import time
from matplotlib.animation import FuncAnimation
import random
from datetime import datetime, timedelta

def set_de_graficos_uno():

    #Instancio clase
    graficador = Graficador(['0,0','0,1','0,2'],1,3,estilo=["seaborn"])

    #Realizo Grafico Uno
    graficador.set_ax_metadata__(0,titulo="Combinacion graficos",x_label="Eje x",y_label="Eje y")
    graficador.g2d_graficar(0,[1,2,3,4,5,6],[1,2,3,4,5,6],estilo_linea="dotted",label="Dotted line",posLegend="upper left")
    graficador.g2d_graficar(0,[1,2,3,4,5,6],[6,5,4,3,2,1],label="Solid line",posLegend="upper center")

    #Realizo Grafico Dos
    graficador.set_ax_metadata__(1,titulo="Histograma")
    graficador.histograma(1,[1,1,2,3,2,5,6,2,1.5,6,4])

    #Realizo Grafico Tres
    graficador.set_ax_metadata__(2,titulo="Histograma conjunto",x_label="Eje x",y_label="Eje y",x_font=24,y_font=24)
    graficador.histograma_conjunto(2,[1,1,2,3,2,5,6,2,1.5,6,6],[1,3,3,2,1,3,6,8,4,5,6,4,1,2],label=["H1","H2"])

    #Hago un display de los graficos
    graficador.display_graficos()

def set_de_graficos_numero_dos():
    graficador = Graficador(['0,0'],1,1,estilo=["seaborn"])
    graficador.set_ax_metadata__(0,titulo="Prueba solo un grafico",x_label="Eje x",y_label="Eje y")
    graficador.g2d_dispersion(0,[1,2,3,4],[1,2,3,4])
    graficador.display_graficos()

def set_de_graficos_numero_tres():
    # #Instancio clase
    graficador = Graficador(['0,0','0,1:','1,0','1,1:'],2,3,estilo=["seaborn"])

    #Realizo grafico numero uno
    graficador.set_ax_metadata__(0,titulo="Prueba Opaquidad")
    graficador.g2d_graficar(0,[1,2,3,4,5,6],[1,2,3,4,5,6],opaquez=0.77,c_marker="red",label="Aproximation",posLegend="upper left")
    graficador.g2d_dispersion(0,[1,2,3,4,5,6],[1.2,2.2,2.8,3.7,5.1,6],s=45,opaquedad=0.8,posLegend="upper left",label="Real")

    #Realizo grafico numero dos
    graficador.set_ax_metadata__(1,titulo="Grafico tarta")
    graficador.grafico_tarta(1,[21321,15689,26500],labels=["Perros","Loros","Tortugas"],anchoLinea=3,
                             colores=["#624848","#394f35","#f45ddc"],sombra=True,d_valores=True,
                             s_destacar="max",angulo_inicio=90)

    #Realizo grafico numero tres
    graficador.g2d_barras(2,[1,2,3,4,5],[20,50,70,50,20],label="Barras")
    graficador.set_ax_metadata__(2,titulo="Grafico barras")
    graficador.set_ax_ticks(2,x_ticks=[1,2,3,4,5],x_labels=[15,20,25,30,35])
    graficador.dibujar_linea(2,23,0.2,1,label="Prueba linea horizontal")

    #Realizo grafico numero cuatro
    graficador.g2d_barras(3,[1,2,3,4,5],[20,50,70,50,20],pos_barras="horizontal",label="Barras")
    graficador.set_ax_metadata__(3,titulo="Grafico barras horizontal")
    graficador.set_ax_ticks(3,y_ticks=[1,2,3,4,5],y_labels=[15,20,25,30,35])
    graficador.dibujar_linea(3,2,0.2,0.8,orientacion="vertical",label="Prueba linea vertical")

    #Hago un display de los graficos
    graficador.display_graficos()

def set_de_graficos_numero_cuatro():
    graficador = Graficador(["0:2,0","2,0","0:2,1:","2:,1:"],filas=3,col=3,estilo="seaborn")
    data = np.array([1,2,3,4,4,5,5,2,6,2.5,6,5,4,8,-5,4.2,7,8,2.3,12,9,5,3,4,6,4.3,5.2,5,4,6.8,15])
    graficador.boxplot(0,data)

    rowL = ["Mean","varianza","Desv_estandar","Std_err"]
    mean = round(np.mean(data),2)
    varianza = round(np.sum((data - mean) ** 2) / len(data),2)
    desv_estandar = round(np.sqrt(varianza),2)
    estandar_error = round(desv_estandar / np.sqrt(len(data)),2)
    celInf = [[mean],[varianza],[desv_estandar],[estandar_error]]
    colLabel = ["Flores"]
    graficador.tabla(1,celInf,rowL,colLabel,c_celdas="#f6f6f6",c_rowL="#c176c8",c_colL="#4f4f4f")

    
    graficador.display_graficos()

def tabla_interactiva():
    def animate(i,graficador):
        def turn_white_and_black(vector):
            return ["#4f4f4f" if x < 0.5 else "#f6f6f6" for x in vector]

        def turn_blank(vector):
            return ["" for _ in vector]
        matrix = np.random.rand(20,20)
        black_and_white_matrix = np.array(list(map(turn_white_and_black,matrix)))
        empty_string_matrix = np.array(np.array(list(map(turn_blank,matrix))))
        graficador.tabla(0,empty_string_matrix,c_celdas=black_and_white_matrix)
        
    graficador = Graficador(["0,0"],filas=1,col=1,estilo="seaborn")
    graficador.set_real_time_on(animate,4000,fargs=[graficador])
    graficador.display_graficos()

def prueba_interactivo():
    def animate(i,x,y,gf):
        x.append(i)
        y.append(random.randint(0,1))
        gf.g2d_graficar(0,x,y)

    gf = Graficador(["0,0"],1,1,estilo="seaborn")
    y = []
    x = []
    gf.set_real_time_on(animate,1000,fargs=(x,y,gf))


def prueba_interactivo_dos() :
    def animate(i,x,y,gf):
        x.append(i)
        y.append(random.randint(0,1))
        gf.g2d_graficar(0,x,y)

    gf = Graficador(["0,0","0,1"],1,2,estilo="seaborn")
    y = []
    x = []
    gf.g2d_graficar(1,[1,2,3,4,5],[1,2,3,4,5])
    gf.set_real_time_on(animate,10,fargs=(x,y,gf))

def prueba_coloreado():
    graficador = Graficador(["0,0"],filas=1,col=1,estilo="seaborn")
    graficador.g2d_graficar(0,[1,2,3,4],[1,2,3,4])
    graficador.set_ax_metadata__(0,titulo="Prueba coloreado",x_label="Eje X",y_label="Eje Y",
                                 x_font=25,y_font=25)
    graficador.colorear_area(0,[1,2],[1,2],label="Area debajo de la curva",posLegend="upper left")
    graficador.display_graficos()


def discreto_vs_continuo():
    gf = Graficador(["0,0","0,1"],filas=1,col=2,estilo="seaborn")
    gf.g2d_graficar(0,[1,2,3,4,5],[1,2,3,4,5],c_linea="#d16f6f",label="Continuo")
    gf.g2d_grafico_discreto(1,[1,2,3,4,5],[1,2,3,4,5],label="Discreto")
    gf.display_graficos()

def prueba_fechas():
    dates = [
        datetime(2019, 5, 24),
        datetime(2019, 5, 25),
        datetime(2019, 5, 26),
        datetime(2019, 5, 27),
        datetime(2019, 5, 28),
        datetime(2019, 5, 29),
        datetime(2019, 5, 30)
    ]

    gf = Graficador(["0,0:"],filas=1,col=2,estilo="seaborn")
    gf.g2d_grafico_discreto(0,dates,[4,5,3,5,6,3,5],baseline=False)
    gf.format_date_axis(0)
    gf.display_graficos()


def prueba_contornos():
    gf = Graficador(["0:,0","0:,1"],filas=2,col=2,estilo="seaborn")
    X = np.array([1,2,3,4,5])
    Y = np.array([1,2,3,4,5])
    Z = np.zeros(shape=(X.shape[0],Y.shape[0]))
    Z[0,0]= 5
    Z[1,1]= 5
    Z[2,2]= 5
    Z[2,2]= 5
    Z[3,3]= 5
    gf.g2d_contour(0,X,Y,Z,niveles=5,display_level=False,fcontour=False)
    gf.display_graficos()

#2980b9
#set_de_graficos_uno()
#set_de_graficos_numero_dos()
#set_de_graficos_numero_tres()
#set_de_graficos_numero_cuatro()

#tabla_interactiva()
#prueba_interactivo()
#prueba_interactivo_dos()

#prueba_coloreado()

#discreto_vs_continuo()

#prueba_fechas()

prueba_contornos()




