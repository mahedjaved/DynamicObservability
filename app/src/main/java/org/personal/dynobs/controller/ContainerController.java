package org.personal.dynobs.controller;

import org.personal.dynobs.service.PodmanService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;

@RestController
@RequestMapping("/api/containers")
public class ContainerController {

    private final PodmanService podmanService;
    private final org.personal.dynobs.service.OllamaService ollamaService;

    public ContainerController(PodmanService podmanService, org.personal.dynobs.service.OllamaService ollamaService) {
        this.podmanService = podmanService;
        this.ollamaService = ollamaService;
    }

    @GetMapping
    public List<String> getRunningContainers() {
        return podmanService.listRunningContainers();
    }

    @GetMapping("/{name}/analyze")
    public String analyzeContainerLogs(@org.springframework.web.bind.annotation.PathVariable String name) {
        String logs = podmanService.getContainerLogs(name);
        if (logs == null || logs.isEmpty() || logs.startsWith("Error")) {
            return "No logs available to analyze for " + name;
        }
        return ollamaService.analyzeLog(logs);
    }
}
