"use client";

import { Sidebar } from "./Sidebar";
import { useAuth } from "@/context/AuthContext";
import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";
import { Loader2 } from "lucide-react";

export function AppShell({ children }: { children: React.ReactNode }) {
    const { user, loading } = useAuth();
    const router = useRouter();
    const pathname = usePathname();

    const isLoginPage = pathname === "/login";

    useEffect(() => {
        if (!loading && !user && !isLoginPage) {
            router.push("/login");
        }
    }, [user, loading, isLoginPage, router]);

    if (loading) {
        return (
            <div className="h-screen w-screen flex items-center justify-center bg-background">
                <Loader2 className="w-8 h-8 animate-spin text-brand-primary" />
            </div>
        );
    }

    if (!user && !isLoginPage) return null;

    if (isLoginPage) return <>{children}</>;

    return (
        <div className="flex bg-background h-screen overflow-hidden relative">
            {/* Dynamic Background Decor */}
            <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-brand-primary/5 rounded-full blur-[120px]" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-brand-accent/5 rounded-full blur-[120px]" />
            </div>

            <Sidebar />
            <main className="flex-1 overflow-y-auto relative scroll-smooth">
                <div className="max-w-5xl mx-auto p-6 md:p-12">
                    {children}
                </div>
            </main>
        </div>
    );
}
