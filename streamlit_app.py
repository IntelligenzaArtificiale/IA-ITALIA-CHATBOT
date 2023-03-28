
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
messages = []

# aggiunge il messaggio in chat
def add_message(content, sender):
    messages.append((content, sender))

# mostra tutti i messaggi
def show_messages():
    for message in messages:
        content, sender = message
        if sender == 'bot':
            st.write(f'<div class="message bot">{content}</div>', unsafe_allow_html=True)
        else:
            st.write(f'<div class="message user">{content}</div>', unsafe_allow_html=True)


prompt = st.text_input("🤔 Puoi chiedergli qualunque cosa...", "Puoi spiegarmi in modo semplice cosa è l'Intelligenza Artificiale ?")

if st.button("Chiedi 🚀"):
  add_message(prompt, 'user')
  show_messages()
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
    
    
    add_message(result, 'bot')
    
    textarea = driver.find_element(By.CLASS_NAME, "model-input-text-input")
    textarea.clear()
    
    show_messages()
