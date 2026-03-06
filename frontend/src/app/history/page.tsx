"use client";

import { useState, useEffect } from "react";
import { History as HistoryIcon, Search, Calendar, Twitter, Linkedin, ChevronRight, Inbox, Sparkles, Loader2 } from "lucide-react";
import { supabase } from "@/lib/supabase";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { motion } from "framer-motion";

export default function HistoryPage() {
    const [jobs, setJobs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");

    useEffect(() => {
        async function loadHistory() {
            try {
                const { data, error } = await supabase
                    .from("jobs")
                    .select("*")
                    .order("created_at", { ascending: false });

                if (error) throw error;
                setJobs(data || []);
            } catch (err) {
                console.error("Failed to load history", err);
            } finally {
                setLoading(false);
            }
        }
        loadHistory();
    }, []);

    const filteredJobs = jobs.filter(job =>
        job.topic?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.platform?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="space-y-12 max-w-5xl mx-auto pb-32">
            {/* Header Area */}
            <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-foreground/5 pb-10 pt-10"
            >
                <div className="space-y-4">
                    <div className="inline-flex items-center gap-2 px-3 py-1 bg-brand-primary/10 rounded-full border border-brand-primary/20">
                        <HistoryIcon className="w-4 h-4 text-brand-primary" />
                        <span className="text-[10px] font-black uppercase tracking-widest text-brand-primary">Archive Studio</span>
                    </div>
                    <h2 className="text-5xl font-black tracking-tighter">Your Creations</h2>
                    <p className="text-lg text-foreground/40 font-medium">Manage and revisit your previously generated viral content.</p>
                </div>

                <div className="relative group">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground/20 group-focus-within:text-brand-primary transition-colors" />
                    <input
                        type="text"
                        placeholder="Search campaigns..."
                        className="bg-surface-100 dark:bg-surface-900/50 border-none rounded-2xl pl-12 pr-6 py-4 outline-none focus:ring-2 focus:ring-brand-primary/50 transition-all font-medium min-w-[300px]"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                    />
                </div>
            </motion.div>

            {/* History List */}
            <div className="grid gap-6">
                {loading ? (
                    Array(3).fill(0).map((_, i) => (
                        <div key={i} className="glass-panel h-32 rounded-3xl animate-pulse bg-surface-100/50" />
                    ))
                ) : filteredJobs.length > 0 ? (
                    filteredJobs.map((job, i) => (
                        <motion.div
                            key={job.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            className="glass-panel p-6 rounded-[2rem] hover:shadow-2xl hover:shadow-brand-primary/5 transition-all duration-500 group cursor-pointer border-white/5"
                        >
                            <div className="flex items-center gap-6">
                                <div className="w-16 h-16 rounded-2xl bg-surface-100 dark:bg-surface-900 flex flex-col items-center justify-center border border-white/5 relative overflow-hidden group-hover:scale-105 transition-transform">
                                    <div className="absolute inset-0 bg-brand-primary/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                                    {job.platform === "LinkedIn" ? <Linkedin className="w-6 h-6 text-brand-secondary" /> : <Twitter className="w-6 h-6 text-brand-primary" />}
                                </div>

                                <div className="flex-1 space-y-1">
                                    <h4 className="font-bold text-lg line-clamp-1">{job.topic || "Untitled Campaign"}</h4>
                                    <div className="flex items-center gap-4 text-xs font-bold text-foreground/30 uppercase tracking-widest">
                                        <span className="flex items-center gap-1.5"><Calendar className="w-3.5 h-3.5" /> {new Date(job.created_at).toLocaleDateString()}</span>
                                        <span className="w-1.5 h-1.5 rounded-full bg-foreground/10" />
                                        <span className="text-brand-primary">{job.platform}</span>
                                    </div>
                                </div>

                                <div className="flex items-center gap-4">
                                    <div className="text-right hidden md:block">
                                        <div className="text-xs font-black uppercase tracking-widest text-foreground/20">Status</div>
                                        <div className={cn(
                                            "font-black text-sm uppercase",
                                            job.status === "completed" ? "text-green-500" : "text-brand-primary animate-pulse"
                                        )}>
                                            {job.status === "completed" ? "Optimized" : "Generating"}
                                        </div>
                                    </div>
                                    <div className="w-12 h-12 rounded-full border border-foreground/5 flex items-center justify-center group-hover:bg-brand-primary group-hover:text-white transition-all duration-300">
                                        <ChevronRight className="w-5 h-5 group-hover:translate-x-0.5 transition-transform" />
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))
                ) : (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="py-32 flex flex-col items-center justify-center text-center space-y-6"
                    >
                        <div className="w-24 h-24 rounded-[2rem] bg-surface-100 dark:bg-surface-900 flex items-center justify-center">
                            <Inbox className="w-10 h-10 text-foreground/10" />
                        </div>
                        <div className="space-y-2">
                            <h3 className="text-2xl font-black uppercase tracking-tighter">
                                {searchQuery ? "No Matches" : "Archive Empty"}
                            </h3>
                            <p className="text-foreground/30 font-bold max-w-xs uppercase tracking-widest text-[10px]">
                                {searchQuery ? "Try searching for another keyword." : "Start your first campaign to see your history here."}
                            </p>
                        </div>
                        {!searchQuery && (
                            <Link href="/" className="inline-flex items-center gap-2 px-6 py-3 bg-brand-primary text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:shadow-xl hover:shadow-brand-primary/20 transition-all active:scale-95">
                                <Sparkles className="w-4 h-4" />
                                Create Magic
                            </Link>
                        )}
                    </motion.div>
                )}
            </div>
        </div>
    );
}
