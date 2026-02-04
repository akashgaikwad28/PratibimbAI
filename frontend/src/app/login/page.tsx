"use client";

import { useState } from "react";
import { supabase } from "@/lib/supabase";
import { Sparkles, Mail, Lock, LogIn, Github, Chrome, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useRouter } from "next/navigation";

export default function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [isSignUp, setIsSignUp] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const router = useRouter();

    const handleAuth = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            if (isSignUp) {
                const { error } = await supabase.auth.signUp({
                    email,
                    password,
                    options: {
                        data: {
                            full_name: email.split("@")[0],
                        }
                    }
                });
                if (error) throw error;
                alert("Check your email for confirmation!");
            } else {
                const { error } = await supabase.auth.signInWithPassword({
                    email,
                    password,
                });
                if (error) throw error;
                router.push("/");
            }
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = async () => {
        await supabase.auth.signInWithOAuth({
            provider: "google",
            options: {
                redirectTo: window.location.origin
            }
        });
    };

    return (
        <div className="min-h-screen bg-background flex items-center justify-center p-6 relative overflow-hidden">
            {/* Background Decor */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-[-20%] left-[-10%] w-[60%] h-[60%] bg-brand-primary/10 rounded-full blur-[160px] animate-pulse" />
                <div className="absolute bottom-[-20%] right-[-10%] w-[60%] h-[60%] bg-brand-accent/10 rounded-full blur-[160px] animate-pulse" style={{ animationDelay: '2s' }} />
            </div>

            <div className="w-full max-w-md relative z-10">
                <div className="text-center space-y-6 mb-10">
                    <div className="inline-flex items-center justify-center p-4 bg-gradient-to-br from-brand-primary to-brand-accent rounded-[1.5rem] shadow-xl shadow-brand-primary/20 rotate-3">
                        <Sparkles className="w-10 h-10 text-white" />
                    </div>
                    <div className="space-y-2">
                        <h1 className="text-5xl font-black tracking-tighter">PratibimbAI</h1>
                        <p className="text-lg text-foreground/40 font-bold uppercase tracking-widest text-[11px]">Personal Content Studio</p>
                    </div>
                </div>

                <div className="glass-panel p-2 rounded-[2.5rem] border-white/10 shadow-2xl">
                    <div className="bg-surface-50 dark:bg-slate-900/50 rounded-[2rem] p-10">
                        <form onSubmit={handleAuth} className="space-y-6">
                            <div className="space-y-3">
                                <label className="text-xs font-black uppercase tracking-widest text-foreground/40 ml-1">Email Connection</label>
                                <div className="relative group">
                                    <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground/20 group-focus-within:text-brand-primary transition-colors" />
                                    <input
                                        type="email"
                                        required
                                        placeholder="you@presence.ai"
                                        className="w-full bg-surface-100 dark:bg-surface-900/80 border-none rounded-2xl pl-12 pr-4 py-4 focus:ring-2 focus:ring-brand-primary/50 outline-none transition-all font-medium"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                    />
                                </div>
                            </div>

                            <div className="space-y-3">
                                <label className="text-xs font-black uppercase tracking-widest text-foreground/40 ml-1">Secret Access</label>
                                <div className="relative group">
                                    <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-foreground/20 group-focus-within:text-brand-primary transition-colors" />
                                    <input
                                        type="password"
                                        required
                                        placeholder="••••••••"
                                        className="w-full bg-surface-100 dark:bg-surface-900/80 border-none rounded-2xl pl-12 pr-4 py-4 focus:ring-2 focus:ring-brand-primary/50 outline-none transition-all font-medium"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                </div>
                            </div>

                            <button
                                disabled={loading}
                                className="w-full bg-gradient-to-br from-brand-primary to-brand-accent text-white py-4 rounded-2xl font-black text-lg hover:shadow-xl hover:shadow-brand-primary/30 transition-all duration-300 flex items-center justify-center gap-3 active:scale-95 disabled:opacity-50 group"
                            >
                                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <LogIn className="w-5 h-5 transition-transform group-hover:translate-x-1" />}
                                {isSignUp ? "Generate Account" : "Access Studio"}
                            </button>

                            {error && (
                                <p className="text-red-500 text-xs font-bold text-center animate-pulse">{error}</p>
                            )}
                        </form>

                        <div className="relative my-8">
                            <div className="absolute inset-0 flex items-center">
                                <span className="w-full border-t border-foreground/5" />
                            </div>
                            <div className="relative flex justify-center text-[10px] uppercase font-black tracking-widest">
                                <span className="bg-transparent px-3 text-foreground/20">Fast Access</span>
                            </div>
                        </div>

                        <button
                            onClick={handleGoogleLogin}
                            className="w-full flex items-center justify-center gap-3 bg-surface-100 dark:bg-surface-900 hover:bg-surface-200 dark:hover:bg-surface-800 py-4 rounded-2xl transition-all font-bold border-2 border-transparent hover:border-brand-primary/20 active:scale-95"
                        >
                            <Chrome className="w-5 h-5" />
                            Google Authentication
                        </button>

                        <p className="mt-8 text-center text-sm font-medium text-foreground/40">
                            {isSignUp ? "Part of the studio?" : "New creator?"}{" "}
                            <button
                                onClick={() => setIsSignUp(!isSignUp)}
                                className="text-brand-primary font-black hover:underline underline-offset-4"
                            >
                                {isSignUp ? "Sign In" : "Join Now"}
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
