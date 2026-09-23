# .. Multi Bottone ..
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.config import Config

# .. Blocca resize ..
Config.set('graphics','resizable','False')
# .. Imposta il colore di sfondo della finestra (es. bianco) ..
Window.clearcolor = (1, 1, 1, 1)
Window.size = (250,350)
Window.resizable = 'False'

class MyApp(App):
    def build(self):
        self.title = "Apriporta"
        #self.theme_cls.theme_style = "Light" # o "Dark"
        #self.theme_cls.primary_palette = "Red"
        # Crea un layout
        layout = FloatLayout()
        # Crea il bottone e assegna una funzione all'evento on_press
        btn1 = Button(
            text='Apri la porta', 
            size_hint=(None,None),
            size=(300,150),
            #pos_hint={'center_x': 0.5, 'center_y': 0.5},        # .. Questo lo posizina al centro ..
            pos=(100,450),
            font_size=20,
            background_color=(0.2, 0.6, 0.8, 1))
        btn1.bind(on_press=self.apri_la_porta)
        #
        btn2 = Button(
                    text ='Chiudi la porta', 
                    size_hint=(None,None),
                    size=(300,150),
                    #pos_hint={'center_x': 0.5, 'center_y': 0.5},        # .. Questo lo posizina al centro ..
                    pos=(100,275),
                    font_size=20,
                    background_color=(0.2, 0.6, 0.8, 1))
        btn2.bind(on_press=self.chiudi_la_porta)
        #
        btn3 = Button(
                            text ='Exit', 
                            size_hint=(None,None),
                            size=(300,150),
                            #pos_hint={'center_x': 0.5, 'center_y': 0.5},        # .. Questo lo posizina al centro ..
                            pos=(100,100),
                            font_size=20,
                            background_color=(0.2, 0.6, 0.8, 1))
        btn3.bind(on_press=self.esci)
        # .. Aggiunge i bottoni al layout ..
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        return layout
    # .. Definisco le funzioni dei bottoni ..
    def apri_la_porta(btn1, instance):
        print('La porta è stata aperta!')
    def chiudi_la_porta(btn2, instance):
        print('La porta è stata chiusa!')
    def esci(btn3, instance):
        App.get_running_app().stop()
      


if __name__ == '__main__':
    MyApp().run()