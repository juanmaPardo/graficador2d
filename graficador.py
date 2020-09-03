#Librerias helpers
import numpy as np

#Clases necesarias
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpmanager import MPManager


#Librerias Graficadoras
from matplotlib import pyplot as ppl
import seaborn as sb


class Graficador:
    """
    Clase que tiene el objetivo de funcionar como API para realizar graficos de to.do tipo, haciendo uso de librerias
    graficadores entre las que se encuentre matplotlib y seaborn.
    """
    def __init__(self,filas=1,col=1):
        """
        Metodo incializador de la figura que contendra los graficos, como a su vez de un mp_manager en caso de requerir subplots
        :param filas: Cantidad de filas de graficos que contendra nuestra figura
        :param col: Cantidad de columnas de graficos que contendra nuestra figura
        """
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

    def obt_ax(self):
        """

        :return: Devuelve el subplot sobre el cual se debe realizar el siguiente grafico
        """
        if(self.mp_manager == None):
            return self.axes
        else:
            return self.mp_manager.get_ax_agraficar(self.axes)

    def g2d_graficar(self,x,y,color='black',estiloPuntos=".",estiloLinea="solid",label=None):
        """
        Genera un grafico con los puntos {(Xi,Yi)....(Xn,Yn)}

        :param x: Vector que representa los puntos en el eje horizontal
        :param y: Vector que representa los puntos en el eje vertical
        :param color: Color de la linea
        :param estiloPuntos: ., o, |,  _, More info: https://matplotlib.org/3.3.1/api/markers_api.html#module-matplotlib.markers
        :param estiloLinea: solid, dashed, dashdot, dotted
        :return:
        """
        ax = self.obt_ax()
        ax.plot(x,y,color=color,marker=estiloPuntos, linestyle=estiloLinea,label=label)

    def display_graficos(self):
        ppl.show()


graficador = Graficador(1,3)
graficador.g2d_graficar([1,2,3,4,5,6],[1,2,3,4,5,6],color="red",estiloLinea="dashed")
graficador.display_graficos()


    

