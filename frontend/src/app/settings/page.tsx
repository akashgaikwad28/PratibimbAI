"use client";

import { useState, useEffect } from "react";
import { Save, Shield, User, Key, CheckCircle2, AlertCircle } from "lucide-react";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

export default function SettingsPage() {
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

    const [profile, setProfile] = useState({
        full_name: "",
        profession: "",
        openai_api_key: "",
        groq_api_key: "",
        gemini_api_key: "",
    });

    useEffect(() => {
        async function loadProfile() {
            try {
                const data = await api.getProfile();
                setProfile({
                    full_name: data.full_name || "",
                    profession: data.profession || "",
                    openai_api_key: data.openai_api_key || "",
                    groq_api_key: data.groq_api_key || "",
                    gemini_api_key: data.gemini_api_key || "",
                });
            } catch (err) {
                console.error("Failed to load profile", err);
            } finally {
                setLoading(false);
            }
        }
        loadProfile();
    }, []);

    const handleSave = async () => {
        setSaving(true);
        setMessage(null);
        try {
            await api.updateProfile(profile);
            setMessage({ type: "success", text: "Profile updated successfully!" });
        } catch (err) {
            setMessage({ type: "error", text: "Failed to update profile. Please try again." });
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-primary"></div>
            </div>
        );
    }

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Settings</h2>
                <p className="text-foreground/60 mt-2">Manage your professional identity and API configurations.</p>
            </div>

            <div className="grid gap-6">
                {/* Personalization Section */}
                <section className="glass-card p-6 rounded-2xl space-y-6">
                    <div className="flex items-center gap-2 text-lg font-semibold border-b pb-4">
                        <User className="w-5 h-5 text-brand-primary" />
                        <h3>Personalization</h3>
                    </div>

                    <div className="grid gap-4 max-w-lg">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Full Name</label>
                            <input
                                type="text"
                                placeholder="Your name"
                                className="w-full bg-surface-100 border rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-primary outline-none transition-all"
                                value={profile.full_name}
                                onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Profession</label>
                            <input
                                type="text"
                                placeholder="e.g. Software Engineer, Crypto Trader"
                                className="w-full bg-surface-100 border rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-primary outline-none transition-all"
                                value={profile.profession}
                                onChange={(e) => setProfile({ ...profile, profession: e.target.value })}
                            />
                            <p className="text-xs text-foreground/40">This helps the AI write content that matches your expertise.</p>
                        </div>
                    </div>
                </section>

                {/* API Security Section */}
                <section className="glass-card p-6 rounded-2xl space-y-6">
                    <div className="flex items-center gap-2 text-lg font-semibold border-b pb-4">
                        <Shield className="w-5 h-5 text-brand-primary" />
                        <h3>LLM Configurations</h3>
                    </div>

                    <div className="grid gap-6 max-w-lg">
                        <div className="space-y-2 text-sm text-foreground/60 bg-brand-primary/5 p-4 rounded-xl border border-brand-primary/10">
                            <p>We use a priority system: <strong>Groq &gt; Gemini &gt; OpenAI</strong>. Your keys are used only for your own generations.</p>
                        </div>

                        <div className="space-y-4">
                            <div className="space-y-2">
                                <div className="flex items-center gap-2">
                                    <Key className="w-4 h-4 text-foreground/40" />
                                    <label className="text-sm font-medium text-foreground/70">Groq API Key (Highest Priority)</label>
                                </div>
                                <input
                                    type="password"
                                    placeholder="gsk_..."
                                    className="w-full bg-surface-100 border rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-primary outline-none transition-all"
                                    value={profile.groq_api_key}
                                    onChange={(e) => setProfile({ ...profile, groq_api_key: e.target.value })}
                                />
                            </div>

                            <div className="space-y-2">
                                <div className="flex items-center gap-2">
                                    <Key className="w-4 h-4 text-foreground/40" />
                                    <label className="text-sm font-medium text-foreground/70">Gemini API Key</label>
                                </div>
                                <input
                                    type="password"
                                    placeholder="AIza..."
                                    className="w-full bg-surface-100 border rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-primary outline-none transition-all"
                                    value={profile.gemini_api_key}
                                    onChange={(e) => setProfile({ ...profile, gemini_api_key: e.target.value })}
                                />
                            </div>

                            <div className="space-y-2">
                                <div className="flex items-center gap-2">
                                    <Key className="w-4 h-4 text-foreground/40" />
                                    <label className="text-sm font-medium text-foreground/70">OpenAI API Key</label>
                                </div>
                                <input
                                    type="password"
                                    placeholder="sk-..."
                                    className="w-full bg-surface-100 border rounded-xl px-4 py-2.5 focus:ring-2 focus:ring-brand-primary outline-none transition-all"
                                    value={profile.openai_api_key}
                                    onChange={(e) => setProfile({ ...profile, openai_api_key: e.target.value })}
                                />
                            </div>
                        </div>
                    </div>
                </section>

                <div className="flex items-center gap-4">
                    <button
                        onClick={handleSave}
                        disabled={saving}
                        className="flex items-center gap-2 bg-brand-primary text-white px-8 py-3 rounded-xl font-semibold hover:bg-brand-primary/90 transition-all active:scale-95 disabled:opacity-50"
                    >
                        <Save className="w-5 h-5" />
                        {saving ? "Saving..." : "Save Changes"}
                    </button>

                    {message && (
                        <div className={cn(
                            "flex items-center gap-2 text-sm font-medium animate-in fade-in zoom-in duration-300",
                            message.type === "success" ? "text-green-500" : "text-red-500"
                        )}>
                            {message.type === "success" ? <CheckCircle2 className="w-5 h-5" /> : <AlertCircle className="w-5 h-5" />}
                            {message.text}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
