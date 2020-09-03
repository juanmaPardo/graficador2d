class Linea2D:
    def __init__(self,color="black",estiloPunto=".",estiloLinea="solid"):
        """
        Instancia caracteristicas basicas de una linea que se usaran para el grafico

        :param color: Color de la linea
        :param estiloPuntos: ., o, |,  _, More info: https://matplotlib.org/3.3.1/api/markers_api.html#module-matplotlib.markers
        :param estiloLinea: solid, dashed, dashdot, dotted
        """
        self.color = color
        self.estiloPunto = estiloPunto
        self.estiloLinea = estiloLinea
        self.tamPunto = 1
        self.colorPunto = color
        self.colorContornoPunto = color

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
























































































