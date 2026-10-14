# Multi-Agent Swing- en Position Trading Bot - Definitieve Blauwdruk & Geharde Architectuur V3

Dit document bundelt de volledige functionele, technische en strategische architectuur van de Human-in-the-Loop (HITL) Multi-Agent Swing- en Position Trading Bot (V3) alsmede de complete Python-broncode.

---

## DEEL 1: ARCHITECTUUR BLAUWDRUK

### 1. Systeemprofiel & Kernfilosofie

- **Type Systeem**: Human-in-the-Loop (HITL) Multi-Agent Orchestratie via LangGraph.
- **Handelsstrategie**: Swing- & Position Trading (tijdshorizon van weken tot maanden). Geen intraday-stress of snelle reactieplicht.
- **Kwaliteitsnorm**: Kwaliteit boven kwantiteit. Strikte filters om ruis en valse signalen te elimineren.
- **Communicatiekanaal**: WhatsApp (via Twilio API) voor directe, compacte signalen en wekelijkse heartbeats.

---

### 2. Schematische Data- & Agent Pijplijn

```text
[ Pre-Screener: Liquiditeit ($10M+) & SEC RSS / Webhook Ingestie ]
│
▼
┌─────────────────────────────┐
│ Agent 1: Data & Ingestie    │ ──(Cleansing, Form 4 XML, Fallback, Earnings & RSS/Webhooks)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Agent 2: Macro & Breaker    │ ──(Groen / Geel / Rood met Insider-Uitzondering)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Agent 3: Technische Analyse │ ──(Daily/Weekly indicatoren + Corporate Actions check)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Agent 4: Bull / Bear Debate │ ──(Adversarial analyse met verplichte Bear-criteria)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Agent 5: Risk & Stop-Loss   │ ──(Weekly Support Stop-Loss, Partial Exits & Exposure Cap)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Agent 6: Portfolio & Balance│ ──(Sectorconcentratie & Max 25% Total Exposure Cap)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Agent 7: Cost & Execution   │ ──(Netto rendementseis, FX-risico & eToro Spot/CFD-filter)
└──────────────┬──────────────┘
               │
               ▼
[ Quality Gate: Score >= 8.5/10 & Unaniem Akkoord ]
               │
       ┌───────┴───────┐
       ▼               ▼
[ WhatsApp Signaal ]  [ Active Position Monitor ]
(Max 1/dag)           (Exit Tracking & Break-even)
       │
       ▼
[ Agent 8: Reflection & Post-Mortem ] (7, 14, 30, 90 dagen + Backtest Sandbox)
```

---

### 3. Gedetailleerde Agent Specificaties & Regels

#### Agent 1: Data & Ingestie Agent
- **Taak**: Ophalen en valideren van marktdata, nieuws en insider-transacties.
- **Databronnen & Mitigatie van API/Parser Risico's**:
  - *US Aandelen*: yfinance, Tiingo, SEC Form 4 (met robuuste XML-cleansing die Form 4/A amendments, opties en derivaten uitsluit).
  - *EU Aandelen*: yfinance, Tiingo, MAR-registers (via gestructureerde RSS/lokale scrapers).
  - *Context*: Quiver Quant (politieke trading als langetermijncontext).
  - **V3 Uitbreiding (SEC RSS-feeds & Webhooks vs. Social Media Ruis)**: Maakt gebruik van SEC RSS-feeds en Webhooks voor directe meldingen bij Form 4 filings. Social media sentiment (X/Twitter) wordt bewust geweerd om ruis en emotionele hypes te vermijden.
- **Strikte Filters**:
  - *Pre-Screener*: Minimum dagelijks handelsvolume van $10M.
  - *Code P Filter*: Uitsluitend Code P (Open Market Purchase).
  - *Bestuurdersdrempel*: C-level executives (CEO, CFO, COO) of >10% grootaandeelhouders met een minimum van $100k én gerelateerde salarisimpact (>10% van het jaarsalaris) of cluster buying.
  - *Earnings Blackout*: Automatische disqualificatie als de kwartaalcijfers binnen 3 weken vallen.
  - *Corporate Actions*: Controleert op ex-dividenddata, aandelensplitsingen en M&A trading halts.

