#===============================
# Classe per le eccezioni
#===============================
class ExamException(Exception):

        pass

#==================================================
# Funzione per calcolare la variazione media del numero di passeggeri per mese su un intervallo di anni
#==================================================
def compute_avg_monthly_difference(time_series, first_year_str, last_year_str):
    
    # controllo che gli argomenti first_year_str e last_year_str siano passati come stringhe, altrimenti alzo un'eccezione

    if not isinstance(first_year_str, str) or not isinstance(last_year_str, str):
         
        raise ExamException('Le date inserite non sono in formato stringa')
    
    # converto a int le stringhe che contengono cli anni
    first_year= int(first_year_str)
    last_year= int(last_year_str)
    
    # se inserisco come first_year un anno che viene dopo quello inserito come last_year alzo un'eccezione
    if first_year > last_year:
    
        raise ExamException('I dati non sono stati inseriti nel modo corretto')

    # calcolo la posizione della cell del primo anno considerato
    cell_index_first_year = (first_year - 1949)*12
    
    # faccio lo stesso per l'ultimo anno
    cell_index_last_year = (last_year - 1949)*12 + 12
    
    # creo una lista che contenga tutti i dati degli anni considerati
    period_series = time_series[cell_index_first_year: (cell_index_last_year)]

    print(f'lista_anni: "{period_series}"')
    
    # creo la lista vuota in cui caricherò i risultati delli incremento medio per ogni mese
    avg_result= []
    
    # dichiaro la variabile monthly_data e chiamo la funzione transform_to_list_of_monthly_data che mi permette di creare una lista di liste in cui ogni lista contiene i dati di un mese specifico per ogni anno considerato
    monthly_data= transform_to_list_of_monthly_data(period_series)
    
    # calcolo dell'incremento medio con la funzione average_for_month per ogni dato all'interno della mia lista 
    for data in monthly_data:
      
       avg_result.append(average_for_month(data))

    print(f'avg_result: {avg_result}')
    
    # la funzione restituisce il risultato del calcolo dell'incremento medio
    return avg_result


# dichiaro la variabile n_of_months che userò nella funzione seguente
n_of_months = 12

#=================================================
# Funzione che crea una lista di liste in cui ogni lista contiene i dati di uno specifico mese
#=================================================
def transform_to_list_of_monthly_data(period_series):
    
    # creo una lista vuota per contenere i dati di uno specifico mese
    monthly_data = []
    
    # per ogni mese in un range di 12 (mesi presenti in un anno) aggiungo alla lista precedentemente creata i dati per mese ottenuti con la funzione get_data_for_month
    for i in range(n_of_months):
        monthly_data.append(get_data_for_month(time_series, i))
    return monthly_data

#================================================
# Funzione che considera l'indice del mese e restituisce una lista con i dati del mese corrispondente
#================================================
def get_data_for_month(period_series, month_index):
    
    # considero la lista period_series e prendo in considerazione i dati numerici riferiti al numero di passeggeri e se il modulo tra l'indice e il numero del mese considerato è uguale al numero del mese allora lo aggiungo alla lista
    return [x[1] for index, x in enumerate(period_series) if (index % (n_of_months) == month_index)] 

#================================================
# Funzione che calcola l'incremento medio per ogni mese
#================================================
def average_for_month(month_series):
    # https://stackoverflow.com/questions/5314241/difference-between-consecutive-elements-in-list
    # per ogni dato nella lista dei mesi calcolo la differenza tra elementi consecutivi facendo attenzione a fare la sottrazione con minuendo appartenente all'anno successivo di quello del sottraendo
    # se il valore è -1 salta il calcolo dell'incremento
    deltas = [x - month_series[i - 1] for i, x in enumerate(month_series) if i > 0 and x != -1 and  month_series[i - 1] !=-1 ]
    
    # restituisce il risultato che cercavamo dato dalla differenza tra le differenze tra i dati di mesi di anni consecutivi calcolate prima, poi sommati e divisi per il numero di somme fatte 
    # ho arrotondato il risultato con due cifre decimali
    return round(sum(deltas) / len(deltas), 2)

   
#====================================================
# Funzione che controlla se la mia lista di timestamp contiene duplicati
#====================================================

def contains_duplicates(string_list):
    
    #ritrona un valore booleano che mi fa capire se ci sono duplicati (True= ci sono duplicati, False= non ci sono duplicati)
    return len(string_list) != len(set(string_list))

