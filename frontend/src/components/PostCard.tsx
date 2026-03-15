"use client";

import { Linkedin, Twitter, Copy, Check, Download, Heart, MessageCircle, Repeat2, Bookmark } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface PostCardProps {
    content: string;
    platform: "LinkedIn" | "X/Twitter";
    index: number;
    jobId?: string;
    criticFeedback?: string;
}

export function PostCard({ content, platform, index, criticFeedback, jobId }: PostCardProps) {
    const [copied, setCopied] = useState(false);
    const [localContent, setLocalContent] = useState(content);
    const isTwitter = platform === "X/Twitter";

    const handleDownload = () => {
        const element = document.createElement("a");
        const file = new Blob([localContent], {type: 'text/plain'});
        element.href = URL.createObjectURL(file);
        element.download = `pratibimbai-post-${index + 1}.txt`;
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

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
                        <button
                            onClick={handleDownload}
                            className="p-3 bg-surface-100 dark:bg-surface-900/50 hover:bg-brand-primary hover:text-white rounded-xl transition-all duration-300 text-foreground/40 active:scale-90"
                            title="Download Content"
                        >
                            <Download className="w-5 h-5" />
                        </button>
                        <button
                            onClick={handleCopy}
                            className="px-4 py-2.5 bg-brand-primary text-white hover:opacity-90 rounded-xl transition-all duration-300 active:scale-90 flex items-center gap-2 font-bold text-sm"
                            title="Copy Content"
                        >
                            {copied ? <><Check className="w-4 h-4" /> Copied</> : <><Copy className="w-4 h-4" /> Copy</>}
                        </button>
                    </div>
                </div>

                {/* Performance metrics removed in favor of simpler text feedback */}

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

                {criticFeedback && (
                    <div className="p-4 bg-brand-primary/10 border border-brand-primary/20 rounded-xl">
                        <div className="text-[10px] font-black uppercase tracking-widest text-brand-primary flex items-center gap-1.5 mb-1.5">
                            <span className="animate-pulse">✨</span> AI Suggestion
                        </div>
                        <div className="text-sm font-medium text-foreground/80 leading-relaxed">
                            {criticFeedback}
                        </div>
                    </div>
                )}

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