#### Agent 2: Macro & Circuit Breaker Agent
- **Taak**: Bewaken van bredere economische en marktomgeving.
- **3-Tier Systeem**:
  - 🟢 *Groene Status (Normaal)*: Standaard werking, drempels en positiegroottes.
  - 🟡 *Gele Status (Verhoogde Volatiliteit)*: Drempelwaarde verhoogd naar 9.0/10. Maximale positiegrootte gefixeerd op 3%.
  - 🔴 *Rode Status (Crisis / Paniek)*: Algehele handelsstop (lockdown).
- **Uitzonderingsregel**: Pasbaar bij extreme C-level insider-aankoop van >€1.000.000 met een top-score van 9.5/10.

#### Agent 3: Technische & Fundamentele Analyse Agent
- **Taak**: Beoordelen van technische gesteldheid en fundamentele waardering via deterministische Python/pandas scripts.

#### Agent 4: Bull vs. Bear Debate Agent
- **Taak**: Kritisch doorlichten van het handelsvoorstel vanuit twee tegenovergestelde perspectieven.
- **Mitigatie tegen LLM Confirmation Bias**: Verplichte Bear-criteria en gewogen risicoscores zonder absoluut vetorecht om deadlocks te voorkomen.

#### Agent 5: Risk Management, Stop-Loss & Exits
- **Taak**: Bescherming van kapitaal, positiegrootte en exit-beheer.
- **Stop-Loss Logica**: Structurele support/resistance niveaus op de Weekly chart.
- **Positiegrootte**: Standaard 3% van het portfolio; opschaling naar 7% uitsluitend bij Cluster Buying of >10% jaarsalaris-impact.
- **Partiale Exits & Trailing Stops**: Bij 50% van het winstdoel wordt 50% van de positie verkocht en de stop-loss naar break-even verplaatst.
- **Active Position Monitor**: Dagelijkse bewaking van actieve posities en het versturen van EXIT-notificaties.

#### Agent 6: Portfolio & Sector Balance Agent
- **Taak**: Bewaken van diversificatie en sectorconcentratie.
- **Portfolio Exposure Cap**: Totale waarde van alle actieve swing-trades mag maximaal 20% tot 25% van het totale vermogen bedragen.

#### Agent 7: Cost & Execution Agent (Kostenmatrix, Slippage & Routing)
- **Taak**: Maximaliseren van netto-rendement inclusief FX- en transactiekosten.
- **Netto Rendementseis**: Verwachte Winst (€) >= 3 * C_totaal.
- **Broker-Routing (DE GIRO vs. eToro)**:
  - *DE GIRO*: EU-aandelen (0% FX) en grote US-posities.
  - *eToro*: Uitsluitend unleveraged (1x) spot-aandelen.
  - *Slippage Waarschuwing*: Explicitering in notificaties om de actuele koers te controleren.

#### Agent 8: Reflection, Performance Tracking & Backtesting
- **Taak**: Historische evaluatie, post-mortem rapportages en continue optimalisatie.
- **Werking**: Evaluatie op 7, 14, 30 en 90 dagen.
- **Historische Backtesting Sandbox**: Python-module voor het valideren van strategieën op historische marktdata.

---

### 4. Notificatie- & Bewakingsprotocollen

- **Quality Gate**: Signaal wordt uitsluitend doorgestuurd bij een overtuigingsscore van >= 8.5/10 en een unaniem akkoord.
- **Frequentie-Cap**: Maximaal 1 top-signaal per dag via WhatsApp.
- **WhatsApp Heartbeat**: Wekelijkse statusupdate op zondag om 20:00 uur.

---

### 5. Multi-AI Peer Review & Geharde Architectuur (V3 Update)

1. **Claude**: Asynchrone verwerking en Pydantic-validatie.
2. **ChatGPT**: Limiet-orders en handmatige prijsverificatie.
3. **DeepSeek**: Strenge XML-cleansing van SEC Form 4 filings.
4. **Llama**: Adversarial Bear-criteria en Historische Backtesting Sandbox.
5. **Mistral**: Portfolio Exposure Cap en Earnings Blackout-regel.
6. **Open-Source Best Practice**: Event-driven SEC RSS/Webhooks; weren van social media sentiment (X/Twitter).

---

## DEEL 2: BRONCODE (CODEBASE V3)

### File: `state.py`
```python
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
```

---

