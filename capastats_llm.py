import os
import re
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType

# 1. Carica e pulisci i file .lrc
def load_lrc_lyrics(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".lrc"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                # Rimuove i timestamp tipo [00:12.34]
                cleaned_lyrics = re.sub(r'\[\d{1,2}:\d{2}(?:\.\d{2})?\]', '', content)
                cleaned_lyrics = cleaned_lyrics.strip()
                if cleaned_lyrics:
                    docs.append(Document(page_content=cleaned_lyrics, metadata={"source": filename}))
    return docs

# Specifica la tua cartella con i file .lrc
lyrics_folder = "./lyrics"
documents = load_lrc_lyrics(lyrics_folder)

# 2. Suddividi in blocchi gestibili
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(documents)

# 3. Embedding
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(split_docs, embeddings)

# 4. Creazione del retriever
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
llm_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.7)

# 5. Retrieval-based QA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm_model, retriever=retriever)

# 6. Definizione dello strumento dell’agente
lyrics_tool = Tool(
    name="LyricsMemory",
    func=qa_chain.run,
    description="Usa questo strumento per capire i testi del cantante e il suo stile di scrittura, include le figure retoriche"
)

# 7. Inizializza l’agente
agent = initialize_agent(
    tools=[lyrics_tool],
    llm=llm_model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 8. Esempi di utilizzo
print(agent.run("Quali sono i temi più ricorrenti nei testi del cantante?"))
print(agent.run("Scrivi una nuova strofa sul tema della noia nello stile del cantante."))
print(agent.run("Quali sono le parole più utilizzate dal cantante?"))
