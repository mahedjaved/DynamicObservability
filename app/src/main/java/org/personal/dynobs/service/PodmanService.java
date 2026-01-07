package org.personal.dynobs.service;

import com.github.dockerjava.api.DockerClient;
import com.github.dockerjava.core.DefaultDockerClientConfig;
import com.github.dockerjava.core.DockerClientImpl;
import com.github.dockerjava.httpclient5.ApacheDockerHttpClient;
import com.github.dockerjava.transport.DockerHttpClient;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class PodmanService {

    private DockerClient dockerClient;

    public PodmanService() {
        // Default configuration looks for DOCKER_HOST env var or default socket
        // For Podman on Windows, user might need to set DOCKER_HOST to
        // tcp://localhost:2375 or pipe
        try {
            DefaultDockerClientConfig config = DefaultDockerClientConfig.createDefaultConfigBuilder().build();
            DockerHttpClient httpClient = new ApacheDockerHttpClient.Builder()
                    .dockerHost(config.getDockerHost())
                    .sslConfig(config.getSSLConfig())
                    .maxConnections(100)
                    .build();
            this.dockerClient = DockerClientImpl.getInstance(config, httpClient);
        } catch (Exception e) {
            System.err.println("Failed to initialize Docker Client (Podman): " + e.getMessage());
        }
    }

    public List<String> listRunningContainers() {
        if (dockerClient == null)
            return Collections.emptyList();
        try {
            return dockerClient.listContainersCmd()
                    .withStatusFilter(Collections.singleton("running"))
                    .exec()
                    .stream()
                    .map(c -> c.getNames()[0]) // simplified for demo
                    .collect(Collectors.toList());
        } catch (Exception e) {
            System.err.println("Error listing containers: " + e.getMessage());
            return Collections.emptyList();
        }
    }

    // Additional methods for start/stop to be added
    public void startContainer(String image) {
        if (dockerClient == null)
            return;
        // Simplified start logic for orchestration demo
        try {
            dockerClient.createContainerCmd(image).exec();
            // Logic to start... simplifying for initial scaffolding
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
