import streamlit as st
import os
import pandas as pd
import base64
import time

from main import get_pixtral_response, get_deepseek_response,pixtral_response_dir,deepseek_response_dir
from util import write_response, note_token_usage, push_into_csv

st.title('FINANCIAL DOCUMENTS PARSING')

uploaded_file = st.file_uploader("Upload an image",type=['jpg','jpeg','png'])
if uploaded_file:
    # Save uploaded image temporarily
    temp_image_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(temp_image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.button("Process"):
        with st.spinner("Processing..."):
            try:
                image_name = uploaded_file.name.split('.')[0]
                token_usage, pixtral_response = get_pixtral_response(temp_image_path)
                deepseek_response = get_deepseek_response(pixtral_response)

                # Save responses
                write_response(pixtral_response_dir, deepseek_response_dir, pixtral_response, deepseek_response, image_name)
                note_token_usage(image_name, str(dict(token_usage)))
                push_into_csv(deepseek_response,image_name)

                st.success("Processing Complete!")
                # st.write("Pixtral Response:")
                # st.write(pixtral_response)
                # st.write("DeepSeek Response:")
                # st.write(deepseek_response)

                # Display and automatically download personal_info.csv
                if os.path.exists(f"personal_info_{image_name}.csv"):
                    # st.write("### Personal Info")
                    # personal_df = pd.read_csv("personal_info.csv")
                    # st.dataframe(personal_df)

                    with open(f"personal_info_{image_name}.csv", "rb") as f:
                        csv = f.read()
                        b64 = base64.b64encode(csv).decode()
                        href = f'<a href="data:file/csv;base64,{b64}" download="personal_info.csv">Download Personal Info CSV</a>'
                        st.markdown(href, unsafe_allow_html=True)

                # Add delay to ensure file creation before reading
                time.sleep(1)

                # Display and automatically download transactions.csv
                if os.path.exists(f"transactions_{image_name}.csv"):
                    # st.write("### Transactions")
                    # transactions_df = pd.read_csv("transactions.csv")
                    # st.dataframe(transactions_df)

                    with open(f"transactions_{image_name}.csv", "rb") as f:
                        csv = f.read()
                        b64 = base64.b64encode(csv).decode()
                        href = f'<a href="data:file/csv;base64,{b64}" download="transactions.csv">Download Transactions CSV</a>'
                        st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")