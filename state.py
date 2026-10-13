"""
state.py - Het centrale datamodel voor de Swing- Trading Bot (V3).
Dit Pydantic-model reist door de gehele LangGraph-pijplijn.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class InsiderTradeData(BaseModel):
    """Gegevens over de gedetecteerde insider-transactie."""
    ticker: str
    company_name: str
    insider_name: str
    insider_title: str  # bijv. CEO, CFO, COO
    transaction_code: str = Field(description="Strikt 'Code P' voor Open Market Purchase")
    shares_bought: int
    price_per_share: float
    total_value_usd: float
    salary_impact_pct: Optional[float] = None
    is_cluster_buying: bool = False
    filing_date: str


class RiskAssessment(BaseModel):
    """Risico- en stop-loss berekeningen."""
    weekly_support_stop_loss: float
    target_take_profit: float
    position_size_pct: float = Field(default=3.0, description="Standaard 3%, opschaling tot 7%")
    risk_reward_ratio: float
    earnings_within_3_weeks: bool = False
    corporate_action_flag: bool = False


class BrokerExecutionPlan(BaseModel):
    """Routing en kostenmatrix naar DE GIRO of eToro."""
    recommended_broker: str  # 'DE_GIRO' of 'eToro'
    is_spot_asset: bool = True  # eToro uitsluitend 1x spot, geen CFD
    estimated_total_costs_eur: float
    expected_net_profit_eur: float
    meets_3x_cost_threshold: bool


class AgentState(BaseModel):
    """De algehele status die door alle 8 agenten wordt bijgewerkt."""
    # Step 1: Ingestie & Screener
    trade_signal: Optional[InsiderTradeData] = None
    daily_volume_usd: float = 0.0
    
    # Step 2: Macro Breaker
    macro_status: str = "GROEN"  # GROEN, GEEL, ROOD
    
    # Step 3 & 4: Analyse & Debate
    bull_arguments: List[str] = Field(default_factory=list)
    bear_arguments: List[str] = Field(default_factory=list)
    bear_risk_score: float = 0.0  # 0 tot 10
    
    # Step 5 & 6: Risk & Portfolio
    risk_metrics: Optional[RiskAssessment] = None
    total_portfolio_exposure_pct: float = 0.0
    
    # Step 7: Execution & Routing
    execution_plan: Optional[BrokerExecutionPlan] = None
    
    # Final Decision & Quality Gate
    final_score: float = 0.0  # Eisen >= 8.5/10
    approved_for_whatsapp: bool = False
    rejection_reason: Optional[str] = None