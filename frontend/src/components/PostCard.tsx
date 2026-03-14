"use client";

import { Linkedin, Twitter, Copy, Check, Share2, Heart, MessageCircle, Repeat2, Bookmark } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface PostCardProps {
    content: string;
    platform: "LinkedIn" | "X/Twitter";
    index: number;
    jobId?: string;
    scores?: {
        clarity: number;
        virality: number;
        hook: number;
        authority: number;
    };
}

export function PostCard({ content, platform, index, scores, jobId }: PostCardProps) {
    const [copied, setCopied] = useState(false);
    const [localContent, setLocalContent] = useState(content);
    const isTwitter = platform === "X/Twitter";

    const avgScore = scores ? (Object.values(scores).reduce((a, b) => a + b, 0) / 4).toFixed(1) : null;

    const handleCopy = async () => {
        navigator.clipboard.writeText(localContent);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);

        // Phase 2: Live Learning (Save edited post to memory)
        if (jobId) {
            try {
                const { api } = await import("@/lib/api");
                await api.finalizeJob({
                    job_id: jobId,
                    content: localContent,
                    platform: platform
                });
            } catch (e) {
                console.error("Failed to store memory", e);
            }
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass-panel rounded-[2rem] overflow-hidden border-white/10 shadow-xl group hover:shadow-2xl hover:shadow-brand-primary/10 transition-all duration-500"
        >
            <div className="p-8 flex flex-col gap-6">
                {/* Header */}
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-surface-200 to-surface-100 dark:from-surface-800 dark:to-surface-900 flex items-center justify-center font-black text-brand-primary text-xl border border-white/10 shadow-inner">
                            PA
                        </div>
                        <div>
                            <div className="font-bold flex items-center gap-1.5 text-lg">
                                PratibimbAI <span className="text-foreground/30 font-medium">Studio</span>
                                <div className="w-4 h-4 bg-brand-primary rounded-full flex items-center justify-center ml-0.5">
                                    <Check className="text-white w-2.5 h-2.5 bold" />
                                </div>
                            </div>
                            <div className="text-xs text-foreground/30 font-bold uppercase tracking-widest flex items-center gap-2">
                                Draft Variation #{index + 1}
                                <span className="w-1 h-1 rounded-full bg-foreground/20" />
                                Just Now
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        {avgScore && (
                            <div className="flex items-center gap-2 px-3 py-1.5 bg-brand-primary/10 rounded-xl border border-brand-primary/20">
                                <span className="text-[10px] font-black text-brand-primary">AI SCORE</span>
                                <span className="text-sm font-black text-brand-primary">{avgScore}</span>
                            </div>
                        )}
                        <button
                            onClick={handleCopy}
                            className="p-3 bg-surface-100 dark:bg-surface-900/50 hover:bg-brand-primary hover:text-white rounded-xl transition-all duration-300 text-foreground/40 active:scale-90"
                            title="Copy Content"
                        >
                            {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                        </button>
                    </div>
                </div>

                {/* Performance Metrics (Pro Layer) */}
                {scores && (
                    <div className="grid grid-cols-4 gap-4 py-2 px-4 bg-surface-100 dark:bg-surface-900/30 rounded-2xl border border-white/5">
                        {[
                            { label: "Clarity", val: scores.clarity },
                            { label: "Hook", val: scores.hook },
                            { label: "Authority", val: scores.authority },
                            { label: "Virality", val: scores.virality },
                        ].map((s) => (
                            <div key={s.label} className="flex flex-col gap-1">
                                <div className="flex justify-between items-end">
                                    <span className="text-[8px] font-black uppercase tracking-wider text-foreground/30">{s.label}</span>
                                    <span className="text-[10px] font-black text-brand-primary">{s.val}</span>
                                </div>
                                <div className="h-1 w-full bg-foreground/5 rounded-full overflow-hidden">
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${s.val * 10}%` }}
                                        className="h-full bg-brand-primary/40 rounded-full"
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {/* Content Body */}
                <div className="relative group/edit">
                    <textarea
                        value={localContent}
                        onChange={(e) => setLocalContent(e.target.value)}
                        className={cn(
                            "w-full bg-surface-50 dark:bg-surface-900/30 p-6 rounded-2xl border border-foreground/5",
                            "text-[16px] leading-relaxed whitespace-pre-wrap text-foreground/80 font-medium outline-none focus:ring-2 focus:ring-brand-primary/20 transition-all resize-none min-h-[200px]",
                            isTwitter ? "font-sans" : "font-sans leading-relaxed"
                        )}
                        spellCheck={false}
                    />
                    <div className="absolute top-2 right-2 opacity-0 group-hover/edit:opacity-100 transition-opacity pointer-events-none">
                        <span className="text-[9px] font-black text-brand-primary bg-brand-primary/10 px-2 py-1 rounded-md border border-brand-primary/20 uppercase tracking-tighter">
                            Editable
                        </span>
                    </div>
                </div>

                {copied && (
                    <motion.div
                        initial={{ opacity: 0, y: 5 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-[10px] font-bold text-center text-brand-primary"
                    >
                        ✓ Copied to clipboard & saved to AI Memory Layer
                    </motion.div>
                )}

                {/* Action Bar (Fake but realistic) */}
                <div className="pt-2 flex items-center justify-between border-t border-foreground/5">
                    <div className="flex items-center gap-6 md:gap-8 text-foreground/30">
                        <div className="flex items-center gap-2 hover:text-brand-primary cursor-pointer transition-colors group/icon">
                            <MessageCircle className="w-5 h-5 group-hover/icon:scale-110 transition-transform" />
                            <span className="text-xs font-bold">24</span>
                        </div>
                        <div className="flex items-center gap-2 hover:text-green-500 cursor-pointer transition-colors group/icon">
                            <Repeat2 className="w-5 h-5 group-hover/icon:scale-110 transition-transform" />
                            <span className="text-xs font-bold">12</span>
                        </div>
                        <div className="flex items-center gap-2 hover:text-red-500 cursor-pointer transition-colors group/icon">
                            <Heart className="w-5 h-5 group-hover/icon:scale-110 transition-transform" />
                            <span className="text-xs font-bold">148</span>
                        </div>
                    </div>

                    <div className="flex items-center gap-2 px-4 py-2 bg-foreground/5 rounded-xl border border-transparent group-hover:border-brand-primary/20 transition-all">
                        {isTwitter ? (
                            <Twitter className="w-4 h-4 text-[#1DA1F2]" />
                        ) : (
                            <Linkedin className="w-4 h-4 text-[#0077b5]" />
                        )}
                        <span className="text-[10px] font-black uppercase tracking-widest text-foreground/40">{platform} Feed</span>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
