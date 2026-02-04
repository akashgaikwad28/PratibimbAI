"use client";

import { useEffect } from "react";
import { supabase } from "@/lib/supabase";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";

export default function AuthCallback() {
    const router = useRouter();

    useEffect(() => {
        const handleAuthCallback = async () => {
            // The Supabase client automatically handles the code exchange in the background
            // when it initializes on the callback route. We just need to wait and then redirect.
            const { data: { session }, error } = await supabase.auth.getSession();

            if (error) {
                console.error("Error during auth callback:", error);
                router.push("/login?error=auth-callback-failed");
            } else if (session) {
                router.push("/");
            } else {
                // Fallback for edge cases
                router.push("/login");
            }
        };

        handleAuthCallback();
    }, [router]);

    return (
        <div className="min-h-screen bg-background flex flex-col items-center justify-center gap-4">
            <div className="w-16 h-16 rounded-[1.5rem] bg-brand-primary/10 flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-brand-primary animate-spin" />
            </div>
            <div className="text-center space-y-2">
                <h2 className="text-xl font-black uppercase tracking-widest text-foreground/40">Securing Session...</h2>
                <p className="text-sm text-foreground/20 font-medium">Please wait while we prepare your studio.</p>
            </div>
        </div>
    );
}
