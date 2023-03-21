
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class Envio_Imagenes(GridLayout):
    def __init__(self, **kwargs):
        super(Envio_Imagenes, self).__init__(**kwargs)

        self.cols = 2

        self.Btn = Button(text= "agrega")
        self.Btn.bind(on_press=self.press)
        self.add_widget(self.Btn)