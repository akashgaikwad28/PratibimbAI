"use client";

import { useState, useEffect } from "react";
import { Globe, Plus, Trash2, Edit2, CheckCircle2, XCircle, Clock, Link as LinkIcon, Youtube, RefreshCcw, Loader2 } from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";

export default function SourcesPage() {
    const [sources, setSources] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [newSource, setNewSource] = useState({ url: "", source_type: "website", poll_interval_hours: 6 });
    const [submitting, setSubmitting] = useState(false);

    useEffect(() => {
        loadSources();
    }, []);

    async function loadSources() {
        try {
            const data = await api.getSources();
            setSources(data);
        } catch (err) {
            console.error("Failed to load sources", err);
        } finally {
            setLoading(false);
        }
    }

    async function handleAddSource() {
        if (!newSource.url) return;
        setSubmitting(true);
        try {
            await api.addSource(newSource);
            setIsAddModalOpen(false);
            setNewSource({ url: "", source_type: "website", poll_interval_hours: 6 });
            loadSources();
        } catch (err) {
            console.error("Failed to add source", err);
        } finally {
            setSubmitting(false);
        }
    }

    async function toggleActive(id: string, current: boolean) {
        try {
            await api.updateSource(id, { is_active: !current });
            loadSources();
        } catch (err) {
            console.error("Failed to toggle source", err);
        }
    }

    async function handleDelete(id: string) {
        if (!confirm("Are you sure you want to remove this source?")) return;
        try {
            await api.deleteSource(id);
            loadSources();
        } catch (err) {
            console.error("Failed to delete source", err);
        }
    }

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
                        <Globe className="w-4 h-4 text-brand-primary" />
                        <span className="text-[10px] font-black uppercase tracking-widest text-brand-primary">Automation Hub</span>
                    </div>
                    <h2 className="text-5xl font-black tracking-tighter">Monitored Sources</h2>
                    <p className="text-lg text-foreground/40 font-medium">PratibimbAI watches these URLs and updates you when new content arrives.</p>
                </div>

                <button
                    onClick={() => setIsAddModalOpen(true)}
                    className="flex items-center gap-2 px-6 py-4 bg-brand-primary text-white rounded-2xl font-black uppercase tracking-widest text-xs hover:shadow-2xl hover:shadow-brand-primary/20 transition-all active:scale-95 group"
                >
                    <Plus className="w-5 h-5 group-hover:rotate-90 transition-transform" />
                    Connect New Source
                </button>
            </motion.div>

            {/* Sources List */}
            <div className="grid gap-6">
                {loading ? (
                    Array(2).fill(0).map((_, i) => (
                        <div key={i} className="glass-panel h-28 rounded-3xl animate-pulse bg-surface-100/50" />
                    ))
                ) : sources.length > 0 ? (
                    sources.map((source, i) => (
                        <motion.div
                            key={source.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            className={cn(
                                "glass-panel p-6 rounded-[2rem] border-white/5 flex items-center gap-6 group transition-all duration-500",
                                !source.is_active && "opacity-60 grayscale-[0.5]"
                            )}
                        >
                            <div className="w-16 h-16 rounded-2xl bg-surface-100 dark:bg-surface-900 flex items-center justify-center border border-white/5 shadow-inner">
                                {source.source_type === 'youtube' ? <Youtube className="w-7 h-7 text-red-500" /> : <Globe className="w-7 h-7 text-brand-primary" />}
                            </div>

                            <div className="flex-1 space-y-1">
                                <div className="flex items-center gap-3">
                                    <h4 className="font-bold text-lg line-clamp-1 truncate max-w-md">{source.url}</h4>
                                    {source.is_active ?
                                        <span className="px-2 py-0.5 rounded-full bg-green-500/10 text-green-500 text-[10px] font-black uppercase tracking-widest border border-green-500/20">Active</span> :
                                        <span className="px-2 py-0.5 rounded-full bg-foreground/10 text-foreground/40 text-[10px] font-black uppercase tracking-widest border border-foreground/5">Paused</span>
                                    }
                                </div>
                                <div className="flex items-center gap-4 text-xs font-bold text-foreground/30 uppercase tracking-widest">
                                    <span className="flex items-center gap-1.5"><Clock className="w-3.5 h-3.5" /> Every {source.poll_interval_hours}h</span>
                                    <span className="w-1.5 h-1.5 rounded-full bg-foreground/10" />
                                    <span>Last Polled: {source.last_polled_at ? new Date(source.last_polled_at).toLocaleTimeString() : 'Never'}</span>
                                </div>
                            </div>

                            <div className="flex items-center gap-3">
                                <button
                                    onClick={() => toggleActive(source.id, source.is_active)}
                                    className={cn(
                                        "p-3 rounded-xl transition-all border border-transparent",
                                        source.is_active ? "text-green-500 hover:bg-green-500/10" : "text-foreground/20 hover:text-foreground hover:bg-surface-100"
                                    )}
                                >
                                    <RefreshCcw className={cn("w-5 h-5", source.is_active && "animate-spin-slow")} />
                                </button>
                                <button
                                    onClick={() => handleDelete(source.id)}
                                    className="p-3 rounded-xl text-foreground/20 hover:text-red-500 hover:bg-red-500/10 transition-all border border-transparent"
                                >
                                    <Trash2 className="w-5 h-5" />
                                </button>
                            </div>
                        </motion.div>
                    ))
                ) : (
                    <div className="py-24 text-center glass-panel rounded-[3rem] border-dashed border-2 border-foreground/5">
                        <div className="flex flex-col items-center gap-4 opacity-30">
                            <Globe className="w-12 h-12" />
                            <div>
                                <h3 className="text-xl font-black uppercase tracking-tighter">No Monitored Sources</h3>
                                <p className="text-xs font-bold uppercase tracking-widest">Add your first URL to start automated tracking.</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Add Modal */}
            <AnimatePresence>
                {isAddModalOpen && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-background/80 backdrop-blur-sm">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.9, y: 20 }}
                            className="glass-panel w-full max-w-lg p-8 rounded-[3rem] shadow-2xl border-white/10"
                        >
                            <div className="space-y-6">
                                <div className="space-y-2">
                                    <h3 className="text-3xl font-black tracking-tighter">Connect Source</h3>
                                    <p className="text-sm text-foreground/40 font-medium tracking-tight">Paste a website URL or YouTube channel link to monitor.</p>
                                </div>

                                <div className="space-y-4">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black uppercase tracking-widest text-foreground/40 ml-1">Source URL</label>
                                        <div className="relative group">
                                            <LinkIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground/20 group-focus-within:text-brand-primary transition-colors" />
                                            <input
                                                type="text"
                                                placeholder="https://example.com/blog"
                                                className="w-full bg-surface-100 dark:bg-surface-900 border-none rounded-2xl pl-12 pr-6 py-4 outline-none focus:ring-2 focus:ring-brand-primary/50 transition-all font-medium"
                                                value={newSource.url}
                                                onChange={(e) => setNewSource({ ...newSource, url: e.target.value })}
                                            />
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-black uppercase tracking-widest text-foreground/40 ml-1">Type</label>
                                            <select
                                                className="w-full bg-surface-100 dark:bg-surface-900 border-none rounded-2xl px-6 py-4 outline-none focus:ring-2 focus:ring-brand-primary/50 transition-all font-medium appearance-none"
                                                value={newSource.source_type}
                                                onChange={(e) => setNewSource({ ...newSource, source_type: e.target.value })}
                                            >
                                                <option value="website">Website/Blog</option>
                                                <option value="youtube">YouTube</option>
                                            </select>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-[10px] font-black uppercase tracking-widest text-foreground/40 ml-1">Polling Interval</label>
                                            <select
                                                className="w-full bg-surface-100 dark:bg-surface-900 border-none rounded-2xl px-6 py-4 outline-none focus:ring-2 focus:ring-brand-primary/50 transition-all font-medium appearance-none"
                                                value={newSource.poll_interval_hours}
                                                onChange={(e) => setNewSource({ ...newSource, poll_interval_hours: parseInt(e.target.value) })}
                                            >
                                                <option value={1}>1 Hour</option>
                                                <option value={6}>6 Hours</option>
                                                <option value={12}>12 Hours</option>
                                                <option value={24}>24 Hours</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                <div className="flex gap-3 pt-4">
                                    <button
                                        onClick={() => setIsAddModalOpen(false)}
                                        className="flex-1 px-6 py-4 rounded-2xl font-black uppercase tracking-widest text-xs border border-foreground/5 hover:bg-surface-100 transition-all"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        onClick={handleAddSource}
                                        disabled={submitting || !newSource.url}
                                        className="flex-1 px-6 py-4 bg-brand-primary text-white rounded-2xl font-black uppercase tracking-widest text-xs hover:shadow-xl hover:shadow-brand-primary/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                                    >
                                        {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                                        Start Tracking
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
}