#=================================================
# Funzione che controlla che la mia lista di timestamp sia nell'ordine giusto
#=================================================
def is_sorted(string_list):
    
    # clono la mia lista e poi la ordino con la funzione sort
    string_list1 = string_list[:]
    string_list1.sort()
    
    # se le due liste (la mia lista iniziale e quella clonata e ordinata) sono uguali...
    if (string_list1 == string_list):
        
        # restituisco True in quanto la mia lista è nell'ordine giusto
        return True
    
    # altrimenti restituisco False
    return False

#===================================================
# Funzione che dalla lista creta nella classe CSVFile ne crea un'altra che contiene solo i valori corrispondenti alle date    
#===================================================    
def get_date_list(data):
  
    #lista di sole date
    return [x[0] for x in (data)]

#==============================
# Classe per file CSV
#==============================

class CSVFile:

    def __init__(self, name):
        
        # setto il nome del file
        self.name = name
        
        
        # provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except ExamException('Errore in apertura del file'):
            self.can_read = False
            


    def get_data(self):
        
        if not self.can_read:
            
            # se nell'init ho settato can_read a False vuol dire che il file non poteva essere aperto o era illeggibile, quindi alzo un'eccezione
            raise ExamException('Errore, file non aperto o illeggibile')

        else:
            # inizializzo una lista vuota per salvare tutti i dati
            data = []
    
            # apro il file
            my_file = open(self.name, 'r')

            # leggo il file linea per linea
            for line in my_file:
                
                # faccio lo split di ogni linea sulla virgola
                elements = line.split(',')
                
                # pulisco il carattere di newline dall'ultimo elemento con la funzione strip():
                elements[-1] = elements[-1].strip()
              
    
                # se NON sto processando l'intestazione...
                if elements[0] != 'date':
                   
                    #aggiungo alla lista gli elementi di questa linea
                    data.append(elements)
                   
            
            # chiudo il file
            my_file.close()
            
            # creo una lista con sole date 
        
            date_list= get_date_list(data)
            
            # controllo se ci sono duplicati
            if contains_duplicates(date_list):
                
                #se ci sono alzo un'eccezione
                raise ExamException('La lista di date contiene duplicati')
            
            # controllo che i dati contenuti nella lista siano nell'ordine corretto e se non lo sono alzo un'eccezione
            if not is_sorted(date_list):
                
                raise ExamException('La lista di date non è in ordine')

            # quando ho processato tutte le righe, ritorno i dati
            return data


#===============================
# Classe per CSVTimeSeriesFile
#===============================

class CSVTimeSeriesFile(CSVFile):
    
    def get_data(self):
        
        # chiamo la get_data del genitore 
        string_data = super().get_data()
        
        # preparo una lista per contenere i dati dei passeggeri ma in formato numerico
        numerical_data= []


        # ciclo su tutte le "righe" corrispondenti al file originale 
        for string_row in string_data:
            
            # preparo una lista di supporto per salvare la riga in "formato" nuumerico (tranne il primo elemento)
            
            numerical_row = []
            
            # ciclo su tutti gli elementi della riga con un enumeratore: cosi' ho anche l'indice "i" della posizione dell'elemento nella riga
                   
            for i, element in enumerate(string_row):
                
                if i == 0:
                    
                    # il primo elemento della riga lo lascio in formato stringa
                    numerical_row.append(element)   
                        
                else:
                    # converto a int tutti gli altri. Ma se fallisco, stampo l'errore e rompo il ciclo (e poi saltero' la riga).
                    
                    #try:
                        # controllo che il valore da inserire nella lista sia positivo altrimenti alzo un'eccezione che verrà gestita nell' except
                    element_value = int(element)
                    if element_value >=0:

                        numerical_row.append(element_value)
                    else:

                        #raise ExamException ('Valore negativo')

                    #except ExamException('Errore in conversione del valore a numerico'):
                        
                        # inserisco -1 per identificare le righe con valore non valido
                        numerical_row.append(-1)
                        
                        break
                        

                
            # aggiungo la riga in formato numerico alla lista, ma solo se sono riuscito a processare tutti gli elementi. 
            # controllo per la lunghezza

            if len(numerical_row) == len(string_row):
                numerical_data.append(numerical_row)

        return numerical_data
        
       


#==============================
#  Corpo del programma
#==============================

mio_file = CSVFile(name='data.csv')
print('Nome del file: "{}"\n'.format(mio_file.name))
print('Dati contenuti nel file: "{}"\n'.format(mio_file.get_data()))

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
print('Nome del file: "{}"\n'.format(time_series_file.name))
print('Dati contenuti nel file: "{}"\n'.format(time_series))

 


compute_avg_monthly_difference(time_series, "1959", "1960")



