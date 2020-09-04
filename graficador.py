#Librerias helpers
import numpy as np

#Clases necesarias
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpmanager import MPManager
from Linea2D import Linea2D


#Librerias Graficadoras
from matplotlib import pyplot as ppl
import seaborn as sb


class Graficador:
    """
    Clase que tiene el objetivo de funcionar como API para realizar graficos de to.do tipo, haciendo uso de librerias
    graficadores entre las que se encuentre matplotlib y seaborn.
    """
    def __init__(self,filas=1,col=1,estilo=["default"]):
        """
        Metodo incializador de la figura que contendra los graficos, como a su vez de un mp_manager en caso de requerir subplots
        :param filas: Cantidad de filas de graficos que contendra nuestra figura
        :param col: Cantidad de columnas de graficos que contendra nuestra figura
        :param estilo: Una lista con los estilos que tendra el grafico.
        
        Para mas informacion sobre estilos: https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
        """
        ppl.style.use(estilo)
        self.figura, self.axes = ppl.subplots(filas, col, figsize=(8.6, 6))
        self.mp_manager = self.__instanciar_manager__(filas,col)

    def __instanciar_manager__(self,filas,col):
        """
        En caso que solo se requiera de graficar en una sola figura mas de un grafico se inicializa
        un MPManager que se encargara de otorgarnos cuando se lo pidamos el subplot sobre el cual
        debemos trabajar

        :param filas: Cantidad de filas de graficos que contendra nuestra figura
        :param col: Cantidad de columnas de graficos que contendra nuestra figura
        :return: Una instancia de la clase MPManager que se encarga de otorgarnos el siguiente subplot sobre el cual
        debemos realizar un grafico
        """
        if(filas == 1 and col == 1):
            return None
        else:
            return MPManager(filas,col)

    def obt_ax(self,saag):
        """
        :param saag: Valor booleano que define si el proximo grafico desea ser realizado
        sobre la misma axis o no.
        :return: Devuelve el subplot sobre el cual se debe realizar el siguiente grafico
        """
        if(self.mp_manager == None):
            return self.axes
        else:
            return self.mp_manager.get_ax_agraficar(self.axes,saag)

    def g2d_graficar(self,x,y,linea,label=None,posLegend="upper right",titulo=None,saag=True):
        """
        Genera un grafico con los puntos {(Xi,Yi)....(Xn,Yn)}

        :param x: Vector que representa los puntos en el eje horizontal
        :param y: Vector que representa los puntos en el eje vertical
        :param linea: Una instancia de la clase Linea2D
        :param label: Un string que represente el label del grafico
        :param posLegend: upper/lower/center + left/right todas las combinaciones
        :param title: Titulo del grafico
        :param saag: Acronimo de "Switch axis after graphing" setear como Falso si se va a realizar
                    otro grafico sobre el mismo subplot.
        """
        ax = self.obt_ax(saag)
        ax.set_title(titulo)
        ax.plot(x,y,color=linea.color,marker=linea.estiloPunto, linestyle=linea.estiloLinea,
                mfc=linea.colorPunto,ms=linea.tamPunto,mec=linea.colorContornoPunto,label=label)
        if label:
            ax.legend(loc=posLegend)

    def histograma(self,x,bins=None,tam_barra=None,color_barra="#5d82c9",color_borde="black",
                   orientacion="vertical",label=None,posLegend="upper right",titulo=None,
                   display_bins_ranges=False):
        """
        Realiza el grafico de un histograma en la axis correspondiente con la informacion que se
        le otorgo por parametro.

        :param x: Vector de valores observados
        :param bins: Una lista con bins custom
        :param tam_barra: Tamaño relativo de la barra
        :param color_barra: Color de la barra
        :param color_borde: El color del borde de las barras del histograma
        :param orientacion: vertical por default, horizontal si lo queres al revez
        :param label: Un string que represente el label del grafico
        :param posLegend: upper/lower/center + left/right todas las combinaciones
        :param title: Titulo del grafico
        :param display_bins_ranges: True si queres que se muestren todos los rangos que determinan cada bien
                                    ya sea en el eje X o en el eje Y
        """
        ax = self.obt_ax(True)
        ax.set_title(titulo)
        (_,bins,_) = ax.hist(x,bins=bins,rwidth=tam_barra,orientation=orientacion,fc=color_barra,ec=color_borde)
        indices = bins[[i%2 == 0 for i in range(len(bins))]] if not display_bins_ranges else bins
        ppl.sca(ax)
        ppl.xticks(indices) if orientacion=="vertical" else ppl.yticks(indices)
        if label:
            ax.legend(loc=posLegend)

    def histograma_conjunto(self,x1,x2,bins1=None,bins2=None,cbarrras=["#fcb27c","#5d82c9"],cbordes=["black","black"],display_bins_ranges=False,
                  orientacion="vertical",label=[None,None],posLegend="upper right",titulo=None):
        """
        Grafica dos histogramas uno arriba del otro con objetivos de comparar resultados
        :param x1: Set de datos 1
        :param x2: Set de datos 2
        :param bins1: Bins custom para set de datos numero 1
        :param bins2: Bins custom para set de datos numero 2
        :param cbarrras: Lista que se usara para darle el color a las barras de los histogramas
        :param cbordes:  Lista que se usara para darle el color al contorno de las barras de los histogramas
        :param display_bins_ranges: True en caso que quieras ver todos los rangos de los dos histogramas
        :param orientacion: Vertical/Horizontal
        :param label: Lista de dos elementos que se usara para agregarle los labels a los histogramas
        :param posLegend: Posicion en donde queres que se encuentre la leyenda
        :param titulo: Titulo del grafico
        """
        ax = self.obt_ax(True)
        ax.set_title(titulo)
        (_,bins1,_) = ax.hist(x1,bins=bins1,alpha=0.8,rwidth=0.97,orientation=orientacion,fc=cbarrras[0],ec=cbordes[0],label=label[0])
        (_,bins2,_) = ax.hist(x2,bins=bins2,alpha=0.5,orientation=orientacion,fc=cbarrras[1],ec=cbordes[1],label=label[1])
        conc_bins = np.sort(np.concatenate((bins1,bins2),axis=None))
        indices = conc_bins[[i%2 == 0 for i in range(len(conc_bins))]] if not display_bins_ranges else conc_bins
        ppl.sca(ax)
        ppl.xticks(indices) if orientacion=="vertical" else ppl.yticks(indices)
        if label:
            ax.legend(loc=posLegend)

    def g2d_dispersion(self,saag=True):
        return false
    def display_graficos(self):
        """
           Hace un display de los graficos
        """
        ppl.show()


