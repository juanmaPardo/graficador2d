#Librerias helpers
import numpy as np

#Clases necesarias
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from graficadorms import GraficadorMS
from graficadoros import GraficadorOS

#Librerias Graficadoras
from matplotlib import pyplot as ppl
import seaborn as sb

class Graficador:
    def __init__(self,filas=1,col=1):
        self.figura, self.axes = ppl.subplots(filas, col, figsize=(8.6, 6))
        self.t_graficador = self.__instanciar_graficador__(filas,col)

    def __instanciar_graficador__(self,filas,col):
        if(filas == 1 and col == 1):
            return GraficadorOS()
        else:
            return GraficadorMS(filas,col)

    def g2d_coneccion_lineal(self,x,y):
        return False




    

