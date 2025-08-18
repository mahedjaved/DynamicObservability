package org.personal.dynobs.service;

import java.util.Random;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Business {

    private static final Logger logger = LoggerFactory.getLogger(Business.class);
    private final Random random = new Random();

    public void performBusinessOperation() {
        logger.info("Starting business operation");
        try {
            // simulate database operation
            simulateDatabaseOperation();

            // simulate external API call
            simulateExternalApiCall();

            // simulate some business logic
            simulateBusinessLogic();

            logger.info("Business operation completed successfully.");
        } catch (Exception e) {
            logger.error("An error occurred during business operation", e);
            throw e;
        }
    }

    private void simulateDatabaseOperation() {
        logger.debug("Executing database query");

        if (random.nextInt(100) < 5) { // 5% chance of database error
            logger.error("ALERT: Database connection failed - Connection pool exhausted");
            throw new RuntimeException("Database connection failed");
        }

        if (random.nextInt(100) < 15) { // 15% chance of slow query
            logger.warn("WARNING: Slow database query detected - Query took 2.5 seconds");
        } else {
            logger.info("Database query executed successfully in 150ms");
        }
    }

    private void simulateExternalApiCall() {
        logger.debug("Calling external API");

        if (random.nextInt(100) < 8) { // 8% chance of API error
            logger.error("ALERT: External API call failed - Service unavailable (503)");
            throw new RuntimeException("External API call failed");
        }

        if (random.nextInt(100) < 20) { // 20% chance of API timeout warning
            logger.warn("WARNING: External API response time exceeded threshold - 3.2 seconds");
        } else {
            logger.info("External API call completed successfully");
        }
    }

    private void simulateBusinessLogic() {
        logger.debug("Executing business logic");

        if (random.nextInt(100) < 3) { // 3% chance of business logic error
            logger.error("ALERT: Business rule validation failed - Invalid customer status");
            throw new RuntimeException("Business rule validation failed");
        }

        if (random.nextInt(100) < 12) { // 12% chance of business warning
            logger.warn("WARNING: Business rule applied - Customer limit exceeded, applying penalty");
        } else {
            logger.info("Business logic executed successfully");
        }
    }
}