#Defino La linea
linea = Linea2D(color="#c82b35",estiloLinea="dotted",estiloPunto=".")
linea.set_color_punto("#f45ddc")
linea.set_tamanio_punto(20)
linea.set_color_contorno_punto("#ffffff")

linea2 = Linea2D(color="#5d1313",estiloLinea="solid",estiloPunto="o")
linea2.set_color_punto("#d9bf36")
linea2.set_tamanio_punto(10)
linea2.set_color_contorno_punto("#ffffff")

# Set de graficos Numero uno #
#Instancio clase
graficador = Graficador(1,3,estilo=["seaborn"])

#Realizo Grafico Uno
graficador.g2d_graficar([1,2,3,4,5,6],[1,2,3,4,5,6],linea,"Dotted line","upper left","Grafico de prueba",saag=False)
graficador.g2d_graficar([1,2,3,4,5,6],[6,5,4,3,2,1],linea2,"Solid line","upper center","Grafico de prueba",saag=True)

#Realizo Grafico Dos
graficador.histograma([1,1,2,3,2,5,6,2,1.5,6,4],titulo="Prueba histograma")

#Realizo Grafico Tres
graficador.histograma_conjunto([1,1,2,3,2,5,6,2,1.5,6,6],[1,3,3,2,1,3,6,8,4,5,6,4,1,2],label=["H1","H2"],titulo="Histogramas conjuntos")

#Hago un display de los graficos
graficador.display_graficos()

# Set de graficos Numero dos #
# #Instancio clase
graficador = Graficador(2,2,estilo=["seaborn"])

