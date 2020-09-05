from graficador import Graficador
from Linea2D import Linea2D

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
