import streamlit as st
import google.generativeai as genai

# 1. Page Setup
st.set_page_config(page_title="AI Workflow Builder", layout="centered")
st.title("⚡ AI Content Workflow")

# 2. Configure Gemini (Securely)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Using 1.5 Flash as it is stable; swap to "gemini-2.0-flash-exp" if you have access
    model = genai.GenerativeModel("gemini-1.5-flash") 
except Exception as e:
    st.error("API Key missing. Please check .streamlit/secrets.toml")
    st.stop()

# 3. Initialize Session State (The "Memory" of the workflow)
if "step" not in st.session_state:
    st.session_state.step = 1
if "draft_content" not in st.session_state:
    st.session_state.draft_content = ""

# --- STEP 1: INPUT ---
if st.session_state.step == 1:
    st.header("Step 1: Define Topic")
    topic = st.text_input("What should I write about?", placeholder="e.g. The future of Robotics")
    
    if st.button("Generate Draft 🚀"):
        if not topic:
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("AI is thinking..."):
                response = model.generate_content(f"Write a short, engaging LinkedIn post about: {topic}")
                st.session_state.draft_content = response.text
                st.session_state.step = 2
                st.rerun()

# --- STEP 2: REVIEW & EDIT ---
elif st.session_state.step == 2:
    st.header("Step 2: Review & Edit")
    
    # Allow user to edit the AI's output
    edited_text = st.text_area("Edit the draft below:", value=st.session_state.draft_content, height=250)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Approve & Finish ✅"):
            st.session_state.final_content = edited_text
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: FINAL OUTPUT ---
elif st.session_state.step == 3:
    st.header("🎉 Workflow Complete!")
    st.success("Your content is ready:")
    
    st.info(st.session_state.final_content)
    
    if st.button("Start New Workflow 🔄"):
        st.session_state.step = 1
        st.session_state.draft_content = ""
        st.rerun()