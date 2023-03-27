
import streamlit as st

"""
## Web scraping on Streamlit Cloud with Selenium
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@st.experimental_singleton
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')

driver = get_driver()

# open https://deepai.org/machine-learning-model/text-generator
# find textarea with class "model-input-text-input"
# send prompt variable to textarea
# click button with id = "modelSubmitButton"
# read all text int div with class "try-it-result-area"

prompt = st.text_input("Prompt", "The quick brown fox jumps over the lazy dog.")
if st.button("Generate"):
  with st.spinner("Generating..."):
    driver.get("https://deepai.org/machine-learning-model/text-generator")
    st.code(driver.page_source)

    textarea = driver.find_element("class", "model-input-text-input")
    textarea.send_keys(prompt)
    button = driver.find_element("id", "modelSubmitButton")
    button.click()
    # wait for result
    #ogni 3 secondi controlla se il risultato è pronto
    reuslt = ""
    while result == "":
        result = driver.find_element("class", "try-it-result-area").text
        time.sleep(3)
    st.code(result)
  
