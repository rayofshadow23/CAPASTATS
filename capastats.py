# ========================
# 1. Importazioni
# ========================
import csv
import os
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from transformers import pipeline

# ========================
# 2. Configurazioni
# ========================
FOLDER_PATH = "lyrics"
STOPWORDS_FILE = "stop-words/italian.txt"
THEMES = {
    "politica": ["governo", "legge", "parlamento", "stato", "politico"],
    "religione": ["dio", "chiesa", "preghiera", "ges\u00f9"],
    "tecnologia": ["computer", "internet", "telefono", "software"],
    "amore": ["amore", "cuore", "passione", "bacio"]
}
EXCLUDE_PREFIXES = ("[id:", "[ar:", "[al:", "[ti:", "[length:")

# ========================
# 3. Funzioni
# ========================
def clean_lyrics(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = re.sub(r'\[\d{2}:\d{2}(?:\.\d{2})?\]', '', text)
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def load_stopwords(path):
    with open(path, "r", encoding="utf-8") as f:
        return set(word.strip().lower() for word in f if word.strip())

def most_common_words(file_path, top_n=5):
    words = clean_lyrics(file_path)
    return Counter(words).most_common(top_n)

def word_count_stats_per_song(files):
    word_counts = []
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        text = " ".join([
            re.sub(r'\[\d{2}:\d{2}(?:\.\d{2})?\]', '', line).strip()
            for line in lines if not line.startswith(EXCLUDE_PREFIXES)
        ])
        words = re.findall(r'\b\w+\b', text)
        word_counts.append((file_path, len(words)))

    if not word_counts:
        return {'media': 0, 'minimo': 0, 'massimo': 0, 'minimo_file': None, 'massimo_file': None}

    media = sum(wc for _, wc in word_counts) / len(word_counts)
    minimo_path, minimo = min(word_counts, key=lambda x: x[1])
    massimo_path, massimo = max(word_counts, key=lambda x: x[1])
    return {
        'media': media,
        'minimo': minimo,
        'minimo_file': os.path.basename(minimo_path),
        'massimo': massimo,
        'massimo_file': os.path.basename(massimo_path)
    }

def average_word_count_per_song(files):
    counts = [len(clean_lyrics(f)) for f in files]
    return sum(counts) / len(counts) if counts else 0

def lexical_richness(file_path):
    words = clean_lyrics(file_path)
    return len(set(words)) / len(words) if words else 0

def repeated_words(file_path, threshold=10):
    word_counts = Counter(clean_lyrics(file_path))
    return {w: c for w, c in word_counts.items() if c > threshold}

def detect_themes(file_path):
    words = set(clean_lyrics(file_path))
    return {theme: sum(1 for w in words if w in kws) for theme, kws in THEMES.items() if any(w in words for w in kws)}

def sentiment_analysis_textblob(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return TextBlob(file.read()).sentiment.polarity

def read_lrc_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def sentiment_analysis(text, pipe):
    # Imposta la troncatura automatica e la gestione dei batch
    result = pipe(text, truncation=True, max_length=512)
    return result

def analyze_sentiment_of_lrc_files(directory, pipe):
    for filename in os.listdir(directory):
        if filename.endswith(".lrc"):
            file_path = os.path.join(directory, filename)
            lyrics = read_lrc_file(file_path)  # Assicurati che questa funzione legga correttamente il testo
            sentiment = sentiment_analysis(lyrics, pipe)
            print(f"Sentiment per {filename}: {sentiment}")


def parola_unica_piu_usata_per_canzone(files, stopwords_set):
    risultati = []

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        text = re.sub(r'\[\d{2}:\d{2}(?:\.\d{2})?\]', '', text)
        words = re.findall(r'\b\w+\b', text.lower())
        filtered = [w for w in words if w not in stopwords_set]
        counter = Counter(filtered)
        unique_words = {w: c for w, c in counter.items() if c == 1}

        if unique_words:
            # Parola unica più lunga (opzionale: puoi scegliere anche in base a criteri diversi)
            top_word = max(unique_words.items(), key=lambda x: len(x[0]))
            risultati.append((os.path.basename(file).replace(".lrc", ""), top_word[0], top_word[1]))

    return risultati

def presenza_parole_per_canzone(files, stopwords_set):
    presenza_per_parola = Counter()

    for file in files:
        words = set(clean_lyrics(file))  # parole uniche nella canzone
        parole_filtrate = {w for w in words if w not in stopwords_set}
        for parola in parole_filtrate:
            presenza_per_parola[parola] += 1

    return presenza_per_parola

def maggior_numero_parole_uniche(files):
    max_unique_words = 0
    file_with_max_unique = ""

    for file in files:
        words = clean_lyrics(file)  # Carica e pulisci le parole dal file
        unique_words = set(words)  # Ottieni le parole uniche (senza ripetizioni)
        num_unique = len(unique_words)  # Conta il numero di parole uniche

        # Aggiorna il file con il maggior numero di parole uniche
        if num_unique > max_unique_words:
            max_unique_words = num_unique
            file_with_max_unique = os.path.basename(file).replace(".lrc", "")

    return file_with_max_unique, max_unique_words

def salva_parole_ripetute_csv(files, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "parole_ripetute.csv")

    with open(output_path, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Canzone", "Parola", "Conteggio"])

        for file in files:
            name = os.path.basename(file).replace(".lrc", "")
            repeated = repeated_words(file)
            for word, count in repeated.items():
                if count > 10:
                    writer.writerow([name, word, count])

# ========================
# 4. Codice principale
# ========================
italian_stopwords = load_stopwords(STOPWORDS_FILE)

# Pulizia iniziale dei file
for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".lrc"):
        path = os.path.join(FOLDER_PATH, filename)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        cleaned = [line for line in lines if not line.lower().startswith(EXCLUDE_PREFIXES) and line.strip()]
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(cleaned)

files = [os.path.join(FOLDER_PATH, f) for f in os.listdir(FOLDER_PATH) if f.endswith('.lrc')]

# Analisi testuale: Word Frequencies & Wordcloud
all_words = []
for file in files:
    all_words.extend(clean_lyrics(file))
filtered_words = [w for w in all_words if w not in italian_stopwords]
filtered_counts = Counter(filtered_words)
top_filtered = filtered_counts.most_common(20)

if top_filtered:
    words, counts = zip(*top_filtered)
    plt.figure(figsize=(12, 6))
    plt.bar(words, counts, color='green')
    plt.xticks(rotation=45)
    plt.title('Top 20 parole pi\u00f9 usate (senza stopword)')
    plt.tight_layout()
    plt.show()

    wordcloud = WordCloud(width=1000, height=600, background_color='white', colormap='Dark2')
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud.generate_from_frequencies(filtered_counts), interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud delle parole pi\u00f9 frequenti')
    plt.show()
else:
    print("Nessuna parola significativa trovata dopo rimozione stopword.")

# Statistiche generali
print(f"\nNumero medio di parole per canzone: {average_word_count_per_song(files):.2f}")
stats = word_count_stats_per_song(files)
print(f"Media parole:  {stats['media']:.2f}")
print(f"Minimo:        {stats['minimo']} (file: {stats['minimo_file']})")
print(f"Massimo:       {stats['massimo']} (file: {stats['massimo_file']})")

# Ricchezza lessicale
print("\nRicchezza Lessicale (TTR):")

# Variabili per tracciare la canzone con la maggiore e minore ricchezza lessicale
max_lexical_richness = -1
min_lexical_richness = float('inf')
max_file = ""
min_file = ""

# Calcola la ricchezza lessicale per ogni canzone
for file in files:
    name = os.path.basename(file).replace(".lrc", "")
    richness = lexical_richness(file)
    print(f"- {name}: {richness:.4f}")

    # Aggiorna la canzone con la ricchezza lessicale maggiore e minore
    if richness > max_lexical_richness:
        max_lexical_richness = richness
        max_file = name

    if richness < min_lexical_richness:
        min_lexical_richness = richness
        min_file = name

# Stampa la canzone con la ricchezza lessicale più alta e più bassa
print(f"\nCanzone con la ricchezza lessicale più alta: {max_file} ({max_lexical_richness:.4f})")
print(f"Canzone con la ricchezza lessicale più bassa: {min_file} ({min_lexical_richness:.4f})")

# Top 5 parole per canzone
for file in files:
    name = os.path.basename(file).replace(".lrc", "")
    print(f"\nTop 5 parole in '{name}':")
    for word, count in most_common_words(file):
        print(f"- {word}: {count}")


# Parole più ripetute in ciascuna canzone

files = [os.path.join(FOLDER_PATH, f) for f in os.listdir(FOLDER_PATH) if f.endswith(".lrc")]
salva_parole_ripetute_csv(files)




# ========================
# Salvataggio temi in CSV
# ========================
with open("outputs/temi_canzoni.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["nome_canzone", "tema", "conteggio_parole"])

    for file in files:
        name = os.path.basename(file).replace(".lrc", "")
        themes_found = detect_themes(file)
        if themes_found:
            for theme, count in themes_found.items():
                writer.writerow([name, theme, count])


def maggior_numero_parole_uniche(files):
    max_unique_words = 0
    file_with_max_unique = ""

    for file in files:
        words = clean_lyrics(file)  # Carica e pulisci le parole dal file
        unique_words = set(words)  # Ottieni le parole uniche (senza ripetizioni)
        num_unique = len(unique_words)  # Conta il numero di parole uniche

        # Aggiorna il file con il maggior numero di parole uniche
        if num_unique > max_unique_words:
            max_unique_words = num_unique
            file_with_max_unique = os.path.basename(file).replace(".lrc", "")

    return file_with_max_unique, max_unique_words


# Utilizzo della funzione
file_name, unique_count = maggior_numero_parole_uniche(files)
print(f"\nLa canzone con il maggior numero di parole uniche è '{file_name}' con {unique_count} parole uniche.")


# Analisi sentiment con modello BERT italiano
#model_name = "MilaNLProc/feel-it-italian-sentiment"
#pipe = pipeline("sentiment-analysis", model=model_name, framework="pt")

#FOLDER_PATH = "lyrics"
#analyze_sentiment_of_lrc_files(FOLDER_PATH, pipe)


# Calcolo parole presenti in più canzoni (una volta per canzone)
presenza_counter = presenza_parole_per_canzone(files, italian_stopwords)

# Istogramma: top 20 parole più presenti
top20 = presenza_counter.most_common(20)
if top20:
    parole, conteggi = zip(*top20)
    plt.figure(figsize=(12, 6))
    plt.bar(parole, conteggi, color='blue')
    plt.xticks(rotation=45)
    plt.title('Top 20 parole presenti in più canzoni (senza stopword)')
    plt.tight_layout()
    plt.show()
else:
    print("Nessuna parola significativa trovata per l’istogramma.")

# Word Cloud: tutte le parole presenti in almeno una canzone
if presenza_counter:
    wordcloud = WordCloud(width=1000, height=600, background_color='white', colormap='viridis')
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud.generate_from_frequencies(presenza_counter), interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud - Parole presenti in più canzoni (senza stopword)')
    plt.show()
else:
    print("Nessuna parola significativa trovata per la word cloud.")