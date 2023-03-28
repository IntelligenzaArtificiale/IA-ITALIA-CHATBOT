
import streamlit as st
st.set_page_config(
    page_title="🧠🤖🇮🇹 - Beta ChatBOT Intelligenza Artificiale Italia",
    page_icon=":robot:",
    layout="wide"
)

st.markdown('<style> \
    .css-1x8cf1d { \
    display: inline-flex; \
    -webkit-box-align: center; \
    align-items: center; \
    -webkit-box-pack: center; \
    justify-content: center; \
    font-weight: 400; \
    padding: 0.25rem 0.75rem; \
    border-radius: 0.25rem; \
    margin: 0px; \
    line-height: 1.6; \
    color: inherit; \
    width: 100%; \
    height: 100%; \
    user-select: none; \
    background-color: rgb(255, 255, 255); \
    border: 1px solid rgba(49, 51, 63, 0.2); \
    } \
    .css-12w0qpk {\
    transform: translateY(45%); \
    } <style>', unsafe_allow_html=True)


"""
### Il chatBOT di [Intelligenza Artificiale Italia](https://www.intelligenzaartificialeitalia.net/)🧠🤖🇮🇹 
"""


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from streamlit_chat_media import message
from craiyon import Craiyon
import translators.server as tts
import base64
import time 



@st.cache_resource(show_spinner=False)
def get_driver():
  with st.spinner(" 💡 Il nostro chatBOT sta caricando, potrebbe volerci qualche secondo ⏳"):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')      
    options.add_argument('--disable-dev-shm-usage')    
    options.add_argument("--disable-features=NetworkService")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-features=VizDisplayCompositor")    
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
    st.session_state['bot'].append('Ciao, sono il chatBOT di Intelligenza Artificiale Italia 🧠🤖🇮🇹, puoi chiedermi qualunque cosa riguardo l\'Intelligenza Artificiale, ti risponderò il prima possibile 🚀 \n\n🧑‍🎨 Usa /img davanti al tuo messaggio per chiedermi di creare 9 immagini a tema, ad esempio: \n\n * /img un cane che corre \n\n🤖 Buon divertimento!')


# aggiunge il messaggio in chat
def add_message(content, sender):
  if sender == 'bot':
      st.session_state['bot'].append(content)
  else:
      st.session_state['user'].append(content)
      
          
def show_messages_alto():
    # stampa i messaggi in modo che il più nuovo sia sempre in alto
    # inoltre il bot può inviare più messaggi di risposta per ogni messaggio dell'utente
    i = len(st.session_state['bot']) - 1
    l = len(st.session_state['user']) - 1
    if i == 0:
        message(st.session_state['bot'][i], key=str(i), allow_html=True)
    else:
        while i > 0:
            message(st.session_state['bot'][i], key=str(i), allow_html=True)
            message(st.session_state['user'][i-1], is_user=True, key=str(i) + '_user')
            i -= 1
    


def Generate(request):
	try:
		generator = Craiyon()
		result = generator.generate(request) 
		return result.images
	except:
		return "Error"

st.write("")

col1, col2 = st.columns([3, 1])
prompt = col1.text_input("🤔 Puoi chiedergli qualunque cosa...")

if col2.button("Chiedi 🚀") and prompt != "" and driver.page_source != "":
# se il prompt inizia con /img 
    if prompt.startswith("/img"):
        with st.spinner(" 💡 Il nostro chatBOT sta creando 9 immagini, potrebbe volerci qualche secondo ⏳"):
    
            prompt = prompt[4:]
            new_request = tts.google(prompt, from_language="it", to_language="en")
            image_files = Generate(new_request)
            if image_files != "Error":
                html_message_image = 'Queste sono le immagini che ti ho generato 🤖📸: \n\n'
                for i in image_files:
                    html_image = f'* Immagine 1\n<img src="{i}" style="max-width: 200px;  flex-basis: 33.33%; border-radius: 10px; margin: 5px; height: auto; "/>'
                    html_message_image += html_image
                add_message(prompt, 'user')
                add_message(html_message_image, 'bot')
                
            else:
                add_message("🤖 Ops, qualcosa è andato storto, riprova più tardi", 'bot')
             
    else: 
        with st.spinner(" 💡 Il nostro chatBOT sta scrivendo, potrebbe volerci qualche secondo ⏳"):
            try:
                textarea = driver.find_element(By.CLASS_NAME, "model-input-text-input")
                textarea.send_keys(prompt)
                time.sleep(0.05)
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
                time.sleep(0.05)
                
            except Exception as e:
                
                print(e)
                textarea = driver.find_element(By.CLASS_NAME, "model-input-text-input")
                textarea.clear()
                add_message(prompt, 'user')
                add_message("Riprova a farmi la domanda", 'bot')
            
print(st.session_state['bot'])
show_messages_alto()

