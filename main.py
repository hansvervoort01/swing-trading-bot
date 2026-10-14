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
