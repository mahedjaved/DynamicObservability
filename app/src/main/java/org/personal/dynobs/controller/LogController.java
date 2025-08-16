package org.personal.dynobs.controller;

import java.util.Random;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class LogController {

    private static final Logger logger = LoggerFactory.getLogger(LogController.class);
    private final Random random = new Random();

    @GetMapping("/health")
    public String health() {
        logger.info("Health check endpoint called");
        return "Service is up and running";
    }

    @PostMapping("/process")
    public String processData(@RequestBody String data) {
        logger.info("Processing data request with payload size: {}", data.length());
        // Simulate processing time
        try {
            Thread.sleep(random.nextInt(1000) + 100);
        } catch (InterruptedException e) {
            logger.error("Processing interrupted", e);
            Thread.currentThread().interrupt();
            return "Processing interrupted";
        }

        // randomly generated different types of logs
        int logType = random.nextInt(10);

        if (logType < 6) {
            logger.info("Data processing completed successfully for request");
            return "Data processed successfully";
        } else if (logType < 8) {
            logger.warn("Data processing completed with warnings - some fields were missing");
            return "Data processed with warnings";
        } else {
            logger.error("Data processing failed - invalid data format detected");
            return "Data processing failed";
        }

    }

    @GetMapping("/simulate-error")
    public String simulateError() {
        logger.error("ALERT: Critical error in simulate-error endpoint - Database connection failed");
        throw new RuntimeException("Simulated critical error");
    }

    @GetMapping("/simulate-warning")
    public String simulateWarning() {
        logger.warn("WARNING: High memory usage detected - Current usage: 85%");
        return "Warning logged";
    }

    @GetMapping("/simulate-info")
    public String simulateInfo() {
        logger.info("INFO: Regular operation - User session created successfully");
        return "Info logged";
    }

    @GetMapping("/batch-process")
    public String batchProcess() {
        logger.info("Starting batch processing job");

        for (int i = 1; i <= 5; i++) {
            try {
                Thread.sleep(200);
                if (i == 3 && random.nextBoolean()) {
                    logger.error("ALERT: Batch processing failed at step {} - Connection timeout", i);
                    return "Batch processing failed";
                } else {
                    logger.info("Batch processing step {} completed", i);
                }
            } catch (InterruptedException e) {
                logger.error("Batch processing interrupted", e);
                Thread.currentThread().interrupt();
                return "Batch processing interrupted";
            }
        }

        logger.info("Batch processing completed successfully");
        return "Batch processing completed";
    }

}
