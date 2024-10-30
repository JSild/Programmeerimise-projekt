import streamlit as st
from scrape_koostisosad import (
    scrape_website, 
    split_dom_content, 
    clean_body_content, 
    exctract_body_content
)
from parse import parse_with_ollama

st.title('Retseptid AI')
url = st.text_input('Sisesta blogi ')

if st.button('Leia retseptid'):
    st.write('Otsin...')

    result = scrape_website(url)
    body_content = exctract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander('View DOM content'):
        st.text_area('DOM content', cleaned_content, height=300)

if 'dom_content' in st.session_state:
    parse_description = st.text_area('Mida soovid parsida?')

    if st.button('Parse'):
        if parse_description:
            st.write('Parsing the content')

            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)