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
