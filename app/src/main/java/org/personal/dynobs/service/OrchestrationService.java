package org.personal.dynobs.service;

import org.springframework.stereotype.Service;
import java.util.concurrent.CompletableFuture;

@Service
public class OrchestrationService {

    private final PodmanService podmanService;

    public OrchestrationService(PodmanService podmanService) {
        this.podmanService = podmanService;
    }

    public java.util.List<String> getAvailableOrchestrations() {
        return java.util.Arrays.asList("Deploy Web Stack (Nginx + Redis)", "Deploy Observability Stack");
    }

    // Example orchestration pattern: Deploy a web stack
    public String deployWebStack() {
        // In a real scenario, this would handle network creation, ordering, etc.
        // For prototype: Async trigger creation of dummy containers
        CompletableFuture.runAsync(() -> {
            podmanService.startContainer("nginx:latest");
            // Simulate startup delay
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
            }
            podmanService.startContainer("redis:alpine");
        });

        return "Web Stack Deployment Triggered";
    }
}
