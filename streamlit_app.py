
import streamlit as st
st.set_page_config(layout="wide")

"""
### Il chatBOT di [Intelligenza Artificiale Italia](https://www.intelligenzaartificialeitalia.net/)🧠🤖🇮🇹 


"""

# definisce il layout dei messaggi
CSS = """
    .message {
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        max-width: 60%;
    }
    .bot {
        background-color: #E8F5E9;
        align-self: flex-start;
    }
    .user {
        background-color: #FFF;
        align-self: flex-end;
    }
"""

# crea lo stile
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time 



@st.cache_resource
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')      
    options.add_argument('--disable-dev-shm-usage')        
    options.add_argument("'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get('https://deepai.org/machine-learning-model/text-generator')
    return driver

driver = get_driver()

# crea lo stack di messaggi
if 'user' not in st.session_state:
    st.session_state['user'] = []

if 'bot' not in st.session_state:
    st.session_state['bot'] = []
    # mostra il messaggio di benvenuto
    add_message("Ciao, sono il chatBOT di Intelligenza Artificiale Italia 🤖🇮🇹", 'bot')

# aggiunge il messaggio in chat
def add_message(content, sender):
    if sender == 'bot':
        st.session_state['bot'].append(content)
    else:
        st.session_state['user'].append(content)

# mostra tutti i messaggi
def show_messages():
    # mostra un messaggio in stile chat
    for user, bot in zip(st.session_state['user'], st.session_state['bot']):
        st.markdown(f'<p class="message user">{user}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="message bot">{bot}</p>', unsafe_allow_html=True)




prompt = st.text_input("🤔 Puoi chiedergli qualunque cosa...", "Puoi spiegarmi in modo semplice cosa è l'Intelligenza Artificiale ?")

if st.button("Chiedi 🚀"):
  with st.spinner(" 💡 Il nostro chatBOT sta elaborando la miglior risposta per te, potrebbe volerci qualche secondo ⏳"):
    textarea = driver.find_element(By.CLASS_NAME, "model-input-text-input")
    textarea.send_keys(prompt)
    print(textarea.text)
    
    button = driver.find_element(By.ID, "modelSubmitButton")
    button.click()

    result = ""
    while result == "":
      result = driver.find_element(By.CLASS_NAME, "try-it-result-area").text
      time.sleep(0.05)
    
    add_message(prompt, 'user')
    add_message(result, 'bot')
    
    textarea = driver.find_element(By.CLASS_NAME, "model-input-text-input")
    textarea.clear()
    
    show_messages()
