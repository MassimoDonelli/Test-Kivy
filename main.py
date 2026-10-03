from datetime import date
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
        
        # Inseriti valori di default validi per evitare crash immediati al click di Calcola
        self.blocco1, self.input1 = self.crea_campo_descrittivo("Data Acquisto:", "01/01/24")
        self.blocco2, self.input2 = self.crea_campo_descrittivo("Data Vendita:", "01/01/26")
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
        self.pannello_scrittura = TextInput(
            hint_text='I dati elaborati appariranno qui...',
            readonly=True, 
            size_hint_y=0.43
        )
        self.add_widget(self.pannello_scrittura)

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
            CLA = float(self.input4.text) / 100  # Convertito in decimale (es: 4.5% -> 0.045)
            CAPITALE_INVESTITO = float(self.input5.text)
            
            # CORRETTO: Cambiato da input5 a input6 per leggere i mesi delle rate
            PAGAMENTO_RATE = int(self.input6.text)  
            
            # Gestione dinamica dell'anno a 2 o 4 cifre
            d1_split = DATA_ACQUISTO.split("/")
            anno1 = int(d1_split[2])
            if anno1 < 100: anno1 += 2000
            D1 = date(anno1, int(d1_split[1]), int(d1_split[0]))
            
            d2_split = DATA_VENDITA.split('/')
            anno2 = int(d2_split[2])
            if anno2 < 100: anno2 += 2000
            D2 = date(anno2, int(d2_split[1]), int(d2_split[0]))
            
            # Calcoli finanziari
            NQ = int(CAPITALE_INVESTITO / PREZZO_ACQUISTO)
            GCC = round((VR - PREZZO_ACQUISTO) * NQ, 2)                
            VN = round(VR * NQ, 2)
            
            # Chiamata a Durata_anni (Eseguita una sola volta)
            NA, ANNI, MESI, GIORNI = self.Durata_anni(D1, D2)            
            GTC = round(VN * CLA * NA, 2)
            
            if GCC > 0:
                R = round((GCC + GTC) * (1 - A), 2)
            else:
                R = round(GCC + GTC * (1 - A), 2)
            
            RP = round((R / CAPITALE_INVESTITO) * 100, 3)
            RPMA = round(RP / NA, 3) if NA > 0 else 0.0 
            N_RATE = self.CalcolaRate(D1,D2,PAGAMENTO_RATE,R)   
            risultato = (
                f"- Guadagno Conto Capitale: {GCC} Euro\n"
                f"- Valore Nominale: {VN} Euro\n"
                f"- Durata Anni Totale: {NA:.4f} (Anni: {ANNI}, Mesi: {MESI}, Giorni: {GIORNI})\n"
                f"- Guadagno Totale Cedole: {GTC} Euro\n"
                f"- Rendimento netto: {R} Euro\n"
                f"- Rendimento totale: {RP} %\n"
                f"- Rendimento medio annuo: {RPMA} %\n"
                f"- Numero rate: {N_RATE} %\n"
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
        # CORRETTO: Aggiunto self. per chiamare il metodo della classe
        Totale_Anni, Anni, Mesi, Giorni = self.Durata_anni(Data_acquisto, Data_vendita)
        
        NumRate = int((Anni * 12 + Mesi) / Pag_Rate_Mesi)
        Anno = Data_acquisto.year
        Mese = Data_acquisto.month
        
        print("Numero Rate: ", NumRate)
        
        for I_X_FOR in range(NumRate - 1):
            Mese += Pag_Rate_Mesi
            while Mese > 12:
                Anno += 1
                Mese -= 12
            
            # Gestione del fine mese per evitare errori (es. 31 Giugno non esiste, diventa 30)
            giorno_valido = Giorni
            while giorno_valido > 28:
                try:
                    DUMMY_DATA = date(Anno, Mese, giorno_valido)
                    break
                except ValueError:
                    giorno_valido -= 1  # Scala indietro al giorno valido più vicino
            else:
                DUMMY_DATA = date(Anno, Mese, giorno_valido)
                
            print(f"Rata {I_X_FOR + 1}: {DUMMY_DATA} - {round(RendimentoNetto / NumRate, 2)} Euro")  
            
        print(f"Rata {NumRate}: {Data_vendita} - {round(RendimentoNetto / NumRate, 2)} Euro")
        return NumRate

    
class MyApp(App):
    def build(self):
        self.title = 'Calcola Rendimento BTP'
        return InterfacciaApp()

if __name__ == '__main__':
    MyApp().run()
