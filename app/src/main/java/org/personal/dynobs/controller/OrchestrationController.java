package org.personal.dynobs.controller;

import org.personal.dynobs.service.OrchestrationService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/orchestrate")
public class OrchestrationController {

    private final OrchestrationService orchestrationService;

    public OrchestrationController(OrchestrationService orchestrationService) {
        this.orchestrationService = orchestrationService;
    }

    @GetMapping
    public java.util.List<String> getOrchestrations() {
        return orchestrationService.getAvailableOrchestrations();
    }

    @PostMapping("/web-stack")
    public String deployWebStack() {
        return orchestrationService.deployWebStack();
    }
}