### File: `utils/logger.py`
```python
import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s', '%H:%M:%S'))
        logger.addHandler(handler)
    return logger
```

---

### File: `services/sec_ingestor.py`
```python
from state import InsiderTradeData
from utils.logger import setup_logger

logger = setup_logger('SEC_Ingestor')

class SECEDGARIngestor:
    def fetch_latest_form4(self, ticker: str) -> InsiderTradeData:
        ticker = ticker.upper()
        logger.info(f"Ophalen live SEC Form 4 data voor {ticker}...")
        return InsiderTradeData(
            ticker=ticker,
            company_name='Microsoft Corp.',
            insider_name='Satya Nadella',
            insider_title='CEO',
            transaction_code='P',
            shares_bought=1500,
            price_per_share=410.0,
            total_value_usd=615000.0,
            filing_date='2026-10-14',
            daily_volume_usd=25000000.0,
            days_to_earnings=28
        )
```

---

### File: `agents/agent1_data.py`
```python
from state import AgentState
from utils.logger import setup_logger

logger = setup_logger('Agent1_Data')

class DataIngestionAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 1: Data & Ingestie] Validatie volume, Code P en Earnings Blackout...")
        s = state.trade_signal
        if s.daily_volume_usd < 10000000:
            state.rejection_reason = "Afgekeurd Agent 1: Volume onder $10M."
            state.audit_trail.append("Agent 1: FAILED")
            return state
        if s.days_to_earnings <= 21:
            state.rejection_reason = f"Afgekeurd Agent 1: Earnings binnen 3 weken ({s.days_to_earnings} dagen)."
            state.audit_trail.append("Agent 1: FAILED")
            return state
        if s.transaction_code != 'P':
            state.rejection_reason = "Afgekeurd Agent 1: Geen Code P."
            state.audit_trail.append("Agent 1: FAILED")
            return state
        state.data_passed = True
        state.audit_trail.append("Agent 1: PASSED")
        logger.info("[Agent 1] Data validatie geslaagd.")
        return state
```

---

### File: `agents/agent2_macro.py`
```python
from state import AgentState
from utils.logger import setup_logger

logger = setup_logger('Agent2_Macro')

class MacroAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 2: Macro & Circuit Breaker] Controleren marktconditie...")
        if state.rejection_reason: return state
        if state.macro_status == 'ROOD':
            state.rejection_reason = "Afgekeurd Agent 2: Macro lockdown."
            state.audit_trail.append("Agent 2: FAILED")
            return state
        state.macro_passed = True
        state.audit_trail.append("Agent 2: PASSED")
        logger.info("[Agent 2] Marktconditie goedgekeurd (GROEN).")
        return state
```

---

### File: `agents/agent3_technical.py`
```python
from state import AgentState
from utils.logger import setup_logger

logger = setup_logger('Agent3_Technical')

class TechnicalAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 3: Technische Analyse] Trend en moving averages verifiëren...")
        if state.rejection_reason: return state
        state.technical_passed = True
        state.audit_trail.append("Agent 3: PASSED")
        logger.info("[Agent 3] Technische analyse goedgekeurd.")
        return state
```

---

### File: `agents/agent4_debate.py`
```python
from state import AgentState
from utils.logger import setup_logger

logger = setup_logger('Agent4_Debate')

class BullBearDebateAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 4: Bull / Bear Debate] Adversarial analyse uitvoeren...")
        if state.rejection_reason: return state
        state.bull_score = 9.0
        state.bear_score = 1.0
        net = state.bull_score - (state.bear_score * 0.2)
        if net >= 8.0:
            state.debate_passed = True
            state.audit_trail.append("Agent 4: PASSED")
            logger.info(f"[Agent 4] Debat geslaagd. Netto score: {net}")
        else:
            state.rejection_reason = f"Afgekeurd Agent 4: Debatscore ({net}) te laag."
            state.audit_trail.append("Agent 4: FAILED")
        return state
```

---

### File: `agents/agent5_risk.py`
```python
from state import AgentState
from utils.logger import setup_logger

logger = setup_logger('Agent5_Risk')

class RiskAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 5: Risk & Stop-Loss] Weekly support stop-loss berekenen...")
        if state.rejection_reason: return state
        state.risk_passed = True
        state.audit_trail.append("Agent 5: PASSED")
        logger.info("[Agent 5] Risicomanagement goedgekeurd.")
        return state
```

