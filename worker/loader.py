"""
Handles the transformation and loading of extracted P2P data into the database.
"""
import logging
from typing import List, Dict, Any, Optional, Set
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import insert # Needed for ON CONFLICT

from .db import db_manager
from .models import (
    DimCryptocurrencies,
    DimFiatCurrencies,
    DimPaymentMethods,
    DimAdvertisers,
    FactOffers,
    FactOfferPaymentMethods,
)

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Transforms and loads P2P offer data into the PostgreSQL database.
    """

    def __init__(self):
        self.processed_offers = 0
        # Caches will now be pre-populated by batch loading for each run
        self._fiat_cache: Dict[str, int] = {}
        self._crypto_cache: Dict[str, int] = {}
        self._payment_method_cache: Dict[str, int] = {} # Key: method_code
        self._advertiser_cache: Dict[str, int] = {} # Key: advertiser_id

    def load_offers(self, offers: List[Dict[str, Any]], batch_id: uuid.UUID) -> None:
        """
        Main method to process and load a batch of offers into the database.

        Args:
            offers: A list of raw offer dictionaries from the extractor.
            batch_id: The UUID for the current extraction batch.
        """
        if not offers:
            logger.info("No offers to load.")
            return

        logger.info(f"Starting to load {len(offers)} offers for batch {batch_id}...")

        with db_manager.get_session() as session:
            try:
                # Clear caches for this run to avoid stale data and allow full batch loading
                self._fiat_cache = {}
                self._crypto_cache = {}
                self._payment_method_cache = {}
                self._advertiser_cache = {}

                logger.info(f"Loading dimensions for batch {batch_id}...")
                self._load_dimensions(session, offers)
                logger.info(f"Dimensions loaded for batch {batch_id}.")

                logger.info(f"Loading facts for batch {batch_id}...")
                self._load_facts(session, offers, batch_id)
                logger.info(f"Facts loaded for batch {batch_id}.")

                self.processed_offers = len(offers) # Processed offers is the count from this batch
                logger.info(f"Committing changes for batch {batch_id}...")
                session.commit() # Commit the transaction here
                logger.info(f"Successfully loaded {self.processed_offers} offers for batch {batch_id}.")
            except Exception as e:
                logger.error(f"Error loading offers for batch {batch_id}: {e}", exc_info=True)
                session.rollback() # Rollback on error
                raise

    def _get_crypto_id(self, session: Session, symbol: str) -> int:
        return self._crypto_cache.get(symbol)

    def _get_fiat_id(self, session: Session, code: str) -> int:
        return self._fiat_cache.get(code)

    def _get_payment_method_id(self, session: Session, method_code: str) -> int:
        return self._payment_method_cache.get(method_code)

    def _get_advertiser_sk(self, session: Session, adv_id: str) -> int:
        return self._advertiser_cache.get(adv_id)

    def _batch_load_cryptocurrencies(self, session: Session, offers: List[Dict[str, Any]]):
        unique_symbols = {offer['asset'] for offer in offers}
        
        # Query existing
        existing_cryptos = session.query(DimCryptocurrencies.crypto_id, DimCryptocurrencies.symbol)\
                                .filter(DimCryptocurrencies.symbol.in_(unique_symbols)).all()
        
        for crypto_id, symbol in existing_cryptos:
            self._crypto_cache[symbol] = crypto_id
        
        # Identify new
        existing_symbols = {c.symbol for c in existing_cryptos}
        new_symbols = unique_symbols - existing_symbols
        
        if new_symbols:
            new_crypto_objects = [
                DimCryptocurrencies(symbol=s, name=s, binance_asset_code=s)
                for s in new_symbols
            ]
            session.bulk_save_objects(new_crypto_objects)
            session.flush() # Flush to get generated IDs

            # Add newly created to cache
            for crypto in new_crypto_objects:
                self._crypto_cache[crypto.symbol] = crypto.crypto_id
        logger.debug(f"Loaded {len(unique_symbols)} crypto dimensions (new: {len(new_symbols)})")


    def _batch_load_fiat_currencies(self, session: Session, offers: List[Dict[str, Any]]):
        unique_codes = {offer['fiat'] for offer in offers}
        
        # Query existing
        existing_fiats = session.query(DimFiatCurrencies.fiat_id, DimFiatCurrencies.currency_code)\
                             .filter(DimFiatCurrencies.currency_code.in_(unique_codes)).all()
        
        for fiat_id, code in existing_fiats:
            self._fiat_cache[code] = fiat_id
            
        # Identify new
        existing_codes = {f.currency_code for f in existing_fiats}
        new_codes = unique_codes - existing_codes

        if new_codes:
            new_fiat_objects = [
                DimFiatCurrencies(currency_code=c, currency_name=c)
                for c in new_codes
            ]
            session.bulk_save_objects(new_fiat_objects)
            session.flush()

            for fiat in new_fiat_objects:
                self._fiat_cache[fiat.currency_code] = fiat.fiat_id
        logger.debug(f"Loaded {len(unique_codes)} fiat dimensions (new: {len(new_codes)})")


    def _batch_load_payment_methods(self, session: Session, offers: List[Dict[str, Any]]):
        unique_methods = set()
        for offer in offers:
            for pm in offer['payment_methods']:
                unique_methods.add((pm['identifier'], pm['tradeMethodName']))
        
        # Query existing
        existing_pms = session.query(DimPaymentMethods.payment_method_id, DimPaymentMethods.method_code)\
                            .filter(DimPaymentMethods.method_code.in_([m[0] for m in unique_methods])).all()
        
        for pm_id, method_code in existing_pms:
            self._payment_method_cache[method_code] = pm_id
        
        # Identify new
        existing_codes = {pm.method_code for pm in existing_pms}
        new_methods = [(code, name) for code, name in unique_methods if code not in existing_codes]

        if new_methods:
            new_pm_objects = [
                DimPaymentMethods(method_code=code, method_name=name)
                for code, name in new_methods
            ]
            session.bulk_save_objects(new_pm_objects)
            session.flush()

            for pm in new_pm_objects:
                self._payment_method_cache[pm.method_code] = pm.payment_method_id
        logger.debug(f"Loaded {len(unique_methods)} payment method dimensions (new: {len(new_methods)})")


    def _batch_load_advertisers(self, session: Session, offers: List[Dict[str, Any]]):
        unique_advertisers = {
            (offer['advertiser']['id'], offer['advertiser']['nickname'])
            for offer in offers
        }
        
        # Query existing (only current ones)
        existing_advertisers = session.query(DimAdvertisers.advertiser_sk, DimAdvertisers.advertiser_id)\
                                      .filter(DimAdvertisers.advertiser_id.in_([adv[0] for adv in unique_advertisers]),
                                              DimAdvertisers.is_current == True).all() # noqa
        
        for advertiser_sk, advertiser_id in existing_advertisers:
            self._advertiser_cache[advertiser_id] = advertiser_sk

        # Identify new
        existing_ids = {a.advertiser_id for a in existing_advertisers}
        new_advertisers = [(adv_id, nickname) for adv_id, nickname in unique_advertisers if adv_id not in existing_ids]

        if new_advertisers:
            new_adv_objects = [
                DimAdvertisers(
                    advertiser_id=adv_id,
                    nickname=nickname,
                    is_merchant=False, # Placeholder
                    registration_days=0, # Placeholder
                    effective_date=datetime.utcnow(),
                    is_current=True
                ) for adv_id, nickname in new_advertisers
            ]
            session.bulk_save_objects(new_adv_objects)
            session.flush()

            for adv in new_adv_objects:
                self._advertiser_cache[adv.advertiser_id] = adv.advertiser_sk
        logger.debug(f"Loaded {len(unique_advertisers)} advertiser dimensions (new: {len(new_advertisers)})")


    def _load_dimensions(self, session: Session, offers: List[Dict[str, Any]]):
        """Pre-load all dimensions using batch operations and leverage caching."""
        self._batch_load_cryptocurrencies(session, offers)
        self._batch_load_fiat_currencies(session, offers)
        self._batch_load_payment_methods(session, offers)
        self._batch_load_advertisers(session, offers)


    def _load_facts(self, session: Session, offers: List[Dict[str, Any]], batch_id: uuid.UUID):
        extraction_ts = datetime.utcnow()
        fact_objects = []
        offer_pm_objects = []

        for offer in offers:
            crypto_id = self._get_crypto_id(session, offer['asset'])
            fiat_id = self._get_fiat_id(session, offer['fiat'])
            advertiser_sk = self._get_advertiser_sk(session, offer['advertiser']['id'])

            fact = FactOffers(
                offer_external_id=offer['id'],
                batch_id=batch_id,
                extraction_timestamp=extraction_ts,
                crypto_id=crypto_id,
                fiat_id=fiat_id,
                advertiser_sk=advertiser_sk,
                trade_type=offer['trade_type'],
                price=offer['price'],
                available_amount=offer['available_amount'],
                min_limit=offer['min_limit'],
                max_limit=offer['max_limit'],
                completion_rate=offer['advertiser']['completion_rate'],
                total_orders_count=offer['advertiser']['total_orders'],
                terms_conditions=offer.get('terms'),
                is_available=True,
            )
            fact_objects.append(fact)
            
        session.bulk_save_objects(fact_objects)
        session.flush() # Flush to get offer_id for bridge table

        for fact in fact_objects:
            offer_data = next(o for o in offers if o['id'] == fact.offer_external_id) # Find original offer data
            for pm in offer_data['payment_methods']:
                pm_id = self._get_payment_method_id(session, pm['identifier'])
                offer_pm_objects.append(FactOfferPaymentMethods(
                    offer_id=fact.offer_id,
                    extraction_timestamp=extraction_ts,
                    payment_method_id=pm_id
                ))
        session.bulk_save_objects(offer_pm_objects)


# Global loader instance
loader = DataLoader()