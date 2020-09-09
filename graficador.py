#Librerias helpers
import numpy as np

#Clases necesarias
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from Linea2D import Linea2D
from matplotlib.animation import FuncAnimation
from threading import Thread


#Librerias Graficadoras
from matplotlib import pyplot as ppl
import seaborn as sb


class Graficador:
    """
    Clase que tiene el objetivo de funcionar como API para realizar graficos de to.do tipo, haciendo uso de librerias
    graficadores entre las que se encuentre matplotlib y seaborn.
    """
    def __init__(self,proporciones,filas=1,col=1,estilo=["default"]):
        """
        Metodo incializador de la figura que contendra los graficos, como a su vez de un mp_manager en caso de requerir subplots
        :param filas: Cantidad de filas de graficos que contendra nuestra figura
        :param col: Cantidad de columnas de graficos que contendra nuestra figura
        :param estilo: Una lista con los estilos que tendra el grafico.
        :param proporciones: Define el lugar y el espacio que va a ocupar cada subplot.Se espera
                             recibir una lista de strings.
        Ejemplo: 3 graficos, 2 filas  y 2 columnas.
        Queremos 1 grafico chico arriba en [0,0], otro chico abajo en [1,0] y el otro largo
        que ocupe [0,1] y [1,1], entonces mandarias por parametro. ['0,0',':,1','1,0']

        Para mas informacion sobre grids = https://matplotlib.org/tutorials/intermediate/gridspec.html#sphx-glr-tutorials-intermediate-gridspec-py
        Para mas informacion sobre estilos: https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
        """

        ppl.style.use(estilo)
        self.figura = ppl.figure(constrained_layout=True)
        self.grid_spec = self.figura.add_gridspec(filas,col)
        self.axes = self.__instanciar_axes__(proporciones)

    def __instanciar_axes__(self,proporciones):
        """
        Agrega todas las axis que se indico que se iba a utilizar. Dicha cantidad de axis esta representada
        por la longitud del vector contenido en la variable proporciones

        :param proporciones: Lista de string que representa la proporcion que va a ocupar cada subplot
        """
        def definir_gridspec(proporcion):
            """
            Traduce el significado de la proporcion a una de las siguientes keywords

            num_: = En caso de que haya un numero seguido de el caracter :
            :_num = En caso de que este el caracter : seguido de un numero

            num_num = En caso que tengamos dos numeros

            num1:_num2 = Todas las filas desde el num1 para abajo en la columna num2
            num1_num2: = Todas las columnas desde el num2 para la derecha en la fila num1

            :num1_num2 = Todas las filas hasta el num1 para abajo en la columna num2
            num1_:num2: = Todas las columnas hasta el num2 en la fila num1

            num1:_:num2 = Todas las filas desde el num1 para abajo hasta la columna num2
            :num1_:num2 = Todas las filas hasta el num1, desde la columna 0 a la num2

            num1:_num2: = Desde la fila num1 en adelante desde la columna dos en adelante
            :num1_num2: = Todas las filas hasta la num1, desde la columna num2 en adelante

            num1:num2,num3  = Desde la fila num1 hasta el num2(sin incluir) en la columna num3
            num1:num2,num3: = Desde la fila num1 hasta el num2(sin incluir) de la columna num3 en adelante
            num1:num2,:num3 = Desde la fila num1 hasta el num2(sin incluir) hasta la columna num3

            num1,num2:num3 = Desde la columna num2 hasta la num3(sin incluir) en la fila num3
            num1:,num2:num3 = Desde la columna num2 hasta la num3(sin incluir) de la fila num3 en adelante
            :num1,num2:num3 = Desde la columna num2 hasta la num3(sin incluir) hasta la fila num3

            num1:num2,num3:num4 = Desde la fila num1 hasta el num2(sin incluir),
                                  Desde la columna num3 hasta la num4(sin incluir)

            :param proporcion: String que representa una proporcion a cubrir del grafico
            :return: El rango de grid que se va a utilizar en dicho subplot
            """
            prop = proporcion.strip()
            if(len(prop) == 3 and prop[0].isdigit() and prop[2].isdigit()):
                n1 = int(prop[0])
                n2 = int(prop[2])
                return self.grid_spec[n1,n2]
            if(len(prop) == 3 and prop[0].isdigit()):
                n1 = int(prop[0])
                return self.grid_spec[n1, :]
            if(len(prop) == 3 and prop[2].isdigit()):
                n2 = int(prop[2])
                return self.grid_spec[:, n2]

            if(len(prop) == 4 and prop[0] == ":"):
                n1 = int(prop[1])
                n2 = int(prop[3])
                return self.grid_spec[:n1, n2]
            if(len(prop) == 4 and prop[1] == ":"):
                n1 = int(prop[0])
                n2 = int(prop[3])
                return self.grid_spec[n1:, n2]
            if(len(prop) == 4 and prop[2] == ":"):
                n1 = int(prop[0])
                n2 = int(prop[3])
                return self.grid_spec[n1, :n2]
            if (len(prop) == 4 and prop[3] == ":"):
                n1 = int(prop[0])
                n2 = int(prop[2])
                return self.grid_spec[n1, n2:]

            if(len(prop) == 5 and prop[0] == ":" and prop[3]== ":"):
                n1 = int(prop[1])
                n2 = int(prop[4])
                return self.grid_spec[:n1, :n2]
            if(len(prop) == 5 and prop[1] == ":" and prop[4]== ":"):
                n1 = int(prop[0])
                n2 = int(prop[3])
                return self.grid_spec[n1:, n2:]
            if(len(prop) == 5 and prop[1] == ":" and prop[3] == ":"):
                n1 = int(prop[0])
                n2 = int(prop[4])
                return self.grid_spec[n1:, :n2]
            if (len(prop) == 5 and prop[0] == ":" and prop[4] == ":"):
                n1 = int(prop[1])
                n2 = int(prop[3])
                return self.grid_spec[:n1, n2:]
            if (len(prop) == 5 and prop[1] == ":" and prop[4].isdigit()):
                n1 = int(prop[0])
                n2 = int(prop[2])
                n3 = int(prop[4])
                return self.grid_spec[n1:n2,n3]
            if (len(prop) == 5 and prop[0].isdigit() and prop[3] == ":"):
                n1 = int(prop[0])
                n2 = int(prop[2])
                n3 = int(prop[4])
                return self.grid_spec[n1,n2:n3]

            if (len(prop)== 6 and prop[0].isdigit() and prop[2].isdigit() and prop[4]==":"):
                n1 = int(prop[0])
                n2 = int(prop[2])
                n3 = int(prop[5])
                return self.grid_spec[n1:n2,:n3]
            if (len(prop)== 6 and prop[0].isdigit() and prop[2].isdigit() and prop[5]==":"):
                n1 = int(prop[0])
                n2 = int(prop[2])
                n3 = int(prop[4])
                return self.grid_spec[n1:n2,n3:]
            if (len(prop)== 6 and prop[0] == ":"):
                n1 = int(prop[1])
                n2 = int(prop[3])
                n3 = int(prop[5])
                return self.grid_spec[:n1,n2:n3]
            if (len(prop)== 6 and prop[0]==":" and prop[3].isdigit() and prop[5].isdigit()):
                n1 = int(prop[0])
                n2 = int(prop[3])
                n3 = int(prop[5])
                return self.grid_spec[n1:,n2:n3]

            if (len(prop)==7):
                n1 = int(prop[0])
                n2 = int(prop[2])
                n3 = int(prop[4])
                n4 = int(prop[6])
                return self.grid_spec[n1:n2, n3:n4]

        axes = []
        for i in range(len(proporciones)):
            axes.append(self.figura.add_subplot(definir_gridspec(proporciones[i])))
        return axes

    def set_real_time_on(self,animate_func,intervalo, fargs=None):
        """
        Comienza un thread que se usara en paralelo al thread original para que tu funcion
        reciba los datos correspondientes y los grafique a tiempo real pero que al mismo tiempo
        puedas generar otros graficos en el thread propio del main

        :param animate_func: Funcion que se usara para recibir datos a tiempo real y generar el grafico
        :param intervalo: Intervalo de tiempo que se usara para llamar nuevamente a animate_func
        :param fargs: Tupla que representa los argumentos extra(ademas del intervalo) que nececita
        tu funcion animate_func
        """
        def comenzar_intervalo():
            ani = FuncAnimation(self.figura,animate_func,fargs=fargs, interval=intervalo)
            self.display_graficos()

        rt_thread = Thread(target=comenzar_intervalo)
        rt_thread.start()
        rt_thread.join()

    def g2d_graficar(self,i_axis,x,y,marker=".",c_linea="black",estilo_linea="solid",ancho_linea=1,opaquez=1,
                     c_marker="black",ec_marker="black",tam_marker=1,label=None,posLegend="upper right"):
        """
        Genera un grafico con los puntos {(Xi,Yi)....(Xn,Yn)}

        :param i_axis =Indice de la axis sobre la cual se desea graficar
        :param x: Vector que representa los puntos en el eje horizontal
        :param y: Vector que representa los puntos en el eje vertical
        :param marker: Estilo del punto. ., o, |,  _,
        :param c_linea: Color de la linea
        :param estilo_linea: Estilo de la linea. solid, dashed, dashdot, dotted
        :param ancho_linea: Ancho de la linea.
        :param opaquez: Opaquez de la linea
        :param c_marker: Color del marcador de los puntos
        :param ec_marker: Color deel contorno del marcador para los puntos
        :param tam_marker: Tamaño del marcador de los puntos
        :param label: Un string que represente el label del grafico
        :param posLegend: upper/lower/center + left/right todas las combinaciones
        :param title: Titulo del grafico
        """
        ax = self.axes[i_axis]
        ax.plot(x,y,color=c_linea,marker=marker, linestyle=estilo_linea,alpha=opaquez,
                mfc=c_marker,ms=tam_marker,mec=ec_marker,label=label,
                lw=ancho_linea)
        if label:
            ax.legend(loc=posLegend)

    def histograma(self,i_axis,x,bins=None,tam_barra=None,color_barra="#5d82c9",color_borde="black",
                   orientacion="vertical",label=None,posLegend="upper right", display_bins_ranges=False):
        """
        Realiza el grafico de un histograma en la axis correspondiente con la informacion que se
        le otorgo por parametro.

        :param i_axis =Indice de la axis sobre la cual se desea graficar
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
        ax = self.axes[i_axis]
        (_,bins,_) = ax.hist(x,bins=bins,rwidth=tam_barra,orientation=orientacion,fc=color_barra,ec=color_borde)
        indices = bins[[i%2 == 0 for i in range(len(bins))]] if not display_bins_ranges else bins
        ppl.sca(ax)
        ppl.xticks(indices) if orientacion=="vertical" else ppl.yticks(indices)
        if label:
            ax.legend(loc=posLegend)

    def histograma_conjunto(self,i_axis,x1,x2,bins1=None,bins2=None,cbarrras=["#fcb27c","#5d82c9"],cbordes=["black","black"],display_bins_ranges=False,
                  orientacion="vertical",label=[None,None],posLegend="upper right"):
        """
        Grafica dos histogramas uno arriba del otro con objetivos de comparar resultados

        :param i_axis =Indice de la axis sobre la cual se desea graficar
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
        ax = self.axes[i_axis]
        (_,bins1,_) = ax.hist(x1,bins=bins1,alpha=0.8,rwidth=0.97,orientation=orientacion,fc=cbarrras[0],ec=cbordes[0],label=label[0])
        (_,bins2,_) = ax.hist(x2,bins=bins2,alpha=0.5,orientation=orientacion,fc=cbarrras[1],ec=cbordes[1],label=label[1])
        conc_bins = np.sort(np.concatenate((bins1,bins2),axis=None))
        indices = conc_bins[[i%2 == 0 for i in range(len(conc_bins))]] if not display_bins_ranges else conc_bins
        ppl.sca(ax)
        ppl.xticks(indices) if orientacion=="vertical" else ppl.yticks(indices)
        if label:
            ax.legend(loc=posLegend)

    def grafico_tarta(self,i_axis,data,labels,colores=None,s_destacar=None,sombra=False,d_valores=False,
                      angulo_inicio=0,anchoLinea=1,opaquedad=1,posLegend="upper right"):
        """
        Realiza un grafico de tarta
        :param i_axis =Indice de la axis sobre la cual se desea graficar
        :param data: Valores por categoria
        :param colores: Categoria respectiva a los valores
        :param s_destacar: Variable que se utiliza para destacar uno de los slices de la torta.
        Las opciones disponibles son {'max','min','#insertLabelName',None}
        :param sombra: True si queres que la tarta tenga sombreado
        :param d_valores: True si queres que se haga un display de los valores al lado de su porcentaje
        :param angulo_inicio: Angulo en el cual queres que empieze la tarta
        :param anchoLinea: Ancho de la linea que separa los slices
        :param c_linea: Color de la linea que separa los slices
        :param opaquedad: Opaquedad de la linea que separa los slices
        :param titulo: Titulo del grafico
        :param posLegend: Posicion donde se encontrara la leyenda
        """
        def make_autopct(values):
            """
                Define el display que se realiza en cada slice
            """
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
            return my_autopct
        def get_explode_list(data,labels,s_destacar):
            """
            Devuelve una lista que representa el factor por el cual hay que levantar a cada
            slice
            """
            estandar = np.arange(len(labels),dtype=np.float64)
            estandar.fill(0.0)
            if(s_destacar == "max"):
                i_max = np.argmax(np.array(data))
                estandar[i_max] = 0.1
            elif(s_destacar == "min"):
                i_min = np.argmin(np.array(data))
                estandar[i_min] = 0.1
            else:
                pos_label = np.where(np.array(labels) == s_destacar)
                if(pos_label[0]):#Si devolvio una lista que no esta vacia
                    estandar[pos_label[0][0]] = 0.1
            return estandar

        ax = self.axes[i_axis]
        explode_list = get_explode_list(data,labels,s_destacar) if s_destacar else None
        auto_pct = make_autopct(data) if d_valores else "%1.1f%%"
        ax.pie(data,labels=labels,explode=explode_list,autopct=auto_pct,colors=colores, startangle=angulo_inicio,
               shadow=sombra,wedgeprops={'alpha':opaquedad,'lw':anchoLinea})
        ax.legend(loc=posLegend)

    def g2d_dispersion(self,i_axis,x,y,c="#552df4f7",s=None,marker="o",ec="face",label=None,posLegend="upper right",
                       opaquedad=1):
        """
        Grafica un grafico de dispersion
        :param i_axis =Indice de la axis sobre la cual se desea graficar
        :param x: Coordenadas X
        :param y: Coordenadas Y
        :param c: color de los puntos
        :param s: tamaño de los puntos
        :param marker: Tipo de punto
        :param ec: color del contorno de los puntos
        :param label: label del grafico
        :param posLegend: Posicion donde se encontrara la legenda
        :param titulo: titulo del grafico
        """
        ax = self.axes[i_axis]
        ax.scatter(x,y,c=c,s=s,marker=marker,edgecolor=ec,alpha=opaquedad,label=label)
        if label:
            ax.legend(loc=posLegend)

    def g2d_barras(self,i_axis,x,altura,pos_barras="vertical",c="#6369b3",ec="black",ancho_barra=0.8,opaquez=1,label=None,
                   posLegend="upper right"):
        """
        Grafica un grafico de barras vertical
        :param i_axis =Indice de la axis sobre la cual se desea graficar
        :param x: Coordenadas en el eje X
        :param altura: Altura de la barra
        :param pos_barras: vertical o horizontal
        :param c: Color de la barra
        :param ec: Color del contorno de la barra
        :param ancho_barra: Ancho de la barra
        :param opaquez: Opaquez de la barra
        :param label: Label del grafico
        :param posLegend: Posicion donde se encontrara la leyenda
        """
        ax = self.axes[i_axis]
        if(pos_barras == "vertical"):
            ax.bar(x,altura,color=c,width=ancho_barra,edgecolor=ec,alpha=opaquez,label=label)
        else:
            ax.barh(x,altura,color=c,height=ancho_barra,edgecolor=ec,alpha=opaquez,label=label)
        if label:
            ax.legend(loc=posLegend)


    def boxplot(self,i_axis,data,labels=None,c_box="black",lw_box=1.2,lw_median=1.5,c_median="#2e3fff",c_outliers="red",
                m_outliers="o",ms_outliers=5,posLegend="upper right"):
        """
        Grafica un box and whiskers plot
        :param i_axis =Indice de la axis sobre la cual se desea graficar
        :param data: Vector o vectores(en caso de nececiitar mas de un plot) a graficar
        :param labels: Labels para cada vector
        :param c_box: Color de la caja
        :param lw_box: Ancho de la linea de la caja
        :param lw_median: Ancho de la linea del 50th quartile
        :param c_median: Color de la linea del 50th quartile
        :param c_outliers: Color de los outliers
        :param m_outliers: Marker a utilizar para los outliers
        :param ms_outliers: El tammaño del marker a utilizar para los outliers
        :param posLegend: Posicion en la que se encontrara la leyenda
        """
        ax = self.axes[i_axis]
        ax.boxplot(data,labels=labels,boxprops={'color':c_box,'linewidth':lw_box},
                   flierprops={'marker':m_outliers,'markerfacecolor':c_outliers,'markersize':ms_outliers},
                   medianprops={'linewidth':lw_median,'color':c_median})
        if labels:
            ax.legend(loc=posLegend)


    def tabla(self,i_axis,data_celdas,row_labels=None,col_labels=None,posTextCeldas="center",c_colL=None,
              posTextFilas="left",posTextCol="center", c_celdas="#f6f6f6",c_rowL=None, special_cell_props=False,
              c_borde = "black",text_font=15,c_texto="black",opaquez_texto=1,peso_texto="normal"):
        """
        Grafica una tabla
        :param i_axis =Indice de la axis sobre la cual se desea graficar
        :param data_celdas: Matriz que representa el valor que cada celda tendra
        :param row_labels: Lista de la misma longitud que la cantidad de filas que tendra nuestra tabla
        representando el label asociado a cada fila
        :param col_labels: Lista de la misma longitud que la cantidad de columnas que tendra nuestra tabla
        representando el label asociado a cada columna
        :param posTextCeldas: Representa la alineacion del texto de las celdas center,right,left
        :param posTextFilas: Representa la alineacion del texto de los labels que representan las filas center,right,left
        :param posTextCol: Representa la alineacion del texto de los labels que representan las columnas center,right,left
        :param special_cell_props: True si se quiere setear caracteristicas especiales referente a la celda
        :param c_celdas: Matriz con la misma shape que data_celdas que representa el color de cada celda, o
        un string que represente un color que sera aplicado a todas las celdas
        :param c_rowL:Lista de la misma longitud que la cantidad de filas que tendra nuestra tabla
        representando el color de cada label, o un color en formato string que aplicara a todos los labels
        :param c_colL: Lista de la misma longitud que la cantidad de columnas que tendra nuestra tabla
        representando el color de cada label, o un color en formato string que aplicara a todos los labels
        """
        def is_numpy_string(array):
            """
            Evalua si un numpy array/matriz esta compuesto por strings
            :param array: Numpy array
            :return: True si el array es un vector de strings o una matriz de strings
            """
            if(len(array.shape) == 1):
                return type(array[0]) == np.str_
            elif(len(array.shape) == 2):
                return type(array[0,0]) == np.str_
            else:
                raise Exception("El array no puede ser tridimencional")
        def stringfy(array):
            """
            Transforma los elementos de un array o matriz a string
            :param array: Numpy array
            :return: String version de los elementos del array
            """
            arr = np.array(array) if type(array) != np.ndarray else array
            if(len(array.shape) == 1):
                return np.array(list(map(str,arr)))
            elif(len(array.shape) == 2):
                return np.array([list(map(str,fila)) for fila in arr])
            else:
                raise Exception("El array no puede ser tridimencional")
        def get_celdas_tabla(data_celdas):
            """
            Transofmra la data de las celdas en el formato correcto para ser recibido en la funcion
            table de matplotlib
            :param data_celdas: Matriz/vector que representa la data que tendra nuestras celdas
            :return: Numpy array representando la data de cada celda en formato string
            """
            celdas_tabla = np.array(data_celdas) if type(data_celdas) != np.ndarray else data_celdas
            return stringfy(celdas_tabla) if not is_numpy_string(celdas_tabla) else celdas_tabla
        def es_lista_elem(var):
            """
            Chekea si una variable es una lista un numpy array
            :param var: Variable
            :return: True si es una lista o np.array
            """
            return type(var) is list or type(var) is np.ndarray
        def get_color_celdas(colorCeldas,cant_filas,cant_col):
            """
            Devuelve el color de cada celda a traves de un array de la misma shape que la tabla
            :param colorCeldas: Color que tendran las celdas
            :param cant_filas: Cantidad de filas de la tabla
            :paramm cant_col: Cantidad de columnas de la tabla
            :return: Devuelve el color de cada celda a traves de un array de la misma shape que la tabla
            """
            if es_lista_elem(colorCeldas):
                return colorCeldas
            elif not colorCeldas:
                return None
            elif cant_fil == 1:
                return [c_celdas] * cant_col
            else:
                return [[c_celdas] * cant_col] * cant_filas
        def vectorizar_colores(colores,long):
            """
            Transforma a un string en una lista de colores de longitud #long
            :param colores: String rerepsentando los colores, valor nulo, o vector de colores
            :param long: Tamaño del vector
            :return: Vector que representa una lista de colores.
            """
            if es_lista_elem(colores):
                return colores

            elif not colores:
                return None

            return [colores]*long

        celdas_tabla = get_celdas_tabla(data_celdas)
        cant_fil = celdas_tabla.shape[0]
        cant_col = celdas_tabla.shape[1]
        c_celdas = get_color_celdas(c_celdas,cant_fil,cant_col)
        c_filas = vectorizar_colores(c_rowL,cant_fil)
        c_columnas = vectorizar_colores(c_colL,cant_col)
        ax = self.axes[i_axis]
        ax.axis("off")
        tabla = ax.table(cellText=celdas_tabla,rowLabels=row_labels,colLabels=col_labels,cellLoc=posTextCeldas,
                 cellColours=c_celdas,rowColours=c_filas,colColours=c_columnas,
                 colLoc=posTextCol,rowLoc=posTextFilas,loc="center")

        tabla.auto_set_font_size(False)
        tabla.set_fontsize(text_font)
        if(special_cell_props):
            for i in range(cant_fil):
                for j in range(cant_col):
                    cell= tabla[i,j]
                    cell.set_text_props(color=c_texto,fontweight=peso_texto,alpha=opaquez_texto)
                    cell.set_edgecolor(c_borde)

    def set_ax_ticks(self,i_axis,x_ticks=None,x_labels=None,y_ticks=None,y_labels=None):
        """
        Cambia los valores que se muestran en el eje x/y de la axis indicada y cambia
        dichos valores por los labels indicados en caso de ser necesario

        :param i_axis =Indice de la axis sobre la cual se desea graficar
        :param x_ticks: Coordenadas X a mostrar
        :param x_labels: Labels de las coordendas X a mostrar
        :param y_ticks: Coordendas Y a mostrar
        :param y_labels: Labels de las coordendas Y a mostrar
        """
        ax = self.axes[i_axis]
        ppl.sca(ax)
        ppl.xticks(x_ticks,labels=x_labels)
        ppl.yticks(y_ticks,labels=y_labels)

    def set_ax_metadata__(self,i_axis,titulo=None,x_label=None,y_label=None,x_font=None,y_font=None):
        """
        Define la metadata de la axis sobre la cual se esta trabajando
        :param i_axis =Indice de la axis sobre la cual se desea graficar
        :param titulo: Titulo del grafico
        :param x_label: label para el eje x
        :param y_label: label para el eje y
        :param x_font: Tamaño de la fuente del label para el eje x
        :param y_font: Tamaño de la fuente del label para el eje y
        """
        ax = self.axes[i_axis]
        ax.set_title(titulo)
        ax.set_xlabel(x_label,fontsize=x_font)
        ax.set_ylabel(y_label,fontsize=y_font)

    def dibujar_linea(self,i_axis,punto,desde,hasta,indice_ax=None,orientacion="horizontal",
                      c="black",ls="solid",lw=1,posLegend="upper right", label=None):
        """
        Dibuja una linea con slope:0 horizontal o vertical sobre el punto y el rango indicado
        :param i_axis =Indice de la axis sobre la cual se desea graficar
        :param punto: Punto Y(en caso que la linea sea horizontal) o X(en caso que sea vertical) sobre
        el cual intersectara la recta con el eje correspondiente
        :param desde: Punto en caracter porcentual (0-1) desde donde comenzara la linea
        :param hasta: Punto en caracter porcentual (0-1) hasta donde llegaragi   la linea
        :param indice_ax: El indice de la axis sobre la cual queres efectuar los cambios,
        por default siempre se tomara la ultima sobre la cual se grafico.
        :param orientacion: Horizontal o Vertical, por default sera horizontal
        :param c: Color de la linea
        :param ls: Tipo de linea, solid/dashed/dotted/...
        :param lw: Ancho de la linea
        :param posLegend: Posicion donde se encontrara la leyenda
        :param label: Label asociado a la linea
        """
        ax = self.axes[i_axis]
        if(orientacion == "horizontal"):
            ax.axhline(punto,desde,hasta,color=c,linestyle=ls,linewidth=lw,label=label)
        else:
            ax.axvline(punto,desde,hasta,color=c,linestyle=ls,linewidth=lw,label=label)
        if label:
            ax.legend(loc=posLegend)

    def display_graficos(self):
        """
           Hace un display de los graficos
        """
        ppl.show()
