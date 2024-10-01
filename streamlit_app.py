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
    "This is a Cuesta chatbot that uses OpenAI's GPT-4 model to generate responses based on internal skills data from the Data Team."
)

# Retrieve the OpenAI API key from Streamlit secrets.
openai_api_key = st.secrets["api_key"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Context information (invisible to the user)
context = """
The following information is about the skills of the Cuesta Data Team. Each skill its corresponding level (from 1 to 5 being 5 very good and 1 bad):
Eduardo Mateus (Senior Data Engineer role) has the following Skills: Data Pipeline - Databricks - 5, Data Pipeline - Keboola - 3, Data Pipeline - Microsoft - 5, Data Warehouse - Snowflake - 3, Data Warehouse - Databricks - 5, Data Viz - PowerBI -5.
Simón Lopera (Associate Consultant role) has the following Skills: Data Viz - PowerBi - 4, Data Viz - Tableau -4.
Simón Vallejo (Data VIsualization Engineer role) has the following Skills: Data Viz - PowerBi - 5, Data Viz - Tableau - 5, Data Pipeline - Keboola - 2.
Sebastián Oliveros González (Data VIsualization Engineer role) has the following Skills: Data Viz - PowerBi - 4, Data Viz - Looker - 3.
Jasmine Heung (Senior Associate role) has the following Skills: Data Viz - PowerBi - 1, Data Viz - Tableau - 3, Data Viz - Looker - 3, Data Warehouse - Microsoft - 2, Data Pipeline - Keboola - 2, Data Warehouse - Snowflake - 4.
Andrés Jaramillo (Data Engineer role) has the following skills: Data Pipeline - Databricks - 3, Data Warehouse - Databricks - 3.
David Jaramillo (Associate Consultant role) has the following skills: Data Pipeline - Google - 5, Data Pipeline - Keboola - 4, Data Viz - PwerBi - 4, Data Warehouse - Google - 4, Data Warehouse - Snowflake - 4.
Estefany Aguilar (Data Engineer role) has the following skills: Data Pipeline - Keboola - 3, Data Warhouse - Snowflake - 3.
Filip Kawka (Senior Associate role) has the following skills: Data Viz - Looker - 3, Data Warehouse - Snowflake - 3.
Holt Zeidler (Principal role) has the following skills: Data Pipeline - Keboola - 1, Data Viz - Tableau - 1.
Jack Lewis (Associate role) has the following skills: Data Pipeline - Keboola - 1, Data Viz - PowerBi - 3, Data Viz - Tableau - 3.
Marcus Wong (Manager role) has the following skills: Data Pipeline - Keboola - 1.

"""

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message.
if prompt := st.chat_input("What do you want to know about Cuesta Skills, Methodologies, Industry/Function Expertise?"):

    # Store the current user prompt (without the context) and display it.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Combine the context with the user messages for OpenAI API call
    messages_with_context = [{"role": "system", "content": context}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_with_context,
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
