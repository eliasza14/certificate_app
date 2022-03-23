import streamlit as st
import streamlit_authenticator as stauth

import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe



def get_options():
    return {
        'encoding': 'UTF-8',
        'enable-local-file-access': True
    }


names = ['MARIA	TERZI','Στεριανή Αβράμη','ΔΕΣΠΟΙΝΑ ΑΒΡΑΜΙΔΟΥ','Μαρία Αγάθου']
usernames = ['Maria-terzi@hotmail.com','stella-a88@hotmail.com','depi1970@hotmail.com','magathou@hotmail.com']
passwords = ['tSYcA8GPCJ','hj2cJpZLXG','u46UXerHf9','pJH9CA7L2g']

hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(names,usernames,hashed_passwords,'some_cookie_name','some_signature_key',cookie_expiry_days=30)


name, authentication_status = authenticator.login('Login','main')

if authentication_status:
    
    st.write('Welcome *%s*' % (name))
    # st.title('Some content')
    # st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
    st.title("🎓 Diploma PDF Generator")

    st.write(
        "This app shows you how you can use Streamlit to make a PDF generator app in just a few lines of code!"
    )

    left, right = st.columns(2)

    right.write("Here's the template we'll be using:")

    right.image("template.png", width=300)

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")


    left.write("Fill in the data:")
   
    form = left.form("template_form")
    
    # student = form.text_input("Student name")
    student=name
    course="Report Generation in Streamlit"
    grade=60
    test="Test a"
    left.write(student)
    # course = form.selectbox(
    #     "Choose course",
    #     ["Report Generation in Streamlit", "Advanced Cryptography"],
    #     index=0,
    # )
    # grade = form.slider("Grade", 1, 100, 60)
    submit = form.form_submit_button("Generate PDF")
    st.write(student)
    if submit:
        html = template.render(
            student=student,
            course=course,
            grade=f"{grade}/100",
            date=date.today().strftime("%d %B, %Y"),
            test=test

        )
        st.write(html)
        

        config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        pdf=pdfkit.from_string(html, 'MyPDF.pdf', configuration=config,options=get_options())
        # pdf = pdfkit.from_string(html, False)
        st.balloons()

        right.success("🎉 Your diploma was generated!")
        # st.write(html, unsafe_allow_html=True)
        # st.write("")
        with open("MyPDF.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        
        st.download_button(
            label="⬇️ Download PDF",
            data=PDFbyte,
            file_name="MyPDF.pdf",
            mime="application/octet-stream",
        )





elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')


# if st.session_state['authentication_status']:
#     st.write('Welcome *%s*' % (st.session_state['name']))
#     st.title('Some content')
elif st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    st.warning('Please enter your username and password')