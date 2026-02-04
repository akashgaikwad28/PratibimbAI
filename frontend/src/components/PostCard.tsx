"use client";

import { Linkedin, Twitter, Copy, Check, Share2, Heart, MessageCircle, Repeat2, Bookmark } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";

interface PostCardProps {
    content: string;
    platform: "LinkedIn" | "X/Twitter";
    index: number;
}

export function PostCard({ content, platform, index }: PostCardProps) {
    const [copied, setCopied] = useState(false);
    const isTwitter = platform === "X/Twitter";

    const handleCopy = () => {
        navigator.clipboard.writeText(content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
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
                            onClick={handleCopy}
                            className="p-3 bg-surface-100 dark:bg-surface-900/50 hover:bg-brand-primary hover:text-white rounded-xl transition-all duration-300 text-foreground/40 active:scale-90"
                            title="Copy Content"
                        >
                            {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                        </button>
                    </div>
                </div>

                {/* Content Body */}
                <div className={cn(
                    "bg-surface-50 dark:bg-surface-900/30 p-6 rounded-2xl border border-foreground/5",
                    "text-[17px] leading-relaxed whitespace-pre-wrap text-foreground/80 font-medium selection:bg-brand-primary/20",
                    isTwitter ? "font-sans" : "font-sans leading-relaxed"
                )}>
                    {content}
                </div>

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
