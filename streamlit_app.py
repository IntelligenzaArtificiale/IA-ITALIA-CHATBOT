
import streamlit as st
st.set_page_config(layout="wide")

"""
### Il chatBOT di [Intelligenza Artificiale Italia](https://www.intelligenzaartificialeitalia.net/)🧠🤖🇮🇹 


"""

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time 



@st.cache_resource
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--no-sandbox')      
options.add_argument('--disable-dev-shm-usage')        
options.add_argument("'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'")

driver = get_driver()

prompt = st.text_input("🤔 Puoi chiedergli qualunque cosa")

if st.button("Chiedi 🚀"):
  with st.spinner(" 💡 Il nostro chatBOT sta elaborando la miglior risposta per te, potrebbe volerci qualche secondo ⏳"):
    driver.get("https://deepai.org/machine-learning-model/text-generator")
    #print(driver.page_source)
    print("Inserimento : ")
    textarea = driver.find_element(By.CLASS_NAME, "model-input-text-input")
    textarea.send_keys(prompt)
    print(textarea.text)
    
    button = driver.find_element(By.ID, "modelSubmitButton")
    time.sleep(1)
    button.click()
    # wait for result
    #ogni 3 secondi controlla se il risultato è pronto
    result = ""
    while result == "":
        result = driver.find_element(By.CLASS_NAME, "try-it-result-area").text
        time.sleep(0.1)
    st.write(result)
  
