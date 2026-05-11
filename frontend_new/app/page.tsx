"use client";

import { useState } from "react";
import PdfUploader from "@/components/PdfUploader";
import ThemeToggle from "@/components/ThemeToggle";
import { SummaryResult } from "@/types";

export default function Home() {
  const [result, setResult] = useState<SummaryResult>({
    loading: false, summary: null, error: null,
  });

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-50 font-sans relative overflow-hidden selection:bg-indigo-100 dark:selection:bg-indigo-900/50 selection:text-indigo-900 dark:selection:text-indigo-100 transition-colors duration-300">
      
      {/* Our Theme Toggler! */}
      <ThemeToggle />

      {/* Premium Ambient Background Effects */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] opacity-20 dark:opacity-10 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-r from-violet-400 to-indigo-500 blur-[100px] rounded-full mix-blend-multiply dark:mix-blend-screen filter"></div>
      </div>

      <main className="relative z-10 max-w-2xl mx-auto px-4 py-20 sm:py-32">
        {/* Header Section */}
        <div className="text-center mb-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 text-xs font-bold tracking-wide uppercase mb-6 border border-indigo-100 dark:border-indigo-500/20 shadow-sm">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
            </span>
            AI-Powered Engine
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white sm:text-5xl mb-4">
            Research, <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400">Summarized.</span>
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-xl mx-auto leading-relaxed">
            Instantly extract key findings and methodologies from any scientific paper using our advanced processing pipeline.
          </p>
        </div>

        {/* Uploader Card */}
        <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl rounded-3xl p-6 sm:p-10 shadow-xl shadow-slate-200/50 dark:shadow-black/50 border border-white dark:border-slate-800 mb-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-150 fill-mode-both transition-colors">
          <PdfUploader onSummaryChange={setResult} />
        </div>

        {/* Results Section */}
        {(result.loading || result.error || result.summary) && (
          <section className="animate-in fade-in slide-in-from-bottom-8 duration-500">
            <div className="bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-10 shadow-xl shadow-slate-200/50 dark:shadow-black/50 border border-slate-100 dark:border-slate-800 relative overflow-hidden transition-colors">
              
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 to-violet-500"></div>

              <h2 className="text-xl font-bold mb-6 text-slate-900 dark:text-white flex items-center gap-2">
                <svg className="w-5 h-5 text-indigo-500 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Analysis Result
              </h2>
              
              {result.loading && (
                <div className="flex flex-col items-center justify-center py-16 gap-5">
                  <div className="relative">
                    <div className="h-12 w-12 rounded-full border-4 border-slate-100 dark:border-slate-800"></div>
                    <div className="h-12 w-12 rounded-full border-4 border-indigo-600 dark:border-indigo-500 border-t-transparent animate-spin absolute top-0 left-0"></div>
                  </div>
                  <p className="text-slate-500 dark:text-slate-400 font-medium animate-pulse">
                    Synthesizing document contents...
                  </p>
                </div>
              )}

              {result.error && (
                <div className="rounded-2xl bg-red-50 dark:bg-red-900/20 p-5 border border-red-100 dark:border-red-900/50 text-red-700 dark:text-red-400 text-sm flex gap-3 items-start">
                  <svg className="w-5 h-5 text-red-500 dark:text-red-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <strong className="block font-bold mb-1">Processing Failed</strong>
                    {result.error}
                  </div>
                </div>
              )}

              {result.summary && !result.loading && (
                <div className="prose prose-slate dark:prose-invert prose-sm sm:prose-base max-w-none">
                  <div className="rounded-2xl bg-slate-50 dark:bg-slate-950 p-6 sm:p-8 text-slate-700 dark:text-slate-300 leading-relaxed border border-slate-100 dark:border-slate-800/60">
                    {result.summary}
                  </div>
                </div>
              )}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}