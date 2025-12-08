"""
Main entry point for the P2P data ingestion worker.
"""
import logging
import time
import uuid
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler # Changed to BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED # New APScheduler event imports

from worker.config import settings
from worker.extractor import extractor
from worker.loader import loader

logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Global variable to store last job's results for display in monitoring loop
last_job_summary = "No job has run yet."

def job_listener(event):
    global last_job_summary
    if event.exception:
        logger.error(f"Job '{event.job_id}' failed with exception: {event.exception}", exc_info=event.traceback)
        last_job_summary = f"Job '{event.job_id}' FAILED at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {event.exception}"
    else:
        # Assuming job() logs its own success, this listener just confirms execution
        # For more detailed summary here, job() would need to return data
        last_job_summary = f"Job '{event.job_id}' EXECUTED successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


def job():
    """The main job to be scheduled."""
    global last_job_summary # Allow modification of global summary
    batch_id = uuid.uuid4()
    job_start_time = datetime.now()
    offers_extracted = 0
    offers_loaded = 0

    logger.info(f"[{job_start_time.strftime('%Y-%m-%d %H:%M:%S')}] Starting P2P data extraction job (Batch ID: {batch_id})...")
    
    # Reset processed_offers for this job run, assuming loader is global
    loader.processed_offers = 0 

    try:
        # 1. Extract data
        offers = extractor.extract_all_offers()
        offers_extracted = len(offers)
        logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Extracted {offers_extracted} offers for Batch ID: {batch_id}.")
        
        # 2. Load data
        if offers:
            loader.load_offers(offers, batch_id)
            offers_loaded = loader.processed_offers # Get count after loading
            logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Loaded {offers_loaded} offers for Batch ID: {batch_id}.")
        else:
            logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] No offers to load for Batch ID: {batch_id}.")
        
        job_end_time = datetime.now()
        duration = (job_end_time - job_start_time).total_seconds()
        logger.info(f"[{job_end_time.strftime('%Y-%m-%d %H:%M:%S')}] P2P data extraction job finished successfully (Batch ID: {batch_id}). Total extracted: {offers_extracted}, Total loaded: {offers_loaded}. Duration: {duration:.2f} seconds.")
        last_job_summary = f"LAST JOB ({str(batch_id)[:8]}...): SUCCESS - Extracted {offers_extracted}, Loaded {offers_loaded} in {duration:.2f}s"
    
    except Exception as e:
        job_end_time = datetime.now()
        duration = (job_end_time - job_start_time).total_seconds()
        logger.error(f"[{job_end_time.strftime('%Y-%m-%d %H:%M:%S')}] An error occurred during job (Batch ID: {batch_id}): {e}", exc_info=True)
        last_job_summary = f"LAST JOB ({str(batch_id)[:8]}...): FAILED - {e}"


def main():
    """Main function to run the worker with APScheduler."""
    logger.info(f"Worker starting. Job will run every {settings.extraction_interval_minutes} minutes.")
    
    # Create scheduler
    scheduler = BackgroundScheduler() # Use BackgroundScheduler
    
    # Add job with interval trigger
    scheduler.add_job(
        job,
        trigger=IntervalTrigger(minutes=settings.extraction_interval_minutes),
        id='p2p_extraction_job',
        name='P2P Data Extraction',
        replace_existing=True,
        next_run_time=datetime.now() # Run immediately on start
    )

    # Add listeners for job events
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    
    logger.info("Scheduler configured. Starting...")
    
    try:
        scheduler.start()
        logger.info("Scheduler started in background. Monitoring worker status...")

        while True:
            # Check for next scheduled run
            jobs = scheduler.get_jobs()
            next_run_info = "No jobs scheduled"
            if jobs:
                # Assuming one job, or getting info for the primary job
                next_run_time = jobs[0].next_run_time
                if next_run_time:
                    next_run_info = f"Next run: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}"
                else:
                    next_run_info = "Job scheduled, but next_run_time is None (likely running now or just finished immediate run)"

            logger.info(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Worker alive. {next_run_info}. {last_job_summary}")
            time.sleep(settings.extraction_interval_minutes * 60 / 2) # Check roughly every half interval

    except (KeyboardInterrupt, SystemExit):
        logger.info("Worker stopped. Shutting down scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down.")

if __name__ == "__main__":
    main()
