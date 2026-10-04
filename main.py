from kivy.uix.scrollview import ScrollView
from datetime import datetime, date
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import sp  

class InterfacciaApp(BoxLayout):
    def __init__(self, **kwargs):
        super(InterfacciaApp, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        # 1. Griglia che conterrà i 6 blocchi
        self.griglia_input = GridLayout(cols=2, rows=3, spacing=15, size_hint_y=0.3)
        
        # Valori di default validi (GG/MM/AA)
        self.blocco1, self.input1 = self.crea_campo_descrittivo("Data Acquisto: ", "01/01/24")
        self.blocco2, self.input2 = self.crea_campo_descrittivo("Data Vendita: ", "01/01/26")
        self.blocco3, self.input3 = self.crea_campo_descrittivo("Prezzo Acquisto %:", "100")
        self.blocco4, self.input4 = self.crea_campo_descrittivo("Rendimento Lordo %:", "4.5")
        self.blocco5, self.input5 = self.crea_campo_descrittivo("Capitale Investito Euro:", "10000")
        self.blocco6, self.input6 = self.crea_campo_descrittivo("Pagamento Rate mesi:", "6")
        
        self.griglia_input.add_widget(self.blocco1)
        self.griglia_input.add_widget(self.blocco2)
        self.griglia_input.add_widget(self.blocco3)
        self.griglia_input.add_widget(self.blocco4)
        self.griglia_input.add_widget(self.blocco5)
        self.griglia_input.add_widget(self.blocco6)
        
        self.add_widget(self.griglia_input)

        # 2. Bottone centrale
        self.bottone_calcola = Button(text='Calcola Rendimento', size_hint_y=0.12, background_color=(0.2, 0.6, 1, 1))
        self.bottone_calcola.bind(on_press=self.elabora_testo)
        self.add_widget(self.bottone_calcola)

        # 3. Pannello di scrittura / Output
        self.scroll_view = ScrollView(size_hint_y=0.43)
        
        self.pannello_scrittura = Label(
            text='I dati elaborati appariranno qui...',
            size_hint_y=None,        # Fondamentale per far funzionare lo scroll
            text_size=(None, None),  # Permette il calcolo dinamico delle dimensioni
            halign='left',
            valign='top',
            padding=(10, 10)
        )
        # Questo comando adatta l'altezza della Label in base alla lunghezza del testo inserito
        self.pannello_scrittura.bind(texture_size=self.pannello_scrittura.setter('size'))
        
        # Aggiungiamo la Label dentro la ScrollView, e la ScrollView all'interfaccia
        self.scroll_view.add_widget(self.pannello_scrittura)
        self.add_widget(self.scroll_view)

        # 4. Bottone Uscita
        self.bottone_esci = Button(text='Esci', size_hint_y=0.12, background_color=(0.2, 0.6, 1, 1))
        self.bottone_esci.bind(on_press=self.esci)
        self.add_widget(self.bottone_esci)

    def crea_campo_descrittivo(self, testo_label, valore_iniziale):
        contenitore = BoxLayout(orientation='vertical', spacing=2)
        label = Label(text=testo_label, halign='left', valign='middle', size_hint_y=0.3)
        label.bind(size=label.setter('text_size')) 
        input_text = TextInput(text=valore_iniziale, multiline=False, size_hint_y=0.7, font_size=sp(22))
        contenitore.add_widget(label)
        contenitore.add_widget(input_text)
        return contenitore, input_text

    def elabora_testo(self, instance):
        try:
            VR = 100     
            A = 0.125    
            
            DATA_ACQUISTO = self.input1.text.strip()
            DATA_VENDITA = self.input2.text.strip()
            PREZZO_ACQUISTO = float(self.input3.text)
            CLA = float(self.input4.text) / 100  
            CAPITALE_INVESTITO = float(self.input5.text)
            PAGAMENTO_RATE = int(self.input6.text)  
            
            # Conversione sicura stringa -> oggetto date 
            D1 = datetime.strptime(DATA_ACQUISTO, "%d/%m/%y").date()
            D2 = datetime.strptime(DATA_VENDITA, "%d/%m/%y").date()
            
            # Calcoli finanziari
            NQ = int(CAPITALE_INVESTITO / PREZZO_ACQUISTO)
            GCC = round((VR - PREZZO_ACQUISTO) * NQ, 2)    
            VN = round(VR * NQ, 2)
            
            # Calcolo durata
            NA, ANNI, MESI, GIORNI = self.Durata_anni(D1, D2)
            
            GTC = round(VN * CLA * NA, 2)
            
            if GCC > 0:
                R = round((GCC + GTC) * (1 - A), 2)
            else:
                R = round(GCC + GTC * (1 - A), 2)
            
            RP = round((R / CAPITALE_INVESTITO) * 100, 3)
            RPMA = round(RP / NA, 3) if NA > 0 else 0.0
            
            # Calcolo delle rate testuali
            testo_rate, num_rate = self.CalcolaRate(D1, D2, PAGAMENTO_RATE, R)
            
            risultato = (
                f"--- RIEPILOGO FINANZIARIO ---\n"
                f"- Guadagno Conto Capitale: {GCC} Euro\n"
                f"- Valore Nominale: {VN} Euro\n"
                f"- Durata Anni Totale: {NA:.4f} (Anni: {ANNI}, Mesi: {MESI}, Giorni: {GIORNI})\n"
                f"- Guadagno Totale Cedole: {GTC} Euro\n"
                f"- Rendimento Netto Complessivo: {R} Euro\n"
                f"- Rendimento Totale: {RP} %\n"
                f"- Rendimento Medio Annuo: {RPMA} %\n\n"
                f"--- SCADENZIARIO CEDOLE (Totale Rate: {num_rate}) ---\n"
                f"{testo_rate}"
            )
            self.pannello_scrittura.text = risultato
            
        except ValueError as e:
            self.pannello_scrittura.text = f"Errore nell'inserimento dati: verifica che i numeri siano corretti e che le date siano in formato GG/MM/AA.\nDettaglio: {e}"
        except Exception as e:
            self.pannello_scrittura.text = f"Errore imprevisto: {e}"

    def esci(self, instance):
        App.get_running_app().stop()

    def Durata_anni(self, Data_acquisto, Data_vendita):
        anni = Data_vendita.year - Data_acquisto.year
        mesi = Data_vendita.month - Data_acquisto.month
        giorni = Data_vendita.day - Data_acquisto.day
           
        if giorni < 0:
            mesi -= 1
            anno_precedente = Data_vendita.year if Data_vendita.month > 1 else Data_vendita.year - 1
            mese_precedente = Data_vendita.month - 1 if Data_vendita.month > 1 else 12
            ultimo_giorno_mese_precedente = (date(Data_vendita.year, Data_vendita.month, 1) - date(anno_precedente, mese_precedente, 1)).days
            giorni += ultimo_giorno_mese_precedente
        
        if mesi < 0:
            anni -= 1            
            mesi += 12 
            
        totale_anni = round(anni + mesi/12 + giorni/365, 4)  
        return totale_anni, anni, mesi, giorni

    def CalcolaRate(self, Data_acquisto, Data_vendita, Pag_Rate_Mesi, RendimentoNetto):
        Totale_Anni, Anni, Mesi, Giorni = self.Durata_anni(Data_acquisto, Data_vendita)
        NumRate = int((Anni * 12 + Mesi) / Pag_Rate_Mesi)
        
        Anno = Data_acquisto.year
        Mese = Data_acquisto.month
        # CORREZIONE: Usiamo il giorno reale di acquisto per calcolare la ricorrenza della cedola
        giorno_cedola = Data_acquisto.day 
        
        stringa_output = ""
        importo_rata = round(RendimentoNetto / NumRate, 2) if NumRate > 0 else 0.0
        
        for I_X_FOR in range(NumRate - 1):
            Mese += Pag_Rate_Mesi
            while Mese > 12:
                Anno += 1
                Mese -= 12
            
            # Controllo di sicurezza per i mesi corti (es. se giorno_cedola è 31, a febbraio diventa 28 o 29)
            giorno_valido = giorno_cedola
            while giorno_valido > 28:
                try:
                    DUMMY_DATA = date(Anno, Mese, giorno_valido)
                    break
                except ValueError:
                    giorno_valido -= 1
            else:
                DUMMY_DATA = date(Anno, Mese, giorno_valido)
            
            data_formattata = DUMMY_DATA.strftime("%d/%m/%Y")
            stringa_output += f"Rata {I_X_FOR + 1}: {data_formattata} -> {importo_rata} Euro\n"
            
        if NumRate > 0:
            data_vendita_formattata = Data_vendita.strftime("%d/%m/%Y")
            stringa_output += f"Rata {NumRate}: {data_vendita_formattata} -> {importo_rata} Euro\n"
        
        return stringa_output, NumRate

class MyApp(App):
    def build(self):
        self.title = 'Calcola Rendimento BTP'
        return InterfacciaApp()

if __name__ == '__main__':
    MyApp().run()
