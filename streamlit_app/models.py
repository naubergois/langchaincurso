from typing import List, Optional
from pydantic import BaseModel, Field

class AuditFinding(BaseModel):
    """Represents a single drafted audit finding."""
    title: str = Field(description="Short title of the finding")
    description: str = Field(description="Detailed description of what was found")
    evidence: str = Field(description="Reference to the evidence supporting this finding")

class RiskAssessment(BaseModel):
    """Risk analysis for a finding."""
    finding_title: str
    risk_score: float = Field(description="Risk score from 0.0 to 10.0")
    anomaly_score: float = Field(description="Anomaly score from PyOD (if applicable)")
    risk_level: str = Field(description="High, Medium, or Low")
    justification: str = Field(description="Reasoning for the risk level")

class AuditPlan(BaseModel):
    """Prioritized plan for the audit."""
    prioritized_findings: List[str] = Field(description="List of finding titles in order of priority")
    recommended_actions: List[str] = Field(description="List of actions to take")
    audit_strategy: str = Field(description="Overall strategy for the audit")

class AuditState(BaseModel):
    """Global state for the LangGraph audit workflow."""
    case_input: str = Field(description="The raw input text/case provided by the user")
    findings: List[AuditFinding] = Field(default_factory=list, description="List of drafted findings")
    risks: List[RiskAssessment] = Field(default_factory=list, description="List of risk assessments")
    plan: Optional[AuditPlan] = Field(None, description="The final audit plan")
    final_report: str = Field("", description="The generated executive report in Markdown")
    telegram_sent: bool = Field(False, description="Whether the telegram notification was sent")
