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
    const [googleLoading, setGoogleLoading] = useState(false);
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
        setGoogleLoading(true);
        setError(null);
        try {
            const { error } = await supabase.auth.signInWithOAuth({
                provider: "google",
                options: {
                    redirectTo: `${window.location.origin}/auth/callback`
                }
            });
            if (error) throw error;
        } catch (err: any) {
            setError(err.message);
            setGoogleLoading(false);
        }
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
                                        disabled={loading || googleLoading}
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
                                        disabled={loading || googleLoading}
                                    />
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={loading || googleLoading}
                                className="w-full bg-gradient-to-br from-brand-primary to-brand-accent text-white py-4 rounded-2xl font-black text-lg hover:shadow-xl hover:shadow-brand-primary/30 transition-all duration-300 flex items-center justify-center gap-3 active:scale-95 disabled:opacity-50 group"
                            >
                                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <LogIn className="w-5 h-5 transition-transform group-hover:translate-x-1" />}
                                {isSignUp ? "Generate Account" : "Access Studio"}
                            </button>

                            {error && (
                                <p className="text-red-500 text-[11px] font-black uppercase tracking-widest text-center animate-pulse">{error}</p>
                            )}
                        </form>

                        <div className="relative my-8">
                            <div className="absolute inset-0 flex items-center">
                                <span className="w-full border-t border-foreground/5" />
                            </div>
                            <div className="relative flex justify-center text-[10px] uppercase font-black tracking-widest">
                                <span className="bg-surface-50 dark:bg-slate-900 px-3 text-foreground/20">Fast Access</span>
                            </div>
                        </div>

                        <button
                            onClick={handleGoogleLogin}
                            disabled={loading || googleLoading}
                            className="w-full flex items-center justify-center gap-3 bg-white dark:bg-white/5 hover:bg-surface-100 dark:hover:bg-white/10 py-4 rounded-2xl transition-all font-bold border-2 border-slate-100 dark:border-white/5 hover:border-brand-primary/20 active:scale-95 disabled:opacity-50 shadow-sm"
                        >
                            {googleLoading ? (
                                <Loader2 className="w-5 h-5 animate-spin text-brand-primary" />
                            ) : (
                                <svg className="w-5 h-5" viewBox="0 0 24 24">
                                    <path
                                        fill="#4285F4"
                                        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                                    />
                                    <path
                                        fill="#34A853"
                                        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                                    />
                                    <path
                                        fill="#FBBC05"
                                        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"
                                    />
                                    <path
                                        fill="#EA4335"
                                        d="M12 5.38c1.62 0 3.06.56 4.21 1.66l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                                    />
                                </svg>
                            )}
                            <span className="text-foreground/80">Continue with Google</span>
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
