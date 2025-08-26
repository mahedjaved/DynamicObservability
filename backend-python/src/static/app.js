// Observability Agent Dashboard JavaScript

class ObservabilityDashboard {
    constructor() {
        this.apiBase = '/api';
        this.monitoringActive = false;
        this.logRefreshInterval = null;
        
        this.initializeEventListeners();
        this.loadInitialData();
        this.startStatusUpdates();
    }

    initializeEventListeners() {
        // Docker monitoring (now Podman-compatible)
        document.getElementById('start-docker-monitoring').addEventListener('click', () => {
            this.startDockerMonitoring();
        });

        // Stop monitoring
        document.getElementById('stop-monitoring').addEventListener('click', () => {
            this.stopMonitoring();
        });

        // Log refresh
        document.getElementById('refresh-logs').addEventListener('click', () => {
            this.refreshLogs();
        });

        // Architecture upload
        document.getElementById('upload-button').addEventListener('click', () => {
            document.getElementById('architecture-upload').click();
        });

        document.getElementById('architecture-upload').addEventListener('change', (e) => {
            this.handleFileUpload(e.target.files);
        });

        // Drag and drop for architecture upload
        const uploadArea = document.querySelector('.border-dashed');
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('border-blue-400', 'bg-blue-50');
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-blue-400', 'bg-blue-50');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-blue-400', 'bg-blue-50');
            this.handleFileUpload(e.dataTransfer.files);
        });
    }

    async loadInitialData() {
        await this.loadContainers();
        await this.refreshLogs();
    }

    async loadContainers() {
        try {
            const response = await fetch(`${this.apiBase}/containers`);
            const data = await response.json();
            
            const select = document.getElementById('docker-containers');
            select.innerHTML = '';
            
            if (data.success && data.containers.length > 0) {
                data.containers.forEach(container => {
                    const option = document.createElement('option');
                    option.value = container.name;
                    option.textContent = `${container.name} (${container.status})`;
                    select.appendChild(option);
                });
            } else {
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'No containers available';
                select.appendChild(option);
            }
        } catch (error) {
            console.error('Error loading containers:', error);
            this.showError('Failed to load containers');
        }
    }

    async startDockerMonitoring() {
        const select = document.getElementById('docker-containers');
        const selectedContainers = Array.from(select.selectedOptions).map(option => option.value);
        
        if (selectedContainers.length === 0) {
            this.showError('Please select at least one container');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/start-monitoring`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    type: 'docker',
                    targets: selectedContainers
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.monitoringActive = true;
                this.updateMonitoringUI();
                this.startLogRefresh();
                this.showSuccess('Monitoring started');
            } else {
                this.showError(data.error || 'Failed to start monitoring');
            }
        } catch (error) {
            console.error('Error starting monitoring:', error);
            this.showError('Failed to start monitoring');
        }
    }

    async stopMonitoring() {
        try {
            const response = await fetch(`${this.apiBase}/stop-monitoring`, {
                method: 'POST'
            });

            const data = await response.json();
            
            if (data.success) {
                this.monitoringActive = false;
                this.updateMonitoringUI();
                this.stopLogRefresh();
                this.showSuccess('Monitoring stopped');
            } else {
                this.showError(data.error || 'Failed to stop monitoring');
            }
        } catch (error) {
            console.error('Error stopping monitoring:', error);
            this.showError('Failed to stop monitoring');
        }
    }

    async refreshLogs() {
        try {
            const response = await fetch(`${this.apiBase}/logs?limit=50`);
            const data = await response.json();
            
            if (data.success) {
                this.updateLogsTable(data.logs);
                document.getElementById('log-count').textContent = data.total;
                
                // Update monitoring status
                if (data.monitoring_active !== this.monitoringActive) {
                    this.monitoringActive = data.monitoring_active;
                    this.updateMonitoringUI();
                }
            }
        } catch (error) {
            console.error('Error refreshing logs:', error);
        }
    }

    updateLogsTable(logs) {
        const tbody = document.getElementById('logs-table-body');
        
        if (logs.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                        <i class="fas fa-inbox text-4xl mb-4"></i>
                        <p>No logs available. Start monitoring to see log analysis.</p>
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = logs.map(log => {
            const typeClass = log.classification === 'ALERT' ? 'log-alert' : 'log-info';
            const typeIcon = log.classification === 'ALERT' ? 'fa-exclamation-triangle' : 'fa-info-circle';
            
            return `
                <tr class="fade-in">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ${this.formatTimestamp(log.timestamp)}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${typeClass}">
                            <i class="fas ${typeIcon} mr-1"></i>
                            ${log.classification}
                        </span>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-900 max-w-md">
                        <div class="truncate" title="${this.escapeHtml(log.log_message)}">
                            ${this.escapeHtml(log.log_message.substring(0, 100))}${log.log_message.length > 100 ? '...' : ''}
                        </div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-900 max-w-md">
                        <div class="truncate" title="${this.escapeHtml(log.analysis)}">
                            ${this.escapeHtml(log.analysis.substring(0, 100))}${log.analysis.length > 100 ? '...' : ''}
                        </div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-900 max-w-md">
                        ${log.resolution ? `
                            <div class="truncate" title="${this.escapeHtml(log.resolution)}">
                                ${this.escapeHtml(log.resolution.substring(0, 100))}${log.resolution.length > 100 ? '...' : ''}
                            </div>
                        ` : '<span class="text-gray-400">-</span>'}
                    </td>
                </tr>
            `;
        }).join('');
    }

    async handleFileUpload(files) {
        const uploadedFilesDiv = document.getElementById('uploaded-files');
        
        if (files.length === 0) return;
        
        // Create FormData for file upload
        const formData = new FormData();
        const validFiles = [];
        
        for (let file of files) {
            if (this.isValidFileType(file)) {
                formData.append('files', file);
                validFiles.push(file);
            } else {
                this.showError(`Invalid file type: ${file.name}`);
                return;
            }
        }
        
        if (validFiles.length === 0) return;
        
        // Show upload progress
        const progressDiv = document.createElement('div');
        progressDiv.className = 'flex items-center justify-between p-3 bg-blue-50 rounded-md mb-2';
        progressDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-spinner fa-spin text-blue-600 mr-2"></i>
                <span class="text-sm font-medium">Uploading ${validFiles.length} file(s)...</span>
            </div>
        `;
        uploadedFilesDiv.appendChild(progressDiv);
        
        try {
            const response = await fetch(`${this.apiBase}/upload-architecture`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            // Remove progress indicator
            progressDiv.remove();
            
            if (result.success) {
                // Show uploaded files
                result.files.forEach(fileInfo => {
                    const fileDiv = document.createElement('div');
                    fileDiv.className = 'flex items-center justify-between p-3 bg-gray-50 rounded-md mb-2';
                    fileDiv.innerHTML = `
                        <div class="flex items-center">
                            <i class="fas fa-file-alt text-blue-600 mr-2"></i>
                            <span class="text-sm font-medium">${fileInfo.filename}</span>
                            <span class="text-xs text-gray-500 ml-2">(${this.formatFileSize(fileInfo.size)})</span>
                        </div>
                        <div class="flex items-center">
                            <span class="text-xs ${fileInfo.processed ? 'text-green-600' : 'text-red-600'} mr-2">
                                <i class="fas ${fileInfo.processed ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i> 
                                ${fileInfo.processed ? 'Processed' : 'Error'}
                            </span>
                        </div>
                    `;
                    uploadedFilesDiv.appendChild(fileDiv);
                });
                
                this.showSuccess(`Successfully uploaded and processed ${validFiles.length} file(s)`);
                
                // Clear the file input
                document.getElementById('architecture-upload').value = '';
                
            } else {
                this.showError(result.error || 'Upload failed');
            }
            
        } catch (error) {
            // Remove progress indicator
            progressDiv.remove();
            console.error('Upload error:', error);
            this.showError('Upload failed: ' + error.message);
        }
    }

    async simulateFileProcessing(file) {
        // Simulate processing the architecture diagram
        const knowledge = `Architecture diagram uploaded: ${file.name}. This diagram shows the microservice architecture with components including API Gateway, Service Registry, Database, and Message Queue.`;
        
        try {
            await fetch(`${this.apiBase}/architecture-knowledge`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ knowledge })
            });
        } catch (error) {
            console.error('Error updating architecture knowledge:', error);
        }
    }

    isValidFileType(file) {
        const validTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg'];
        return validTypes.includes(file.type);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    updateMonitoringUI() {
        const stopButton = document.getElementById('stop-monitoring');
        const startDockerButton = document.getElementById('start-docker-monitoring');
        
        if (this.monitoringActive) {
            stopButton.disabled = false;
            startDockerButton.disabled = true;
        } else {
            stopButton.disabled = true;
            startDockerButton.disabled = false;
        }
    }

    startLogRefresh() {
        if (this.logRefreshInterval) {
            clearInterval(this.logRefreshInterval);
        }
        this.logRefreshInterval = setInterval(() => this.refreshLogs(), 1000);
    }

    stopLogRefresh() {
        if (this.logRefreshInterval) {
            clearInterval(this.logRefreshInterval);
            this.logRefreshInterval = null;
        }
    }

    startStatusUpdates() {
        setInterval(() => this.updateStatus(), 5000);
    }

    async updateStatus() {
        try {
            const response = await fetch(`${this.apiBase}/status`);
            const data = await response.json();
            
            if (data.success) {
                const statusIndicator = document.getElementById('status-indicator');
                const statusText = document.getElementById('status-text');
                
                if (data.monitoring_active) {
                    statusIndicator.className = 'w-3 h-3 rounded-full bg-green-500 mr-2';
                    statusText.textContent = 'Monitoring Active';
                } else {
                    statusIndicator.className = 'w-3 h-3 rounded-full bg-gray-400 mr-2';
                    statusText.textContent = 'Monitoring Inactive';
                }

                const knowledgeStatus = document.getElementById('knowledge-status');
                if (data.architecture_knowledge_available) {
                    knowledgeStatus.className = 'w-3 h-3 rounded-full bg-green-500 mr-2';
                    knowledgeStatus.nextElementSibling.textContent = 'Knowledge Available';
                } else {
                    knowledgeStatus.className = 'w-3 h-3 rounded-full bg-red-500 mr-2';
                    knowledgeStatus.nextElementSibling.textContent = 'No Knowledge';
                }

                const ollamaStatus = document.getElementById('ollama-status');
                if (data.ollama_connected) {
                    ollamaStatus.className = 'w-3 h-3 rounded-full bg-green-500 mr-2';
                    ollamaStatus.nextElementSibling.textContent = 'Ollama Connected';
                } else {
                    ollamaStatus.className = 'w-3 h-3 rounded-full bg-red-500 mr-2';
                    ollamaStatus.nextElementSibling.textContent = 'Ollama Disconnected';
                }

            } else {
                this.showError(data.error || 'Failed to fetch status');
            }
        } catch (error) {
            console.error('Error updating status:', error);
            this.showError('Failed to connect to backend');
        }
    }

    showSuccess(message) {
        const notification = document.getElementById('notification');
        notification.className = 'bg-green-500 text-white px-4 py-2 rounded-md mb-4';
        notification.textContent = message;
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 3000);
    }

    showError(message) {
        const notification = document.getElementById('notification');
        notification.className = 'bg-red-500 text-white px-4 py-2 rounded-md mb-4';
        notification.textContent = message;
        notification.style.display = 'block';
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ObservabilityDashboard();
});