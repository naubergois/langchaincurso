import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

from models import AuditState, AuditFinding, RiskAssessment, AuditPlan
from tools import run_pyod_anomaly_detection, send_telegram_message
from dotenv import load_dotenv

# Load environment variables from .env file (parent directory)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# --- LLM Setup ---
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)

# --- Nodes ---

def drafting_node(state: AuditState):
    """
    Agent 1: Draft findings from the raw case input.
    """
    print("--- Draft Node ---")
    case_input = state.case_input
    
    # Parser for structured output
    parser = PydanticOutputParser(pydantic_object=AuditFinding)
    
    # We want a list of findings, so we instruct the LLM to generate one by one or a list wrapper
    # For simplicity in this demo, let's ask for a single major finding or list them
    # Better approach: structured output of a wrapper model or just list handling.
    # Let's use with_structured_output if available, else prompting.
    
    # Using Gemini's structured output capability if possible:
    structured_llm = llm.with_structured_output(AuditFinding) 
    # Note: with_structured_output usually returns one object. 
    # To get multiple, we might need a wrapper or iterative calls. 
    # Let's define a wrapper for simplicity.
    
    class FindingsList(BaseModel):
        findings: List[AuditFinding]
        
    structured_llm_list = llm.with_structured_output(FindingsList)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Internal Auditor. Analyze the provided case text and extract potential audit findings."),
        ("human", "Case: {case}\n\nExtract the findings.")
    ])
    
    chain = prompt | structured_llm_list
    result = chain.invoke({"case": case_input})
    
    return {"findings": result.findings}

def risk_node(state: AuditState):
    """
    Agent 2: Assess risks using PyOD tool and LLM judgment.
    """
    print("--- Risk Node ---")
    findings = state.findings
    case_input = state.case_input
    
    # Calulate anomaly score for the whole case text as a signal
    anomaly_score = run_pyod_anomaly_detection.invoke(case_input)
    
    risks = []
    for finding in findings:
        # Ask LLM to assess risk, injecting the anomaly score as context
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Risk Assessment Expert. Evaluate the risk of the following audit finding."),
            ("human", f"""
            Finding: {finding.title}
            Description: {finding.description}
            
            Contextual Anomaly Score (from AI model): {anomaly_score:.4f} (High score > 10 indicates potential irregularity)
            
            Classify the risk (High/Medium/Low), give a score (0-10), and justify.
            """)
        ])
        
        structured_llm = llm.with_structured_output(RiskAssessment)
        chain = prompt | structured_llm
        assessment = chain.invoke({})
        
        # Ensure finding title matches (or just force it)
        assessment.finding_title = finding.title
        assessment.anomaly_score = anomaly_score # persist the score in the object
        risks.append(assessment)
        
    return {"risks": risks}

def planning_node(state: AuditState):
    """
    Agent 3: Prioritize and plan.
    """
    print("--- Planning Node ---")
    risks = state.risks
    
    # Sort risks by score for the prompt context
    sorted_risks = sorted(risks, key=lambda x: x.risk_score, reverse=True)
    risks_text = "\n".join([f"- {r.finding_title}: {r.risk_level} (Score: {r.risk_score})" for r in sorted_risks])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an Audit Manager. Create a prioritized audit plan based on the risk assessments."),
        ("human", f"Risks:\n{risks_text}\n\nCreate a plan with prioritized findings and recommended actions.")
    ])
    
    structured_llm = llm.with_structured_output(AuditPlan)
    chain = prompt | structured_llm
    plan = chain.invoke({})
    
    return {"plan": plan}

def reporting_node(state: AuditState):
    """
    Agent 4: Generate Executive Report (Markdown).
    """
    print("--- Reporting Node ---")
    findings = state.findings
    risks = state.risks
    plan = state.plan
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Chief Audit Executive. Write a concise, professional Executive Summary report in Markdown."),
        ("human", f"""
        Findings: {findings}
        Risks: {risks}
        Plan: {plan}
        
        Format:
        # Executive Audit Report
        ## Overview
        ## Key Findings & Risks
        ## Strategic Plan
        """)
    ])
    
    params = {} # Context is already in the f-string (simplified)
    # Note: best practice is passing via input dict, but f-string works for simple cases
    
    result = llm.invoke(prompt.format_messages())
    return {"final_report": result.content}

def notification_node(state: AuditState):
    """
    Agent 5: Send Telegram notification.
    """
    print("--- Notification Node ---")
    import streamlit as st # Access secrets
    
    # Try to get secrets, handling potential missing keys
    try:
        bot_token = st.secrets["TELEGRAM_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]
        
        preview = state.final_report[:200] + "..."
        message = f"🚨 *New Audit Report Generated* 🚨\n\n{preview}\n\n_Check the dashboard for full details._"
        
        result = send_telegram_message.invoke({"message": message, "chat_id": chat_id, "bot_token": bot_token})
        print(f"Telegram result: {result}")
        return {"telegram_sent": True}
        
    except Exception as e:
        print(f"Skipping Telegram: {e}")
        return {"telegram_sent": False}

# --- Graph Construction ---

workflow = StateGraph(AuditState)

workflow.add_node("drafting", drafting_node)
workflow.add_node("risk", risk_node)
workflow.add_node("planning", planning_node)
workflow.add_node("reporting", reporting_node)
workflow.add_node("notification", notification_node)

workflow.set_entry_point("drafting")
workflow.add_edge("drafting", "risk")
workflow.add_edge("risk", "planning")
workflow.add_edge("planning", "reporting")
workflow.add_edge("reporting", "notification")
workflow.add_edge("notification", END)

app_graph = workflow.compile()
