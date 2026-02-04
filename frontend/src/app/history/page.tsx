"use client";

import { useState, useEffect } from "react";
import { History as HistoryIcon, Search, Calendar, Twitter, Linkedin, ChevronRight, Inbox, Sparkles } from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { motion } from "framer-motion";

export default function HistoryPage() {
    const [jobs, setJobs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadHistory() {
            try {
                const response = await api.getProfile(); // Assuming profile or a separate history endpoint returns jobs
                // If history is not in profile, we might need a dedicated endpoint
                // For now, let's keep it simple or assume we'll add it
            } catch (err) {
                console.error("Failed to load history", err);
            } finally {
                setLoading(false);
            }
        }
                                        <span className="capitalize">{job.platform}</span>
                                        <span>•</span>
                                        <span className={cn(
                                            "font-medium",
                                            job.status === "completed" ? "text-green-500" :
                                                job.status === "failed" ? "text-red-500" : "text-brand-primary"
                                        )}>
                                            {job.status}
                                        </span>
                                    </div >
                                </div >
                            </div >

            <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button className="p-2 hover:bg-surface-200 rounded-lg text-foreground/40 group-hover:text-foreground">
                    <ExternalLink className="w-5 h-5" />
                </button>
                <button className="p-2 hover:bg-red-50 rounded-lg text-foreground/40 hover:text-red-500">
                    <Trash2 className="w-5 h-5" />
                </button>
            </div>
                        </div >
                    ))
                )
}
            </div >
        </div >
    );
}
