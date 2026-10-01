from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class InterfacciaApp(BoxLayout):
    def __init__(self, **kwargs):
        super(InterfacciaApp, self).__init__(**kwargs)
        
        # Imposta l'orientamento verticale e aggiunge un po' di spaziatura esterna (padding) e interna (spacing)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 45

        # 1. Casella di testo (Label) per visualizzare l'output o le istruzioni
        self.scatola_testo = Label(
            text="Il testo inserito comparirà qui", 
            font_size=20,
            size_hint_y=0.4 # Occupa il 40% dello spazio verticale
        )
        self.add_widget(self.scatola_testo)

        # 2. Input di testo (TextInput) a riga singola per l'inserimento dati
        self.input_utente = TextInput(
            hint_text="Scrivi qualcosa qui...", 
            multiline=False, # Disabilita il vai a capo con l'Invio
            size_hint_x=0.1, # Occupa il 30% dello spazio verticale
            size_hint_y=0.3 # Occupa il 30% dello spazio verticale           
        )
        self.add_widget(self.input_utente)

        # 2.2 Input di testo 2 (TextInput) a riga singola per l'inserimento dati
        self.input_utente2 = TextInput(
                    hint_text="Scrivi qualcosa qui...", 
                    multiline=False, # Disabilita il vai a capo con l'Invio
                    size_hint_x=0.1, # Occupa il 30% dello spazio verticale
                    size_hint_y=0.3 # Occupa il 30% dello spazio verticale           
                )
        self.add_widget(self.input_utente2)

        # 3. Pulsante (Button) per confermare l'azione
        self.pulsante_invia = Button(
            text="Invia Testo", 
            font_size=18,
            background_color=(0.2, 0.6, 1, 1), # Colore azzurro
            size_hint_y=0.3 # Occupa il 30% dello spazio verticale
        )
        # Collega il clic del pulsante alla funzione 'aggiorna_testo'
        self.pulsante_invia.bind(on_press=self.aggiorna_testo)
        self.add_widget(self.pulsante_invia)

        # 3. Pulsante (Button) per confermare l'azione
        self.pulsante_invia = Button(
            text="Nuovo Bottone", 
            font_size=18,
            background_color=(0.2, 0.6, 1, 1), # Colore azzurro
            size_hint_y=0.3 # Occupa il 30% dello spazio verticale
        )
        # Collega il clic del pulsante alla funzione 'aggiorna_testo'
        self.pulsante_invia.bind(on_press=self.aggiorna_testo)
        self.add_widget(self.pulsante_invia)


    def aggiorna_testo(self, istanza):
        # Legge il contenuto inserito nell'input di testo
        testo_recuperato = self.input_utente.text
        
        if testo_recuperato.strip():
            # Aggiorna la casella di testo (Label) principale
            self.scatola_testo.text = f"Hai scritto: {testo_recuperato}"
            # Svuota il campo di input dopo averlo inviato
            self.input_utente.text = ""
        else:
            self.scatola_testo.text = "Per favore, inserisci del testo valido!"

class EsempioKivyApp(App):
    def build(self):
        # Restituisce il layout principale creato sopra
        return InterfacciaApp()

if __name__ == '__main__':
    # Avvia l'applicazione Kivy
    EsempioKivyApp().run()
