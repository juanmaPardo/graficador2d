#Librerias helpers
import numpy as np

from matplotlib import pyplot as ppl
import seaborn as sb

class Graficador:
    def __init__(self,filas,col):
        self.figura, self.axes = ppl.subplots(filas,col,figsize=(8.6,6))
        self.filas = filas
        self.col = col

    

