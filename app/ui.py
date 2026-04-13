import streamlit as st
from main import app  # This imports the compiled LangGraph 'app' from your main.py

# 1. Page Configuration
st.set_page_config(page_title="AI PR-Bot | Strike Team", page_icon="🛡️", layout="wide")

# 2. Sidebar for Info
with st.sidebar:
    st.title("System Status")
    st.success("Cloud Server: Connected")
    st.success("AWS Bedrock: Active (Llama 3.1)")
    st.divider()
    st.info("This system uses a Multi-Agent loop to refine PR responses until they meet a quality threshold.")

# 3. Main Interface
st.title("🛡️ AI PR-Bot: Crisis Simulator")
st.markdown("### Rapid Response Agentic Workflow")

# Input Section
crisis_desc = st.text_area(
    "Enter the Crisis Scenario:", 
    placeholder="e.g., A software update caused global banking systems to go offline...",
    height=100
)

if st.button("Deploy Strike Team", type="primary"):
    if not crisis_desc:
        st.warning("Please describe a crisis first.")
    else:
        # Initialize the state for LangGraph
        inputs = {"crisis_description": crisis_desc, "history": [], "critique_score": 0}
        
        container = st.container()
        
        with st.spinner("Agents are coordinating..."):
            # Stream the graph execution
            for output in app.stream(inputs):
                for key, value in output.items():
                    if key == "aggressor":
                        with container.chat_message("user", avatar="😈"):
                            st.write("**Aggressor (Angry Public):**")
                            st.write(value["current_attack"])
                    
                    elif key == "strategist":
                        with container.chat_message("assistant", avatar="🛡️"):
                            st.write("**Strategist (PR Response):**")
                            st.write(value["current_response"])
                    
                    elif key == "monitor":
                        score = value["critique_score"]
                        color = "green" if score >= 8 else "orange"
                        st.markdown(f"**Monitor Score:** :{color}[{score}/10]")
            
            st.balloons()
            st.success("Final Response Approved by Monitor.")