#Librerias helpers
import numpy as np

#Clases necesarias
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from Linea2D import Linea2D


#Librerias Graficadoras
import matplotlib
matplotlib.use('TkAgg')
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
        self.cur_index = 0

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

        axes = []
        for i in range(len(proporciones)):
            axes.append(self.figura.add_subplot(definir_gridspec(proporciones[i])))
        return axes

    def get_axis_actual(self,saag):
        """
        :param saag: Valor booleano que define si el proximo grafico desea ser realizado
        sobre la misma axis o no.
        :return: Devuelve el subplot sobre el cual se debe realizar el siguiente grafico
        """
        cur_ax = self.axes[self.cur_index]
        self.cur_index += 1 if saag else 0
        return cur_ax

    def g2d_graficar(self,x,y,linea,label=None,posLegend="upper right",saag=True):
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
        ax = self.get_axis_actual(saag)
        ax.plot(x,y,color=linea.color,marker=linea.estiloPunto, linestyle=linea.estiloLinea,alpha=linea.opaquedad,
                mfc=linea.colorPunto,ms=linea.tamPunto,mec=linea.colorContornoPunto,label=label,
                lw=linea.anchoLinea)
        if label:
            ax.legend(loc=posLegend)

    def histograma(self,x,bins=None,tam_barra=None,color_barra="#5d82c9",color_borde="black",
                   orientacion="vertical",label=None,posLegend="upper right", display_bins_ranges=False):
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
        ax = self.get_axis_actual(True)
        (_,bins,_) = ax.hist(x,bins=bins,rwidth=tam_barra,orientation=orientacion,fc=color_barra,ec=color_borde)
        indices = bins[[i%2 == 0 for i in range(len(bins))]] if not display_bins_ranges else bins
        ppl.sca(ax)
        ppl.xticks(indices) if orientacion=="vertical" else ppl.yticks(indices)
        if label:
            ax.legend(loc=posLegend)

    def histograma_conjunto(self,x1,x2,bins1=None,bins2=None,cbarrras=["#fcb27c","#5d82c9"],cbordes=["black","black"],display_bins_ranges=False,
                  orientacion="vertical",label=[None,None],posLegend="upper right"):
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
        ax = self.get_axis_actual(True)
        (_,bins1,_) = ax.hist(x1,bins=bins1,alpha=0.8,rwidth=0.97,orientation=orientacion,fc=cbarrras[0],ec=cbordes[0],label=label[0])
        (_,bins2,_) = ax.hist(x2,bins=bins2,alpha=0.5,orientation=orientacion,fc=cbarrras[1],ec=cbordes[1],label=label[1])
        conc_bins = np.sort(np.concatenate((bins1,bins2),axis=None))
        indices = conc_bins[[i%2 == 0 for i in range(len(conc_bins))]] if not display_bins_ranges else conc_bins
        ppl.sca(ax)
        ppl.xticks(indices) if orientacion=="vertical" else ppl.yticks(indices)
        if label:
            ax.legend(loc=posLegend)

    def grafico_tarta(self,data,labels,colores=None,s_destacar=None,sombra=False,d_valores=False,
                      angulo_inicio=0,anchoLinea=1,opaquedad=1,posLegend="upper right"):
        """
        Realiza un grafico de tarta
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

        ax = self.get_axis_actual(True)
        explode_list = get_explode_list(data,labels,s_destacar) if s_destacar else None
        auto_pct = make_autopct(data) if d_valores else "%1.1f%%"
        ax.pie(data,labels=labels,explode=explode_list,autopct=auto_pct,colors=colores, startangle=angulo_inicio,
               shadow=sombra,wedgeprops={'alpha':opaquedad,'lw':anchoLinea})
        ax.legend(loc=posLegend)

    def g2d_dispersion(self,x,y,c="#552df4f7",s=None,marker="o",ec="face",label=None,posLegend="upper right",
                       saag=True,opaquedad=1):
        """
        Grafica un grafico de dispersion
        :param x: Coordenadas X
        :param y: Coordenadas Y
        :param c: color de los puntos
        :param s: tamaño de los puntos
        :param marker: Tipo de punto
        :param ec: color del contorno de los puntos
        :param label: label del grafico
        :param posLegend: Posicion donde se encontrara la legenda
        :param titulo: titulo del grafico
        :param saag: Acronimo de "Switch axis after graphing" setear como Falso si se va a realizar
            otro grafico sobre el mismo subplot.
        """
        ax = self.get_axis_actual(saag)
        ax.scatter(x,y,c=c,s=s,marker=marker,edgecolor=ec,alpha=opaquedad,label=label)
        if label:
            ax.legend(loc=posLegend)

    def g2d_barras(self,x,altura,c="#6369b3",ec="black",ancho_barra=0.8,opaquez=1,label=None,
                   posLegend="upper right", saag=True):
        """
        Grafica un grafico de barras vertical
        :param x: Coordenadas en el eje X
        :param altura: Altura de la barra
        :param c: Color de la barra
        :param ec: Color del contorno de la barra
        :param ancho_barra: Ancho de la barra
        :param opaquez: Opaquez de la barra
        :param label: Label del grafico
        :param posLegend: Posicion donde se encontrara la leyenda
        :param saag: Acronimo de "Switch axis after graphing" setear como Falso si se va a realizar
            otro grafico sobre el mismo subplot.
        """
        ax = self.get_axis_actual(saag)
        ax.bar(x,altura,color=c,width=ancho_barra,edgecolor=ec,alpha=opaquez,label=label)
        if label:
            ax.legend(loc=posLegend)

    def set_ax_ticks(self,indice_ax=None,x_ticks=None,x_labels=None,y_ticks=None,y_labels=None):
        """
        Cambia los valores que se muestran en el eje x/y de la axis indicada y cambia
        dichos valores por los labels indicados en caso de ser necesario

        :param indice_ax:
        :param x_ticks: Coordenadas X a mostrar
        :param x_labels: Labels de las coordendas X a mostrar
        :param y_ticks: Coordendas Y a mostrar
        :param y_labels: Labels de las coordendas Y a mostrar
        """
        if not indice_ax:
            indice_ax = self.cur_index - 1 if self.cur_index >  0 else 0
        ax = self.axes[indice_ax]
        ppl.sca(ax)
        ppl.xticks(x_ticks,x_labels)
        ppl.yticks(y_ticks,y_labels)

    def set_ax_metadata__(self,indice_ax=None,titulo=None,x_label=None,y_label=None,x_font=None,y_font=None):
        """
        Define la metadata de la axis sobre la cual se esta trabajando
        :param indice_ax: El indice de la ax sobre la cual queres efectuar los cambios,
        por default siempre se tomara la ultima sobre la cual se grafico.
        :param titulo: Titulo del grafico
        :param x_label: label para el eje x
        :param y_label: label para el eje y
        :param x_font: Tamaño de la fuente del label para el eje x
        :param y_font: Tamaño de la fuente del label para el eje y
        """
        if not indice_ax:
            indice_ax = self.cur_index - 1 if self.cur_index >  0 else 0
        ax = self.axes[indice_ax]
        ax.set_title(titulo)
        ax.set_xlabel(x_label,fontsize=x_font)
        ax.set_ylabel(y_label,fontsize=y_font)

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
graficador = Graficador(['0,0','0,1','0,2'],1,3,estilo=["seaborn"])

#Realizo Grafico Uno
graficador.set_ax_metadata__(titulo="Combinacion graficos",x_label="Eje x",y_label="Eje y")
graficador.g2d_graficar([1,2,3,4,5,6],[1,2,3,4,5,6],linea,"Dotted line","upper left",saag=False)
graficador.g2d_graficar([1,2,3,4,5,6],[6,5,4,3,2,1],linea2,"Solid line","upper center",saag=True)

#Realizo Grafico Dos
graficador.set_ax_metadata__(titulo="Histograma")
graficador.histograma([1,1,2,3,2,5,6,2,1.5,6,4])

#Realizo Grafico Tres
graficador.set_ax_metadata__(titulo="Histograma conjunto",x_label="Eje x",y_label="Eje y",x_font=24,y_font=24)
graficador.histograma_conjunto([1,1,2,3,2,5,6,2,1.5,6,6],[1,3,3,2,1,3,6,8,4,5,6,4,1,2],label=["H1","H2"])

#Hago un display de los graficos
graficador.display_graficos()


# Set de graficos Numero Dos #
graficador = Graficador(['0,0'],1,1,estilo=["seaborn"])
graficador.set_ax_metadata__(titulo="Prueba solo un grafico",x_label="Eje x",y_label="Eje y")
graficador.g2d_dispersion([1,2,3,4],[1,2,3,4])
graficador.display_graficos()

# Set de graficos Numero tres #
# #Instancio clase
graficador = Graficador(['0,0','0,1:','1,0','1,1:'],2,3,estilo=["seaborn"])

#Realizo grafico numero uno
linea.set_opaquedad(0.7)
graficador.set_ax_metadata__(titulo="Prueba Opaquidad")
graficador.g2d_graficar([1,2,3,4,5,6],[1,2,3,4,5,6],linea,"Aproximation","upper left",saag=False)
graficador.g2d_dispersion([1,2,3,4,5,6],[1.2,2.2,2.8,3.7,5.1,6],s=45,opaquedad=0.8,posLegend="upper left",label="Real",saag=True)

#Realizo grafico numero dos
graficador.set_ax_metadata__(titulo="Grafico tarta")
graficador.grafico_tarta([21321,15689,26500],labels=["Perros","Loros","Tortugas"],anchoLinea=3,
                         colores=["#624848","#394f35","#f45ddc"],sombra=True,d_valores=True,
                         s_destacar="max",angulo_inicio=90)

#Realizo grafico numero tres
graficador.g2d_barras([1,2,3,4,5],[20,50,70,50,20],label="Barras")
graficador.set_ax_metadata__(titulo="Grafico barras")
graficador.set_ax_ticks(2,x_ticks=[1,2,3,4,5],x_labels=[15,20,25,30,35])

#Hago un display de los graficos
graficador.display_graficos()
