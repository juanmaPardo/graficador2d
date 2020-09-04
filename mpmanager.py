class CantGraficosException(Exception):
    pass

class MPManager:
    """
    Clase que tiene el objetivo de organizar la manera que se realizan graficos sobre la Figure cuando estamos en una
    situacion en donde deseamos realizar mas de un grafico, es decir, ya sea la cantidad de filas o columnas que tendra nuestra
    figura es mayor a uno.
    """
    def __init__(self,filas,col):
        """
        Se inicializa la variable vIndices que tendra todos los indices posibles en donde se tiene que realizar un
        grafico como a su vez mantiene al tanto cual es el proximo indice a utilizar y la cantidad de graficos que se
        planea realizar sobre la figura.

        :param filas: Numero de filas que tendra la figura
        :param col: Numero de columnas que tendra la figura
        """
        self.mono_fila_o_col = (filas == 1) or (col == 1) #Si solo tenemos una fila o una columna
        self.vIndices = self.__instanciar_indices__(filas,col)
        self.index_actual = 0
        self.cant_graficos = len(self.vIndices)


    def __instanciar_indices__(self,filas,col):
        """
        Si solo tenemos una fila o una columna, las coordenadas en pyplot no se indican con un vector de dos posiciones
        sino con un vector de una posicion, por eso es necesario diferenciarlas y establecer una variable booleana que
        trackee si tenemos multiples filas y columnas, o nos encontramos en el caso contrario

        :param filas: Cantidad de filas de graficos que contendra nuestra figura
        :param col: Cantidad de columnas de graficos que contendra nuestra figura
        :return: una lista de indices que representara todas las coordinadas en donde se deberan realizar graficos
        """
        vIndices = []
        if(self.mono_fila_o_col):
           return range(col) if (filas == 1) else range(filas)
        else:
            for i in range(filas):
                for j in range(col):
                    vIndices.append((i,j))
            return vIndices

    def get_ax_agraficar(self,axes,saag):
        """
        :param axes: variable pertenenciente a la clase Axis que contiene tantas filas y columnas como se indico en la
        inicializacion
        :param saag: Valor booleano que define si el proximo grafico desea ser realizado
        sobre la misma axis o no. En caso de ser True se sumara 1 al valor actual del index, en caso
        de ser Falso no.
        :return: Devuelve el subplot sobre el cual se debe realizar el siguiente grafico, en caso que se desee realizar
        mas graficos de los que son posibles para los valores indicados se lanza una excepcion.
        """
        if(self.index_actual == self.cant_graficos):
            raise CantGraficosException("La cantidad de graficos que se desea realizar excede a la cantidad indicada")

        ax = None
        if(self.mono_fila_o_col):
            ax = axes[self.vIndices[self.index_actual]]
        else:
            ax = axes[self.vIndices[self.index_actual][0], self.vIndices[self.index_actual][1]]
        self.index_actual += 1 if saag else 0
        return ax




