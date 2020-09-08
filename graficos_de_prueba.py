from graficador import Graficador
from Linea2D import Linea2D
import numpy as np
import time
from matplotlib.animation import FuncAnimation

def set_de_graficos_uno():
    #Defino La linea
    linea = Linea2D(color="#c82b35",estiloLinea="dotted",estiloPunto=".")
    linea.set_color_punto("#f45ddc")
    linea.set_tamanio_punto(20)
    linea.set_color_contorno_punto("#ffffff")

    linea2 = Linea2D(color="#5d1313",estiloLinea="solid",estiloPunto="o")
    linea2.set_color_punto("#d9bf36")
    linea2.set_tamanio_punto(10)
    linea2.set_color_contorno_punto("#ffffff")

    #Instancio clase
    graficador = Graficador(['0,0','0,1','0,2'],1,3,estilo=["seaborn"])

    #Realizo Grafico Uno
    graficador.set_ax_metadata__(0,titulo="Combinacion graficos",x_label="Eje x",y_label="Eje y")
    graficador.g2d_graficar(0,[1,2,3,4,5,6],[1,2,3,4,5,6],linea,"Dotted line","upper left")
    graficador.g2d_graficar(0,[1,2,3,4,5,6],[6,5,4,3,2,1],linea2,"Solid line","upper center")

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
    #Defino La linea
    linea = Linea2D(color="#c82b35",estiloLinea="dotted",estiloPunto=".")
    linea.set_color_punto("#f45ddc")
    linea.set_tamanio_punto(20)
    linea.set_color_contorno_punto("#ffffff")
    # #Instancio clase
    graficador = Graficador(['0,0','0,1:','1,0','1,1:'],2,3,estilo=["seaborn"])

    #Realizo grafico numero uno
    linea.set_opaquedad(0.7)
    graficador.set_ax_metadata__(0,titulo="Prueba Opaquidad")
    graficador.g2d_graficar(0,[1,2,3,4,5,6],[1,2,3,4,5,6],linea,"Aproximation","upper left")
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
    def turn_white_and_black(vector):
        return ["#ffffff" if x<0.5 else "#000000" for x in vector]
    def turn_blank(vector):
        return ["" for _ in vector]

    def animate(graficador):
        matrix = np.random.rand(5,5)
        black_and_white_matrix = np.array(list(map(turn_white_and_black,matrix)))
        empty_string_matrix = np.array(np.array(list(map(turn_blank,matrix))))
        graficador.tabla(empty_string_matrix,c_celdas=black_and_white_matrix)
        time.sleep(2)
        
    graficador = Graficador(["0,0"],filas=1,col=1,estilo="seaborn")
    ani = FuncAnimation(graficador.figura,lambda i: animate(graficador),interval=1000)
    graficador.display_graficos()



set_de_graficos_uno()
set_de_graficos_numero_dos()
set_de_graficos_numero_tres()
set_de_graficos_numero_cuatro()

#tabla_interactiva()



