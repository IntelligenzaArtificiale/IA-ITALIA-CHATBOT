
import streamlit as st
st.set_page_config(
    page_title="🧠🤖🇮🇹 - Beta ChatBOT Intelligenza Artificiale Italia",
    page_icon=":robot:",
    layout="wide"
)

"""
### Il chatBOT di [Intelligenza Artificiale Italia](https://www.intelligenzaartificialeitalia.net/)🧠🤖🇮🇹 


"""


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from streamlit_chat import message
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
    prompt = st.text_input("🤔 Puoi chiedergli qualunque cosa...", "Puoi spiegarmi in modo semplice cosa è l'Intelligenza Artificiale ?")
else:
    prompt = st.text_input("🤔 Puoi chiedergli qualunque cosa...")

if 'bot' not in st.session_state:
    st.session_state['bot'] = []
    # mostra il messaggio di benvenuto
    st.session_state['bot'].append('Ciao, sono il chatBOT di Intelligenza Artificiale Italia 🧠🤖🇮🇹, puoi chiedermi qualunque cosa riguardo l\'Intelligenza Artificiale, ti risponderò il prima possibile 🚀')


# aggiunge il messaggio in chat
def add_message(content, sender):
    if sender == 'bot':
        st.session_state['bot'].append(content)
    else:
        st.session_state['user'].append(content)


# mostra tutti i messaggi
def show_messages():
    # mostra i messaggi come una chat, considerando che il bot da il messaggio di benvenuto
    # e quindi il primo messaggio è sempre del bot
    #pero controlla sempre che non ci sia un index out of range
    for i in range(len(st.session_state['bot'])):
        if i == 0:
            message(st.session_state['bot'][i], key=str(i))
        else:
            message(st.session_state['bot'][i], key=str(i))
            message(st.session_state['user'][i-1], is_user=True, key=str(i) + '_user')
      



if st.button("Chiedi 🚀"):
  #with st.spinner(" 💡 Il nostro chatBOT sta elaborando la miglior risposta per te, potrebbe volerci qualche secondo ⏳"):
  textarea = driver.find_element(By.CLASS_NAME, "model-input-text-input")
  textarea.send_keys(prompt)
  
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
    

print(st.session_state['bot'])
show_messages()

