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

    public ContainerController(PodmanService podmanService) {
        this.podmanService = podmanService;
    }

    @GetMapping
    public List<String> getRunningContainers() {
        return podmanService.listRunningContainers();
    }
}
