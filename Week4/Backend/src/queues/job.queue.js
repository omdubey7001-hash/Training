import logger from "../utils/logger.js";
import { jobMetrics } from "../metrics/job.metrics.js";

class JobQueue {
  constructor() {
    this.queue = [];
    this.processing = false;
  }

  add(job, options = {}) {
    const jobWithMeta = {
      handler: job,
      attempts: options.attempts || 3,
      backoff: options.backoff || 1000,
      currentAttempt: 0
    };

    jobMetrics.totalJobs++;

    logger.info("Job added to queue", {
      totalJobs: jobMetrics.totalJobs
    });

    this.queue.push(jobWithMeta);
    this.process();
  }

  async process() {
    if (this.processing) return;
    this.processing = true;

    while (this.queue.length > 0) {
      const job = this.queue.shift();

      try {
        job.currentAttempt++;
        logger.info("Job attempt started", {
          attempt: job.currentAttempt
        });

        await job.handler();


        jobMetrics.completedJobs++;

        logger.info("Job completed", {
          completedJobs: jobMetrics.completedJobs
        });

      } catch (err) {
        jobMetrics.failedJobs++;

        logger.error("Job failed", {
          failedJobs: jobMetrics.failedJobs,
          error: err.message
        });

        if (job.currentAttempt < job.attempts) {
          const delay = job.backoff * job.currentAttempt;

          logger.info("Retrying job with backoff", {
            delayMs: delay
          });

          await new Promise(res => setTimeout(res, delay));
          this.queue.push(job);
        }
      }
    }

    this.processing = false;
  }
}

export default new JobQueue();
