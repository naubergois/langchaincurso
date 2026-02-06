import streamlit as st
import os
from agents import app_graph
from models import AuditState

st.set_page_config(page_title="Audit Agent AI", page_icon="🕵️‍♂️", layout="wide")

st.title("🕵️‍♂️ AI Agent Audit Assistant")
st.markdown("Automate your audit workflow: Draft, Analyze Risks, Plan, and Report.")

# --- Sidebar: Configuration ---
with st.sidebar:
    st.header("Configuration")
    
    # API Keys Management
    api_key = st.text_input("Gemini API Key", type="password", help="Needed if not set in .env")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        
    st.divider()
    
    st.subheader("Telegram Notifications")
    telegram_token = st.text_input("Bot Token", type="password")
    telegram_chat_id = st.text_input("Chat ID")
    
    # Store in streamlit secrets session state wrapper if needed, 
    # but for simplicity we modify os.environ or rely on st.secrets if file exists.
    # The agents.py tries to read from st.secrets. Let's mock it if user inputs here.
    if telegram_token and telegram_chat_id:
        if "secrets" not in st.session_state:
             st.session_state.secrets = {}
        # Hack: Streamlit secrets are read-only. We might need to patch the tool or use env vars.
        # Let's use env vars as fallback in agents.py if we updated it, but agents.py imported st.secrets.
        # Ideally, we should update agents.py to check env vars too.
        # For now, let's assume user sets them here and we patch os.environ, 
        # and we will update agents.py to look at os.environ as fallback.
        os.environ["TELEGRAM_TOKEN"] = telegram_token
        os.environ["TELEGRAM_CHAT_ID"] = telegram_chat_id

# --- Main Interface ---

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Audit Case Input")
    case_input = st.text_area(
        "Describe the audit finding or scenario:",
        height=300,
        placeholder="Example: During the review of procurement contracts for the IT department, we observed that 3 contracts were awarded to 'TechSolutions Inc.' without a competitive bidding process. The total value is $150,000. The justification provided was 'emergency', but no documentation supports this claim."
    )
    
    start_btn = st.button("🚀 Start Audit Workflow", type="primary")

if start_btn and case_input:
    with col2:
        st.subheader("⚙️ Workflow Execution")
        status_container = st.container()
        
        with st.status("Running AI Agents...", expanded=True) as status:
            try:
                # Initialize State
                initial_state = AuditState(case_input=case_input)
                
                # Stream the graph execution
                final_state = None
                for output in app_graph.stream(initial_state):
                    for key, value in output.items():
                        st.write(f"✅ **{key.capitalize()} Agent** finished.")
                        if key == "drafting":
                            st.info(f"Found {len(value.get('findings', []))} findings.")
                        elif key == "risk":
                            st.warning(f"Risk assessment complete.")
                        elif key == "notification":
                            if value.get("telegram_sent"):
                                st.success("Telegram notification sent!")
                            else:
                                st.error("Telegram notification failed (check credentials).")
                
                status.update(label="Workflow Complete!", state="complete", expanded=False)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                status.update(label="Workflow Failed", state="error")
                st.stop()

        # Display Results (Outside Status Expander)
        st.divider()
        st.subheader("📊 Final Report")
        
        try:
            # Run invoke to get final complete state
            final_result = app_graph.invoke(initial_state)
            
            tab1, tab2, tab3 = st.tabs(["📄 Executive Report", "🔍 Findings Details", "📉 Risk Analysis"])
            
            with tab1:
                st.markdown(final_result.get("final_report"))
                
            with tab2:
                findings = final_result.get("findings", [])
                for f in findings:
                    with st.expander(f.title):
                        st.write(f"**Description:** {f.description}")
                        st.write(f"**Evidence:** {f.evidence}")
                        
            with tab3:
                risks = final_result.get("risks", [])
                for r in risks:
                     st.write(f"**{r.finding_title}**")
                     st.progress(r.risk_score / 10.0)
                     st.caption(f"Risk Level: {r.risk_level} | Anomaly Score context: {r.anomaly_score:.2f}")
                     st.write(f"Justification: {r.justification}")
                     st.divider()
        except Exception as e:
             st.error(f"Error displaying results: {e}")
