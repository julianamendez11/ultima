import streamlit as st
from openai import OpenAI
from PIL import Image

# CSS for background image and container styles
st.markdown(
    """
    <style>
    .image-container {
        display: flex;
        flex-direction: row;
        position: absolute;
        top: 0px;
        right: 20px;
    }
    .image-container img {
        margin-right: 10px;
    }
    /* Background image for the entire page */
    .stApp {
        background-image: URL('https://raw.githubusercontent.com/julianamendez11/chatbot2/main/montañas.png');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image("logo.png", use_column_width=False, width=250)
    st.markdown('</div>', unsafe_allow_html=True)

# Show title and description.
st.title("CuesTalent")
st.write(
    "This is a Cuesta chatbot that uses OpenAI's GPT-4o model to generate responses based on internal data."
)

# Retrieve the OpenAI API key from Streamlit secrets.
openai_api_key = st.secrets["api_key"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What do you want to know about Cuesta Skills, Methodologies, Industry/Function Expertise?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": "In base of this information: Eduardo Mateus has the following Skills: Data Pipeline - Databricks, Data Pipeline - Keboola, Data Pipeline - Microsoft, Data Warehouse - Snowflake, Data Warehouse - Databricks, Data Viz - PowerBI. Simón Lopera has the following Skills: Data Viz - PowerBi, Data Viz - Tableau. Simón Vallejo has the following Skills: Data Viz - PowerBi, Data Viz - Tableau, Data Pipeline - Keboola. Sebastián Oliveros González has the following Skills: Data Viz - PowerBi, Data Viz - Looker. Jasmine Heung has the following Skills: Data Viz - PowerBi, Data Viz - Tableau, Data Viz - Looker, Data Warrehouse - Microsoft, Data Pipeline - Keboola, Data Warehouse - Snowflake. Answer the following question" + prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
