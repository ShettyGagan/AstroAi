
import streamlit as st
from datetime import datetime
import os

from astro import calculate_chart_data
from visuals import draw_natal_chart
from llm_chain import AstroChain
from utils import get_geolocation


# PAGE CONFIGURATION
st.set_page_config(
    page_title="AstroGuru",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

st.title("✨ AstroGuru ✨")
st.caption("Your Personal AI Astrologer based on Vedic (Sidereal) Principles")

if "chart_generated" not in st.session_state:
    st.session_state.chart_generated = False
    
if "chart_data" not in st.session_state:
    st.session_state.chart_data = None
if "aspects" not in st.session_state:
    st.session_state.aspects = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chain" not in st.session_state:
    st.session_state.chain = None



# If a chart has NOT been generated, display the input form.
if not st.session_state.chart_generated:
    st.header("🌟 Enter Your Birth Details")
    
    with st.form("details_form"):
        # Use columns for a cleaner layout in the main area
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name", "Adi")
            dob = st.date_input("Date of Birth", datetime(2000, 8, 18))
        with col2:
            tob = st.time_input("Time of Birth", datetime(1, 1, 1, 14, 30).time())
            pob = st.text_input("Place of Birth (e.g., 'Mangaluru, India')", "Mangaluru, India")

        initial_question = st.text_area(
            "Your initial question for the cosmos",
            "Give me a holistic overview of my personality, highlighting my key strengths and potential challenges based on my chart."
        )
        
        submit_button = st.form_submit_button("🔮 Generate My Cosmic Blueprint")

    if submit_button:
        with st.spinner("Aligning the cosmos... This may take a moment."):
            geo = get_geolocation(pob)
            if geo["status"] == "error":
                st.error(geo["message"])
            else:
                result = calculate_chart_data(
                    dob, tob, geo["latitude"], geo["longitude"], geo["timezone_id"]
                )
                if result["status"] == "error":
                    st.error(result["message"])
                else:
                    # Store results in session state
                    st.session_state.chart_data = result["data"]
                    st.session_state.aspects = result["aspects"]
                    
                    # Initialize the AI chain with the new data
                    st.session_state.chain = AstroChain(
                        chart_data=result["data"], 
                        aspects=result["aspects"]
                    )
                    
                    # Generate the initial AI response
                    response = st.session_state.chain.predict(initial_question)
                    st.session_state.messages.append({"role": "user", "content": initial_question})
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Set the flag to True to switch views
                    st.session_state.chart_generated = True
                    st.rerun() # Rerun the script to display the results view

# If a chart HAS been generated, display the results in tabs.
else:
    # result tabs
    tab1, tab2 = st.tabs(["**🔮 AI Astrologer Chat**", "**📊 Visual Chart**"])

    with tab1:
        st.subheader("Chat with AstroGuide AI")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("Ask a follow-up question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Interpreting the stars..."):
                    response = st.session_state.chain.predict(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

    with tab2:
        st.subheader("Your Sidereal Natal Chart (Lahiri)")
        try:
            fig = draw_natal_chart(st.session_state.chart_data, st.session_state.aspects)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not draw the chart. Error: {e}")

    
    # Reset button
    st.markdown("---")
    if st.button("🔁 Start a New Chart"):
        # Clear all session state variables to reset the app
        st.session_state.chart_generated = False
        st.session_state.chart_data = None
        st.session_state.aspects = None
        st.session_state.messages = []
        st.session_state.chain = None
        st.rerun()