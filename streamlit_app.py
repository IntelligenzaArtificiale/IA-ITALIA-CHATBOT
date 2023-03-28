import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

st.set_page_config(layout="wide")

# Funzione per ottenere uno user agent casuale
def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

# Funzione per ottenere il driver di Chrome
@st.cache(allow_output_mutation=True)
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')      
    options.add_argument('--disable-dev-shm-usage')        
    options.add_argument(f'user-agent={get_random_user_agent()}')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get('https://deepai.org/machine-learning-model/text-generator')
    return driver

# Inizializza il driver
driver = get_driver()

# Storico dei messaggi
messages = [{'sender': 'bot', 'text': 'Benvenuti nella nostra chat! Siamo il chatbot di IntelligenzaArtificialeItalia.net e siamo qui per aiutarti a rispondere a qualsiasi domanda riguardante l\'Intelligenza Artificiale. Scrivi qui di seguito la tua domanda e premi il pulsante "Invia" per ottenere una risposta.'}]

# Funzione per aggiungere un messaggio al chat
def add_message(text, sender='bot'):
    messages.append({'sender': sender, 'text': text})

# Funzione per visualizzare la chat
def show_chat():
    for message in messages:
        if message['sender'] == 'bot':
            st.markdown(f'<div style="text-align:right">{message["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:left">{message["text"]}</div>', unsafe_allow_html=True)

# Funzione per ottenere la risposta dal chatbot
def get_chatbot_response(prompt):
    textarea = driver.find_element(By.CLASS_NAME, 'model-input-text-input')
    textarea.send_keys(prompt)
    button = driver.find_element(By.ID, 'modelSubmitButton')
    button.click()
    result = ''
    while not result:
        result = driver.find_element(By.CLASS_NAME, 'model-output-text-output').text
    return result

# Interfaccia grafica
st.title('ChatBot di Intelligenza Artificiale Italia 🧠🤖🇮🇹')
st.markdown('Scrivi qui di seguito la tua domanda e premi il pulsante "Invia" per ottenere una risposta.')
chat_col, user_col = st.beta_columns(2)
prompt = user_col.text_input('Scrivi qui', key='prompt')
if user_col.button('Invia'):
    with st.spinner('💡 Il nostro chatBOT sta elaborando la miglior risposta per te, potrebbe volerci qualche secondo ⏳'):
        result = get_chatbot_response(prompt)
        add_message(result, 'bot')
        show_chat()
        st.balloons()  # effetto wow!

# Chiudi il driver di Chrome 
driver.quit()
