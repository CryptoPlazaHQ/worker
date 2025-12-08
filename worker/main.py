"""
Main entry point for the P2P data ingestion worker.
"""
import logging
import time
import schedule
import uuid
from datetime import datetime # New import

from worker.config import settings
from worker.extractor import extractor
from worker.loader import loader

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def job():
    """The main job to be scheduled."""
    batch_id = uuid.uuid4()
    logger.info(f"[{datetime.now()}] Starting P2P data extraction job (Batch ID: {batch_id})...")
    
    offers_extracted = 0
    offers_loaded = 0

    try:
        # 1. Extract data
        offers = extractor.extract_all_offers()
        offers_extracted = len(offers)
        logger.info(f"[{datetime.now()}] Extracted {offers_extracted} offers for Batch ID: {batch_id}.")
        
        # 2. Load data
        if offers:
            offers_loaded = loader.load_offers(offers, batch_id) # Assuming loader.load_offers returns count
            logger.info(f"[{datetime.now()}] Loaded {offers_loaded} offers for Batch ID: {batch_id}.")
        else:
            logger.info(f"[{datetime.now()}] No offers to load for Batch ID: {batch_id}.")
        
        logger.info(f"[{datetime.now()}] P2P data extraction job finished successfully (Batch ID: {batch_id}). Total extracted: {offers_extracted}, Total loaded: {offers_loaded}.")
    
    except Exception as e:
        logger.error(f"[{datetime.now()}] An error occurred during job (Batch ID: {batch_id}): {e}", exc_info=True)

def main():
    """
    Main function to run the worker.
    Schedules the job to run at the specified interval and provides continuous feedback.
    """
    logger.info(f"Worker starting. Job will run every {settings.extraction_interval_minutes} minutes.")
    
    # Schedule the job FIRST (before running manually)
    schedule.every(settings.extraction_interval_minutes).minutes.do(job)
    
    # Get next run time
    next_run_time = schedule.next_run()
    logger.info(f"[{datetime.now()}] Next scheduled run: {next_run_time}")
    
    # Run immediately
    job()
    
    # Recalculate next run after manual execution for accurate tracking
    # APScheduler's next_run_time would handle this more elegantly, but for `schedule` we re-evaluate
    next_run_time = schedule.next_run()
    logger.info(f"[{datetime.now()}] After initial run, next scheduled run: {next_run_time}")
    
    # Keep running and checking for pending jobs
    while True:
        schedule.run_pending()
        time.sleep(10)  # Check every 10 seconds instead of 1 for less CPU usage
        
        # Log a heartbeat every 60 seconds (approx) to indicate worker is alive
        if int(time.time()) % 60 == 0:
            next_run = schedule.next_run()
            logger.info(f"[{datetime.now()}] Scheduler alive. Next job: {next_run}")

if __name__ == "__main__":
    main()
