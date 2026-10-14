from pydantic import BaseModel, Field
from typing import List, Optional

class InsiderTradeData(BaseModel):
    ticker: str
    company_name: str
    insider_name: str
    insider_title: str
    transaction_code: str
    shares_bought: int
    price_per_share: float
    total_value_usd: float
    filing_date: str
    daily_volume_usd: float = 15000000.0
    days_to_earnings: int = 28

class AgentState(BaseModel):
    trade_signal: InsiderTradeData
    macro_status: str = "GROEN"
    data_passed: bool = False
    macro_passed: bool = False
    technical_passed: bool = False
    bull_score: float = 0.0
    bear_score: float = 0.0
    debate_passed: bool = False
    risk_passed: bool = False
    portfolio_passed: bool = False
    execution_passed: bool = False
    final_score: float = 0.0
    unanimous_agreement: bool = False
    approved_for_trade: bool = False
    rejection_reason: Optional[str] = None
    audit_trail: List[str] = Field(default_factory=list)
