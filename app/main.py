import streamlit as st
from chains import Chain
from portfolio import Portfolio

st.title("📧 Cold Mail Generator")
url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
submit_button = st.button("Submit")

if submit_button:
    myObj = Chain()
    pf = Portfolio()

    j = myObj.extractJobs(str(url_input))



    k = pf.query_links(str(j))

    email = myObj.generateEmail(j,k)
    print(k)
    st.code(email, language='markdown')