import streamlit as st
from streamlit_option_menu import option_menu
import database as db
from datetime import date
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

#---------------------------------------------------
# page config settings:

page_title="Personal Diary"
page_icon=":beginner:"
layout="centered"

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title(page_title+" "+page_icon)

#--------------------------------------------------
#hide the header and footer 

hide_ele="""
        <style>
        #Mainmenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
        """
st.markdown(hide_ele,unsafe_allow_html=True)
#---------------------------------------------------
cursignin=""
now=date.today()
def log_sign():
    selected=option_menu(
        menu_title=None,
        options=["Login","signup"],
        icons=["bi-box-arrow-in-right","bi-x-diamond-fill"],
        orientation="horizontal"
    )
    global submit
    if(selected=="Login"):
        with st.form("Login",clear_on_submit=True):
            st.header("Login")
            username=st.text_input("Username")
            password=st.text_input("Password",type="password")
            submit=st.form_submit_button()
            if(submit):
                if(username=="" or password==""):
                    st.warning("Enter your login credentials")
                else:
                    if(db.authenticate(username,password)):
                        st.session_state["curlogin"]=username
                        st.session_state["key"]="main"
                        st.experimental_rerun()
                    else:
                        st.error("Please check your username / password ")

    elif(selected=="signup"):
        with st.form("Sign Up",clear_on_submit=True):
            st.header("Sign Up")
            email=st.text_input("Enter your email")
            username=st.text_input("Enter your username")
            password=st.text_input("Enter your password",type="password")
            submit=st.form_submit_button()
            if(submit):
                dev=db.fetch_all_users()
                usernames=[]
                emails=[]
                for user in dev:
                    usernames.append(user["key"])
                    emails.append(user["email"])
                if(username in usernames):
                    st.error("Username already exists!\nTry another username !")
                elif(email in emails):
                    st.error("email already exists!\nTry with another email !")
                elif(len(password)<=6):
                    st.error("Password cannot be less than 6 characters")
                else:
                    db.insert_user(username,password,email)
                    st.success("Signed Up Successfully")

def main():
        selected=option_menu(
            menu_title=None,
            options=["Enter Data","View Past Entries","Delete an entry"],
            icons=["bi-box-arrow-in-right","bi-x-diamond-fill"],
            orientation="horizontal"
        )
        if(selected=="Enter Data"):
            with st.form("Enter Data",clear_on_submit=True):
                st.header("Enter Data")
                data=st.text_area("How did Your day go?",placeholder="Store your memories here :)")
                submit=st.form_submit_button()
                if(submit):                    
                    date=now.strftime("%d/%m/%Y")
                    db.entrydata(date,data,st.session_state["curlogin"])
                    st.success("Data Entry Successful")
        elif(selected=="View Past Entries"):
            import pandas as pd
            data=db.fetch_all_entries(st.session_state["curlogin"])
            if(bool(data)):
                data=db.fetch_all_entries(st.session_state["curlogin"])
                df = pd.DataFrame.from_dict(data)
                st.dataframe(df)
            else:
                st.warning("No Data to work on !!!")

        else:
            import pandas as pd
            data=db.fetch_all_entries(st.session_state["curlogin"])
            if(bool(data)):
                data=db.fetch_all_entries(st.session_state["curlogin"])
                df=pd.DataFrame.from_dict(data)
                st.dataframe(df) 
                dev=st.button("Clear Recent Entry")
                if(dev):
                    num=0
                    x=data[num]
                    if(len(db.fetch_all_entries(st.session_state["curlogin"]))>num):
                        db.deleteinfo(x["Key"])
            else:
                st.warning("No Data to work on !!!")

#--------------------------------------------------

if "key" not in st.session_state:
    st.session_state["key"] = "log_sign"

if st.session_state["key"] == "log_sign":
    log_sign()
elif st.session_state["key"] == "main":
    main()
