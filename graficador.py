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
    def __init__(self,filas=1,col=1):
        """
        Clase inicializadora de la figura que contendra los graficos, como a su vez de un mp_manager en caso de requerir subplots
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

    def obt_axes(self):
        """

        :return: Devuelve el subplot sobre el cual se debe realizar el siguiente grafico
        """
        if(self.mp_manager == None):
            return self.axes
        else:
            return self.mp_manager.get_ax_agraficar(self.axes)

    #def g2d_coneccion_lineal(self,x,y):
    #    return False


Graficador(1,3)

    

