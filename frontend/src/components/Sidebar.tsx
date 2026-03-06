"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, History, User, Settings, Sparkles, LogOut, Globe } from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/context/AuthContext";

const menuItems = [
    { icon: Home, label: "Home", href: "/" },
    { icon: Globe, label: "Sources", href: "/sources" },
    { icon: History, label: "History", href: "/history" },
    { icon: User, label: "Profile", href: "/profile" },
    { icon: Settings, label: "Settings", href: "/settings" },
];

export function Sidebar() {
    const pathname = usePathname();
    const { signOut } = useAuth();

    return (
        <div className="flex flex-col h-screen w-72 border-r bg-card/50 backdrop-blur-xl p-6 gap-10 relative z-20">
            <div className="flex items-center gap-3 px-2">
                <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-brand-primary to-brand-accent flex items-center justify-center shadow-lg shadow-brand-primary/20 rotate-3 hover:rotate-0 transition-transform duration-300">
                    <Sparkles className="text-white w-6 h-6" />
                </div>
                <div>
                    <h1 className="text-xl font-black tracking-tight leading-none">PratibimbAI</h1>
                    <span className="text-[10px] uppercase tracking-widest text-brand-primary font-bold">Studio</span>
                </div>
            </div>

            <nav className="flex-1 flex flex-col gap-2">
                <div className="text-[10px] uppercase tracking-widest text-foreground/30 font-bold mb-2 ml-2">Menu</div>
                {menuItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-4 py-3 rounded-2xl transition-all duration-300 group relative",
                                isActive
                                    ? "text-brand-primary font-bold"
                                    : "text-foreground/50 hover:text-foreground hover:bg-surface-100 dark:hover:bg-surface-900/50"
                            )}
                        >
                            {isActive && (
                                <div className="absolute inset-0 bg-brand-primary/10 rounded-2xl -z-10 animate-in fade-in zoom-in-95 duration-300" />
                            )}
                            <item.icon className={cn(
                                "w-5 h-5 transition-transform duration-300 group-hover:scale-110",
                                isActive ? "text-brand-primary" : "group-hover:text-foreground"
                            )} />
                            <span className="text-sm">{item.label}</span>
                            {isActive && (
                                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-brand-primary shadow-[0_0_10px_rgba(29,155,240,0.5)]" />
                            )}
                        </Link>
                    );
                })}
            </nav>

            <div className="mt-auto pt-6 border-t border-foreground/5 flex flex-col gap-4">
                <button
                    onClick={() => signOut()}
                    className="flex items-center gap-3 px-4 py-3 rounded-2xl text-foreground/40 hover:text-red-500 hover:bg-red-500/10 transition-all duration-300 w-full group"
                >
                    <LogOut className="w-5 h-5 transition-transform group-hover:-translate-x-1" />
                    <span className="text-sm font-medium">Sign Out</span>
                </button>
            </div>
        </div>
    );
}
