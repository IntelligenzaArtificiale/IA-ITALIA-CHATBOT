
import streamlit as st

"""
## Web scraping on Streamlit Cloud with Selenium
"""

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time 


@st.experimental_singleton
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')

driver = get_driver()

prompt = st.text_input("Prompt", "The quick brown fox jumps over the lazy dog.")

if st.button("Generate"):
  with st.spinner("Generating..."):
    driver.get("https://deepai.org/machine-learning-model/text-generator")
    print(driver.page_source)
    time.sleep(5)

    textarea = driver.find_element(By.CLASS_NAME, "model-input-text-input")
    textarea.send_keys(prompt)
    time.sleep(5)
    print(textarea.text)
    
    button = driver.find_element(By.ID, "modelSubmitButton")
    time.sleep(5)
    button.click()
    # wait for result
    #ogni 3 secondi controlla se il risultato è pronto
    time.sleep(5)
    reuslt = ""
    while result == "":
        result = driver.find_element(By.CLASS_NAME, "try-it-result-area").text
        time.sleep(3)
    st.write(result)
  
