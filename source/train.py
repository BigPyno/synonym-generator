import gensim
from gensim.models import Word2Vec
import pandas as pd
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import time
from source import utils as ut

def crea_datalist():
    # scarico il pacchetto di stopword(se non presente)
    nltk.download('stopwords')

    #estraggo le frasi dal primo dataset
    data = pd.read_csv('../data/IMDB_Dataset.csv')
    lines = data['review'].values.tolist()

    #lestraggo le frasi dal secondo dataset
    datasetAggiuntivo = open('../data/archive/movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
    nuove_frasi = [frase.split(' +++$+++ ')[-1] for frase in datasetAggiuntivo]

    #combino i due dataset
    datasetCompleto = [*lines,*nuove_frasi]

    data_list = list()
    for line in datasetCompleto:
        # rimuovo la punteggiatura
        rem_tok_punc = RegexpTokenizer(r'\w+')
        tokens = rem_tok_punc.tokenize(line)

        # converto le parole in minuscolo
        parole = [parola.lower() for parola in tokens]

        # rimuovo le stop words
        lista_stopwords = set(stopwords.words('english'))
        parole = [parola for parola in parole if not parola in lista_stopwords]

        # aggiungo le parole all lista
        data_list.append(parole)

    return data_list

def train_model(data_list):

    emb_dim = 100
    # addestro il modello word2vec
    modello = gensim.models.Word2Vec(sentences=data_list, size=emb_dim, workers=4, min_count=1)



    return modello

def training(nuoveParole):

    print('\nInizio il training..')
    inizio = time.time()

    data_list = crea_datalist()
    if nuoveParole:
        data_list.extend(nuoveParole)

    modello = train_model(data_list)

    #salvo il modello su file
    ut.scrivi_modello(modello)

    middle = time.time()
    tempo = middle - inizio

    print('\nTraining terminato')

    # dimensione vocabolario
    parole = list(modello.wv.vocab)
    print(f'Dimensione vocabolario: {len(parole)}')
    print(f'Tempo impiegato per il training: {tempo} secondi')

    print('\nCostruisco il modello grafico..')
    ut.costruisci_grafico(modello)
    finale = time.time()
    print(f'\nTempo totale impiegato:{finale-inizio}')
    print("\nOperazioni terminate, pronto all'utilizzo")

    return modello



if __name__ == "__main__":
    training(nuoveParole=[])