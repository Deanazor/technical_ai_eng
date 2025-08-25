import time
import uuid

import streamlit as st

from frontend.backend_client import send_message, upload_file

if "messages" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid1())
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's start chatting! 👇"}
    ]

upload_form = st.sidebar.form("upload_form")
store_name = upload_form.text_input("Store Name")
transaction_date = upload_form.date_input("Transaction Date")
uploaded_file = upload_form.file_uploader("Receipt Image", type=["jpg", "jpeg", "png"])
is_submitted = upload_form.form_submit_button("Upload Receipt")

if is_submitted:
    transaction_date = transaction_date.strftime("%Y-%m-%d")
    response = upload_file(
        uploaded_file.read(),
        metadata={
            "store_name": store_name,
            "transaction_date": transaction_date,
        },
    )
    if response == "success":
        sucess = st.sidebar.success("Receipt uploaded successfully")
        time.sleep(2)
        sucess.empty()
    else:
        error = st.sidebar.error("Failed to upload receipt")
        time.sleep(2)
        error.empty()
    is_submitted = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = send_message(prompt, st.session_state.session_id)
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
