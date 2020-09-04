class Linea2D:
    def __init__(self,color="black",estiloPunto=".",estiloLinea="solid",tamPunto=1,
                 opaquedad=1,anchoLinea=1):
        """
        Instancia caracteristicas basicas de una linea que se usaran para el grafico

        :param color: Color de la linea
        :param estiloPuntos: ., o, |,  _, More info: https://matplotlib.org/3.3.1/api/markers_api.html#module-matplotlib.markers
        :param estiloLinea: solid, dashed, dashdot, dotted
        """
        self.color = color
        self.estiloPunto = estiloPunto
        self.estiloLinea = estiloLinea
        self.tamPunto = tamPunto
        self.colorPunto = color
        self.colorContornoPunto = color
        self.opaquedad = opaquedad
        self.anchoLinea = anchoLinea

    def set_color(self,color):
        self.color = color

    def set_estiloPunto(self,estPunto):
        self.estiloPunto = estPunto

    def set_estiloLinea(self,estLin):
        self.estiloLinea = estLin

    def set_tamanio_punto(self,tamPunto):
        self.tamPunto = tamPunto

    def set_color_punto(self,color):
        self.colorPunto = color

    def set_color_contorno_punto(self, color):
        self.colorContornoPunto = color

    def set_opaquedad(self,opaquedad):
        self.opaquedad = opaquedad

    def set_ancholinea(self,ancho):
        self.anchoLinea = ancho























































































