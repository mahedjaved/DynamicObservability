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
        try {
            dockerClient.createContainerCmd(image).exec();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String getContainerLogs(String containerName) {
        if (dockerClient == null)
            return "Docker Client Unavailable";
        try {
            // Fetch last 5 lines of logs
            // Logic requires a callback to capture the stream
            final StringBuilder logBuilder = new StringBuilder();
            dockerClient.logContainerCmd(containerName)
                    .withStdOut(true)
                    .withStdErr(true)
                    .withTail(5) // Last 5 lines
                    .exec(new com.github.dockerjava.api.async.ResultCallback.Adapter<com.github.dockerjava.api.model.Frame>() {
                        @Override
                        public void onNext(com.github.dockerjava.api.model.Frame object) {
                            logBuilder.append(new String(object.getPayload()));
                        }
                    }).awaitCompletion();
            return logBuilder.toString();
        } catch (Exception e) {
            return "Error fetching logs: " + e.getMessage();
        }
    }
}
