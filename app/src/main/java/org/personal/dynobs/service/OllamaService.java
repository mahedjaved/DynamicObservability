package org.personal.dynobs.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Map;
import java.util.HashMap;

@Service
public class OllamaService {

    private final RestTemplate restTemplate = new RestTemplate();
    private final String OLLAMA_API_URL = "http://localhost:11434/api/chat"; // Default Ollama URL

    public String analyzeLog(String logMessage) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            Map<String, Object> body = new HashMap<>();
            body.put("model", "llama3.2:3b");
            body.put("stream", false);

            String prompt = "Analyze this log for ALERT or INFO: " + logMessage
                    + ". Return JSON with classification and analysis.";

            Map<String, String> message = new HashMap<>();
            message.put("role", "user");
            message.put("content", prompt);

            body.put("messages", new Object[] { message });

            HttpEntity<Map<String, Object>> request = new HttpEntity<>(body, headers);

            ResponseEntity<String> response = restTemplate.postForEntity(OLLAMA_API_URL, request, String.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                ObjectMapper mapper = new ObjectMapper();
                JsonNode root = mapper.readTree(response.getBody());
                return root.path("message").path("content").asText();
            }
        } catch (Exception e) {
            System.err.println("Ollama analysis failed: " + e.getMessage());
            return "Analysis Unavailable";
        }
        return "Unknown";
    }
}
