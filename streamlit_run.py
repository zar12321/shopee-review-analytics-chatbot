import time
import streamlit as st

from langchain_core.messages import (
HumanMessage,
AIMessage
)

from config.llm import load_llm
from rag.embeddings import load_embedding_model
from rag.vectorstore import load_vectorstore
from rag.retriever import create_retriever

from agent.tools import create_tools
from agent.graph_builder import build_graph

# ==========================

# PAGE CONFIG

# ==========================

st.set_page_config(
page_title="Shopee Review Analysis Agent",
page_icon="🛍️",
layout="wide"
)

# ==========================

# CUSTOM CSS

# ==========================

st.markdown("""

<style>

.block-container{
    padding-top:2rem;
}

.big-title{
    text-align:center;
    font-size:3.5rem;
    font-weight:700;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:1.2rem;
    margin-bottom:2rem;
}

</style>

""", unsafe_allow_html=True)

# ==========================

# SESSION STATE

# ==========================

if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.messages = []

# ==========================

# SIDEBAR

# ==========================

with st.sidebar:


    st.image(
        "assets/shopee_logo.png",
        width=120
    )

    st.title(
        "Shopee Review Agent"
    )

    api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

    model_options = {
        "Gemini 2.5 Flash": "gemini-2.5-flash",
        "Gemini 2.5 Flash Lite": "gemini-2.5-flash-lite",
        "Gemini 2.5 Pro": "gemini-2.5-pro",
        "Gemini 2.0 Flash": "gemini-2.0-flash",
        "Gemini 2.0 Flash Lite": "gemini-2.0-flash-lite",
        "Gemini 1.5 Pro": "gemini-1.5-pro",
        "Gemini 1.5 Flash": "gemini-1.5-flash"
    }
    selected_model = st.selectbox(
        'Gemini Model', 
        options=list(model_options.keys()), 
        index=0 # default si gemini 2.5 flash yg tampil
    )
    model = model_options[selected_model]


    if st.button(
        "Connect"
    ):

        try:

            llm = load_llm(api_key, model)

            embedding_model = (
                load_embedding_model()
            )

            vectorstore = (
                load_vectorstore(
                    embedding_model
                )
            )

            retriever = (
                create_retriever(
                    vectorstore
                )
            )

            tools = create_tools(
                retriever,
                llm
            )

            app = build_graph(
                llm=llm,
                retrieve_reviews=tools["retrieve_reviews"],
                analyze_sentiment=tools["analyze_sentiment"],
                review_statistics=tools["review_statistics"]
            )

            st.session_state.app = app
            st.session_state.initialized = True

            st.success(
                "Connected successfully"
            )

        except Exception as e:
            st.error(str(e))
    

# ==========================

# WELCOME SCREEN

# ==========================

if len(
st.session_state.messages
) == 0:

    st.markdown(
        """
        <div class="big-title">
        👋 Hai, Selamat Datang
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        Saya adalah Shopee Review Analysis Agent.
        <br><br>
        Saya dapat membantu Anda menganalisis:
        <br>
        • Keluhan pengguna
        <br>
        • Sentimen review
        <br>
        • Distribusi rating
        <br>
        • Voucher, checkout, kurir, dan pengiriman
        <br><br>
        Silakan ajukan pertanyaan pada kolom di bawah.
        </div>
        """,
        unsafe_allow_html=True
    )
    

# ==========================

# DISPLAY CHAT HISTORY

# ==========================

for message in st.session_state.messages:


    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==========================

# CHAT INPUT

# ==========================

prompt = st.chat_input(
"Tanyakan sesuatu tentang review Shopee..."
)

if prompt:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.markdown(prompt)

    if not st.session_state.initialized:

        st.warning(
            "Masukkan API Key terlebih dahulu."
        )

    else:

        with st.chat_message(
            "assistant",
            avatar="🛍️"
        ):

            chat_history = []

            for msg in st.session_state.messages:

                if msg["role"] == "user":
                    chat_history.append(
                        HumanMessage(
                            content=msg["content"]
                        )
                    )

                else:
                    chat_history.append(
                        AIMessage(
                            content=msg["content"]
                        )
                    )

            result = (
                st.session_state.app.invoke(
                    {
                        "messages": chat_history
                    }
                )
            )

            answer = result[
                "final_answer"
            ]

            placeholder = st.empty()

            streamed_text = ""

            for char in answer:

                streamed_text += char

                placeholder.markdown(
                    streamed_text
                )

                time.sleep(
                    0.01
                )

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

