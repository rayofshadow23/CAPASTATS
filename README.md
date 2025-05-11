# CAPASTATS

## Descrizione
CAPASTATS è uno strumento di analisi dei testi delle canzoni di Caparezza. Utilizzando i file LRC delle canzoni, il progetto esegue diverse analisi, come il conteggio delle parole, l'analisi del sentiment, l'identificazione di temi ricorrenti e la generazione di visualizzazioni come grafici e nuvole di parole. Il progetto permette di esplorare la struttura e i contenuti delle canzoni in modo dettagliato.

## Funzionalità principali

- **Pulizia dei testi**: rimozione di prefissi non necessari nei file LRC.
- **Analisi delle parole**: calcolo delle parole più frequenti, delle parole uniche, e analisi della ricchezza lessicale.
- **Word Cloud**: creazione di una nuvola di parole basata sulla frequenza delle parole nei testi.
- **Analisi dei temi**: rilevamento di temi specifici come politica, religione, tecnologia e amore.
- **Analisi del sentiment**: utilizzo di modelli pre-addestrati per analizzare il sentiment delle canzoni.
- **Statistiche per canzone**: numero medio di parole, parole più comuni, ricchezza lessicale, e molto altro.

## Requisiti

Per eseguire questo progetto, avrai bisogno di:

- Python 3.7+
- Le seguenti librerie Python:
  - `transformers`
  - `textblob`
  - `matplotlib`
  - `wordcloud`
  - `csv`
  - `os`
  - `re`

Puoi installare le dipendenze richieste con il comando:

```bash
pip install -r requirements.txt
```

## Come usare

1. **Carica i file LRC**: Metti i file delle canzoni in formato `.lrc` nella cartella specificata (`caparezza_lrc`).

2. **Esegui lo script**: Esegui il file `caparezza.py` per iniziare l'analisi. Questo eseguirà diverse analisi sui file, tra cui:
   - Pulizia del testo.
   - Generazione di statistiche sul numero di parole.
   - Creazione di una WordCloud.
   - Analisi dei temi e sentiment.

3. **Esegui il comando**:

   ```bash
   python capastats.py
   ```



## Esempio di output

L'esecuzione produrrà:

- Un grafico delle parole più frequenti.
- Una nuvola di parole delle parole più comuni.
- Statistiche come il numero medio di parole per canzone e la canzone con la maggiore ricchezza lessicale.
- Un file CSV con l'elenco dei temi rilevati nelle canzoni.

## Contribuire

Se desideri contribuire al progetto, puoi fare un fork del repository, apportare modifiche e inviare una pull request. Assicurati che il codice sia ben documentato e che le modifiche siano testate.

