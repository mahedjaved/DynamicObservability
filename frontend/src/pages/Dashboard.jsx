import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Activity, Server, Play, Terminal } from "lucide-react";
import { motion } from "framer-motion";

export default function Dashboard() {
    const [orchestrations, setOrchestrations] = useState([]);
    const [logs, setLogs] = useState(["Waiting for logs..."]);
    const [containers, setContainers] = useState([]);

    useEffect(() => {
        // Fetch available orchestrations
        fetch('/api/orchestrate')
            .then(res => res.json())
            .then(data => setOrchestrations(data))
            .catch(err => console.error("Failed to fetch orchestrations", err));

        // Fetch containers (mock/real)
        const interval = setInterval(() => {
            fetch('/api/containers')
                .then(res => res.json())
                .then(data => setContainers(data))
                .catch(err => console.error(err));
        }, 5000);

        return () => clearInterval(interval);
    }, []);

    const triggerOrchestration = (orch) => {
        console.log("Triggering:", orch);
        // In real app, we'd map the name to an endpoint or ID
        fetch('/api/orchestrate/web-stack', { method: 'POST' })
            .then(res => res.text())
            .then(msg => setLogs(prev => [`[SYSTEM] ${msg}`, ...prev]));
    };

    return (
        <div className="min-h-screen bg-background text-foreground p-8 font-sans">
            <header className="mb-10 flex items-center justify-between">
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="flex items-center gap-2"
                >
                    <Activity className="h-8 w-8 text-primary" />
                    <h1 className="text-3xl font-bold tracking-tight">DynObs Orchestrator</h1>
                </motion.div>
                <div className="flex gap-4">
                    <Button variant="outline">Docs</Button>
                    <Button>Settings</Button>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                {/* Orchestration Panel */}
                <Card className="col-span-1 border-primary/20 bg-card/50 backdrop-blur">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Server className="h-5 w-5 text-blue-500" />
                            Orchestration
                        </CardTitle>
                        <CardDescription>Deploy stacks with one click</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {orchestrations.length === 0 && <p className="text-sm text-muted-foreground">Loading actions...</p>}
                        {orchestrations.map((orch, idx) => (
                            <motion.div
                                key={idx}
                                whileHover={{ scale: 1.02 }}
                                className="p-4 border rounded-lg bg-background/50 flex items-center justify-between group"
                            >
                                <span className="font-medium text-sm">{orch}</span>
                                <Button size="sm" onClick={() => triggerOrchestration(orch)}>
                                    <Play className="h-4 w-4 mr-2" /> Deploy
                                </Button>
                            </motion.div>
                        ))}
                    </CardContent>
                </Card>

                {/* Active Containers */}
                <Card className="col-span-1 border-primary/20 bg-card/50 backdrop-blur">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Activity className="h-5 w-5 text-green-500" />
                            Active Containers
                        </CardTitle>
                        <CardDescription>Real-time status</CardDescription>
                    </CardHeader>
                    <CardContent>
                        {containers.length === 0 ? (
                            <div className="text-center py-8 text-muted-foreground">
                                No containers running
                            </div>
                        ) : (
                            <ul className="space-y-2">
                                {containers.map((c, i) => (
                                    <li key={i} className="flex items-center gap-2 text-sm">
                                        <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                                        {c}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </CardContent>
                </Card>

                {/* Live Logs */}
                <Card className="col-span-1 md:col-span-2 lg:col-span-3 border-primary/10 bg-black/90 text-green-400 font-mono text-sm">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-gray-400 text-base">
                            <Terminal className="h-4 w-4" />
                            System Logs
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="h-64 overflow-y-auto space-y-1 p-4 pt-0">
                        {logs.map((log, i) => (
                            <div key={i} className="break-all border-l-2 border-transparent hover:border-green-500 pl-2 transition-colors">
                                <span className="opacity-50 mr-2">[{new Date().toLocaleTimeString()}]</span>
                                {log}
                            </div>
                        ))}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