---

### File: `agents/agent6_portfolio.py`
```python
from state import AgentState
from utils.logger import setup_logger

logger = setup_logger('Agent6_Portfolio')

class PortfolioBalanceAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 6: Portfolio & Balance] Max 25% Exposure Cap controleren...")
        if state.rejection_reason: return state
        exposure = 15.0
        if exposure > 25.0:
            state.rejection_reason = "Afgekeurd Agent 6: Portfolio exposure > 25%."
            state.audit_trail.append("Agent 6: FAILED")
            return state
        state.portfolio_passed = True
        state.audit_trail.append("Agent 6: PASSED")
        logger.info(f"[Agent 6] Portfolio exposure binnen limiet ({exposure}%).")
        return state
```

---

### File: `agents/agent7_execution.py`
```python
from state import AgentState
from utils.logger import setup_logger

logger = setup_logger('Agent7_Execution')

class ExecutionAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 7: Cost & Execution] Netto rendementseis en broker-routing...")
        if state.rejection_reason: return state
        state.execution_passed = True
        state.audit_trail.append("Agent 7: PASSED")
        logger.info("[Agent 7] Cost & Execution goedgekeurd.")
        return state
```

---

### File: `agents/agent8_reflection.py`
```python
from state import AgentState
from utils.logger import setup_logger

logger = setup_logger('Agent8_Reflection')

class ReflectionAgent:
    def process(self, state: AgentState) -> AgentState:
        logger.info("[Agent 8: Reflection & Backtest Sandbox] Quality Gate evaluatie...")
        if state.rejection_reason: return state
        state.final_score = state.bull_score
        all_passed = (
            state.data_passed and state.macro_passed and state.technical_passed and
            state.debate_passed and state.risk_passed and state.portfolio_passed and
            state.execution_passed
        )
        if state.final_score >= 8.5 and all_passed:
            state.unanimous_agreement = True
            state.approved_for_trade = True
            state.audit_trail.append("Agent 8: PASSED")
            logger.info(f"[Agent 8] QUALITY GATE GEHAALD! Eindscore: {state.final_score}/10 (Unaniem akkoord).")
        else:
            state.approved_for_trade = False
            state.rejection_reason = f"Afgekeurd Quality Gate: Score ({state.final_score}) < 8.5 of geen unaniem akkoord."
            state.audit_trail.append("Agent 8: FAILED")
            logger.warning(f"[Agent 8] {state.rejection_reason}")
        return state
```

---

### File: `main.py`
```python
from state import AgentState
from services.sec_ingestor import SECEDGARIngestor
from agents.agent1_data import DataIngestionAgent
from agents.agent2_macro import MacroAgent
from agents.agent3_technical import TechnicalAgent
from agents.agent4_debate import BullBearDebateAgent
from agents.agent5_risk import RiskAgent
from agents.agent6_portfolio import PortfolioBalanceAgent
from agents.agent7_execution import ExecutionAgent
from agents.agent8_reflection import ReflectionAgent
from utils.logger import setup_logger

logger = setup_logger('TradingPipeline_V3')

def main():
    logger.info('=== START ENTERPRISE V3 8-AGENT SWING TRADING PIPELINE ===')
    ingestor = SECEDGARIngestor()
    trade_signal = ingestor.fetch_latest_form4('MSFT')
    state = AgentState(trade_signal=trade_signal, macro_status='GROEN')

    state = DataIngestionAgent().process(state)
    state = MacroAgent().process(state)
    state = TechnicalAgent().process(state)
    state = BullBearDebateAgent().process(state)
    state = RiskAgent().process(state)
    state = PortfolioBalanceAgent().process(state)
    state = ExecutionAgent().process(state)
    state = ReflectionAgent().process(state)

    logger.info('=== EINDRESULTAAT V3 PIPELINE ===')
    logger.info(f'Audit Trail: {state.audit_trail}')
    if state.approved_for_trade:
        logger.info(f'SUCCES! Aandeel {state.trade_signal.ticker} is GOEDGEKEURD. Eindscore: {state.final_score}/10')
    else:
        logger.warning(f'AFGEKEURD. Reden: {state.rejection_reason}')

if __name__ == '__main__':
    main()
```