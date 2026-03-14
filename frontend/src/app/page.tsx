"use client";

import { useState, useEffect } from "react";
import { Sparkles, Link as LinkIcon, Send, Twitter, Linkedin, MessageSquare, Loader2, Wand2 } from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";
import { PostCard } from "@/components/PostCard";
import { motion, AnimatePresence } from "framer-motion";

const platformOptions = [
  { id: "LinkedIn", icon: Linkedin, color: "text-[#0077b5]", desc: "Professional Network" },
  { id: "X/Twitter", icon: Twitter, color: "text-[#1DA1F2]", desc: "Micro-blogging" },
];

export default function HomePage() {
  const [topic, setTopic] = useState("");
  const [urls, setUrls] = useState("");
  const [platform, setPlatform] = useState<any>("LinkedIn");
  const [generating, setGenerating] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [posts, setPosts] = useState<{ content: string, scores?: any }[]>([]);
  const [ideas, setIdeas] = useState<any[]>([]);
  const [generatingIdeas, setGeneratingIdeas] = useState(false);
  const [trendingItems, setTrendingItems] = useState<any[]>([]);
  const [selectedTrendSource, setSelectedTrendSource] = useState("hacker_news");
  const [fetchingTrends, setFetchingTrends] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTrends = async () => {
      setFetchingTrends(true);
      try {
        const res = await api.getTrends(selectedTrendSource);
        setTrendingItems(res);
      } catch (e) { }
      setFetchingTrends(false);
    };
    fetchTrends();
  }, [selectedTrendSource]);

  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (jobId && jobStatus !== "completed" && jobStatus !== "failed") {
      interval = setInterval(async () => {
        try {
          const job = await api.getJob(jobId);
          setJobStatus(job.status);
          if (job.status === "completed") {
            const formattedPosts = (job.final_posts || []).map((p: string) => ({
              content: p,
              scores: job.scores
            }));
            setPosts(formattedPosts);
            setGenerating(false);
            clearInterval(interval);
          } else if (job.status === "failed") {
            setError(job.errors?.[0] || "Generation failed");
            setGenerating(false);
            clearInterval(interval);
          }
        } catch (err) {
          console.error("Polling error", err);
        }
      }, 2000);
    }

    return () => clearInterval(interval);
  }, [jobId, jobStatus]);

  const handleGenerate = async () => {
    if (!topic) return;
    setGenerating(true);
    setJobId(null);
    setJobStatus(null);
    setPosts([]);
    setError(null);

    try {
      const response = await api.generate({
        topic,
        urls: urls.split(",").map(u => u.trim()).filter(Boolean),
        platform,
        tone: "Professional",
        style: "Concise",
        num_posts: 3
      });
      setJobId(response.job_id);
      setJobStatus("queued");
    } catch (err: any) {
      setError(err.message || "Failed to start generation");
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-16 max-w-5xl mx-auto pb-32">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-6 pt-10"
      >
        <div className="inline-flex items-center gap-2 px-4 py-2 bg-brand-primary/10 rounded-full border border-brand-primary/20 backdrop-blur-md">
          <Sparkles className="w-4 h-4 text-brand-primary" />
          <span className="text-xs font-bold text-brand-primary uppercase tracking-widest">Powered by Advanced AI</span>
        </div>

        <h2 className="text-6xl md:text-7xl font-black tracking-tight leading-[1.1]">
          Impactful Content, <br />
          <span className="shimmer-text">Zero Effort.</span>
        </h2>

        <p className="text-xl text-foreground/50 max-w-2xl mx-auto font-medium">
          Create viral LinkedIn threads and high-engagement X posts in seconds from any topic or raw links.
        </p>
      </motion.div>

      {/* Trending Discovery Section (Phase 3) */}
      <div className="space-y-4 px-2">
        <div className="flex items-center justify-between">
          <h4 className="text-xs font-black uppercase tracking-[0.2em] text-foreground/40 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
            Live Discovery: Trending Now
          </h4>
          <div className="flex gap-2">
            {["hacker_news", "reddit_ai", "product_hunt"].map((s) => (
              <button
                key={s}
                onClick={() => setSelectedTrendSource(s)}
                className={cn(
                  "px-3 py-1 rounded-full text-[10px] font-bold border transition-all",
                  selectedTrendSource === s
                    ? "bg-brand-primary text-white border-brand-primary"
                    : "bg-surface-100 dark:bg-surface-900/50 border-white/5 text-foreground/40 hover:border-brand-primary/30"
                )}
              >
                {s.split("_").join(" ").toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide no-scrollbar">
          {fetchingTrends ? (
            Array(3).fill(0).map((_, i) => (
              <div key={i} className="min-w-[280px] h-[100px] bg-foreground/5 rounded-3xl animate-pulse" />
            ))
          ) : (
            trendingItems.map((item: any, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                onClick={() => {
                  setTopic(item.title);
                  setUrls(item.link);
                }}
                className="min-w-[300px] md:min-w-[350px] p-5 glass-panel rounded-3xl border-white/5 hover:border-brand-primary/30 cursor-pointer group hover:bg-brand-primary/[0.02] transition-all"
              >
                <div className="text-[10px] font-black text-brand-primary uppercase tracking-widest mb-1">{selectedTrendSource.replace("_", " ")}</div>
                <h5 className="font-bold text-sm text-foreground/80 line-clamp-2 group-hover:text-brand-primary transition-colors leading-tight">
                  {item.title}
                </h5>
              </motion.div>
            ))
          )}
        </div>
      </div>

      {/* Main Studio Area */}
      <motion.div
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
        className="glass-panel p-2 md:p-3 rounded-[2.5rem] border-white/10 shadow-2xl relative"
      >
        <div className="bg-surface-50 dark:bg-slate-900/50 rounded-[2rem] p-8 md:p-10 space-y-10">
          <div className="grid md:grid-cols-5 gap-10">
            {/* Input Side */}
            <div className="md:col-span-3 space-y-8">
              <div className="space-y-4">
                <label className="text-sm font-bold flex items-center gap-2 ml-1">
                  <span className="w-8 h-8 rounded-full bg-brand-primary/10 flex items-center justify-center text-brand-primary">1</span>
                  What's the topic?
                </label>
                <div className="relative group">
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-brand-primary to-brand-accent rounded-3xl blur opacity-0 group-focus-within:opacity-20 transition duration-500" />
                  <textarea
                    placeholder="e.g. The impact of Llama 3 on open-source AI..."
                    className="relative w-full bg-surface-100 dark:bg-surface-900/80 border-none rounded-3xl px-6 py-5 min-h-[160px] focus:ring-2 focus:ring-brand-primary/50 outline-none transition-all placeholder:text-foreground/20 text-lg font-medium leading-relaxed"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                  />
                  <button
                    onClick={async () => {
                      if (!topic) return;
                      setGeneratingIdeas(true);
                      try {
                        const res = await api.getIdeas(topic);
                        setIdeas(res);
                      } catch (e) { }
                      setGeneratingIdeas(false);
                    }}
                    className="absolute bottom-4 right-4 p-3 bg-brand-primary text-white rounded-2xl hover:shadow-lg transition-all active:scale-95 disabled:opacity-50"
                    title="Generate Ideas"
                    disabled={generatingIdeas || !topic}
                  >
                    {generatingIdeas ? <Loader2 className="w-5 h-5 animate-spin" /> : <Wand2 className="w-5 h-5" />}
                  </button>
                </div>

                {/* Ideas Display */}
                <AnimatePresence>
                  {ideas.length > 0 && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      className="grid grid-cols-1 gap-3 pt-2"
                    >
                      <div className="flex items-center justify-between px-2">
                        <span className="text-[10px] font-black uppercase tracking-widest text-brand-primary">Suggested Angles</span>
                        <button onClick={() => setIdeas([])} className="text-[10px] font-black uppercase tracking-widest text-foreground/20 hover:text-red-500">Clear</button>
                      </div>
                      {ideas.map((idea: any, i) => (
                        <div
                          key={i}
                          onClick={() => setTopic(`${idea.title}: ${idea.hook}`)}
                          className="p-4 bg-brand-primary/5 border border-brand-primary/10 rounded-2xl cursor-pointer hover:bg-brand-primary/10 transition-all group"
                        >
                          <div className="font-bold text-sm text-brand-primary group-hover:underline">{idea.title}</div>
                          <div className="text-xs text-foreground/50 line-clamp-1 italic">"{idea.hook}"</div>
                        </div>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <div className="space-y-4">
                <label className="text-sm font-bold flex items-center gap-2 ml-1">
                  <span className="w-8 h-8 rounded-full bg-brand-primary/10 flex items-center justify-center text-brand-primary">2</span>
                  Context URLs (Optional)
                </label>
                <div className="relative group">
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-brand-primary to-brand-accent rounded-2xl blur opacity-0 group-focus-within:opacity-20 transition duration-500" />
                  <div className="relative flex items-center">
                    <LinkIcon className="absolute left-5 w-5 h-5 text-foreground/20" />
                    <input
                      type="text"
                      placeholder="YouTube or article links..."
                      className="w-full bg-surface-100 dark:bg-surface-900/80 border-none rounded-2xl pl-14 pr-6 py-5 focus:ring-2 focus:ring-brand-primary/50 outline-none transition-all placeholder:text-foreground/20 font-medium"
                      value={urls}
                      onChange={(e) => setUrls(e.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Platform Selection Side */}
            <div className="md:col-span-2 space-y-8">
              <div className="space-y-4">
                <label className="text-sm font-bold flex items-center gap-2 ml-1">
                  <span className="w-8 h-8 rounded-full bg-brand-primary/10 flex items-center justify-center text-brand-primary">3</span>
                  Target Network
                </label>
                <div className="flex flex-col gap-3">
                  {platformOptions.map((opt) => (
                    <button
                      key={opt.id}
                      onClick={() => setPlatform(opt.id)}
                      className={cn(
                        "flex items-center gap-4 p-4 rounded-2xl transition-all duration-300 border-2 text-left group",
                        platform === opt.id
                          ? "bg-brand-primary/5 border-brand-primary ring-4 ring-brand-primary/5"
                          : "border-transparent bg-surface-100 dark:bg-surface-900/80 hover:bg-surface-200 dark:hover:bg-surface-900"
                      )}
                    >
                      <div className={cn(
                        "w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300",
                        platform === opt.id ? "bg-brand-primary text-white scale-110" : "bg-white dark:bg-surface-800 text-foreground/40 group-hover:scale-105"
                      )}>
                        <opt.icon className="w-6 h-6" />
                      </div>
                      <div>
                        <div className={cn("font-bold text-sm", platform === opt.id ? "text-brand-primary" : "text-foreground/70")}>{opt.id}</div>
                        <div className="text-[10px] text-foreground/30 font-bold uppercase tracking-wider">{opt.desc}</div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              <div className="pt-4">
                <button
                  onClick={handleGenerate}
                  disabled={generating || !topic}
                  className="w-full bg-gradient-to-br from-brand-primary to-brand-accent text-white py-6 rounded-[1.5rem] text-lg font-black hover:shadow-2xl hover:shadow-brand-primary/40 transition-all duration-300 flex items-center justify-center gap-3 active:scale-[0.97] disabled:opacity-50 disabled:grayscale group relative overflow-hidden"
                >
                  <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-500" />
                  {generating ? (
                    <>
                      <Loader2 className="w-6 h-6 animate-spin" />
                      <span>{jobStatus === "running" ? "Cooking Content..." : "Initializing..."}</span>
                    </>
                  ) : (
                    <>
                      <Wand2 className="w-6 h-6 group-hover:rotate-12 transition-transform" />
                      <span>Generate Magic</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 p-4 bg-red-500/10 text-red-500 rounded-2xl text-sm border border-red-500/20 font-bold text-center"
          >
            {error}
          </motion.div>
        )}
      </motion.div>

      {/* Results Section */}
      <AnimatePresence>
        {(posts.length > 0 || jobStatus === "running") && (
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="space-y-10"
          >
            <div className="flex items-center justify-between border-b border-foreground/5 pb-6">
              <h3 className="text-3xl font-black flex items-center gap-3">
                <Sparkles className="text-brand-primary w-8 h-8" />
                Your Viral Variations
              </h3>
              <div className="px-4 py-1.5 bg-brand-primary/10 text-brand-primary rounded-full text-xs font-black uppercase tracking-widest">
                {posts.length} Finished
              </div>
            </div>

            <div className="grid gap-8">
              {posts.map((post, i) => (
                <PostCard key={i} index={i} content={post.content} scores={post.scores} platform={platform} jobId={jobId || undefined} />
              ))}
              {jobStatus === "running" && posts.length === 0 && (
                <div className="flex flex-col items-center justify-center py-20 animate-pulse text-foreground/20">
                  <Loader2 className="w-12 h-12 animate-spin mb-4" />
                  <p className="font-bold uppercase tracking-widest text-sm text-foreground/30">AI is crafting the perfect posts...</p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
