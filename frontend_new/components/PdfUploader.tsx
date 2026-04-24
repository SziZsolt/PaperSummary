"use client";

import { useState, useEffect, useRef } from "react";
import { Domain, SummaryResult } from "@/types";

interface PdfUploaderProps {
  onSummaryChange: (result: SummaryResult) => void;
}

export default function PdfUploader({ onSummaryChange }: PdfUploaderProps) {
  const [domains, setDomains] = useState<Domain[]>([]);
  const [domainId, setDomainId] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [isDomainsLoading, setIsDomainsLoading] = useState(true);
  const [domainsError, setDomainsError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch("/api/domains")
      .then(async (res) => {
        if (!res.ok) throw new Error("Failed to load domains");
        return res.json();
      })
      .then((list: Domain[]) => {
        setDomains(list);
        if (list.length > 0) setDomainId(list[0].id);
      })
      .catch((err) => setDomainsError(err.message))
      .finally(() => setIsDomainsLoading(false));
  }, []);

  // --- Drag and Drop Handlers ---
  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };
  const onDragLeave = () => setIsDragging(false);
  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === "application/pdf") setFile(droppedFile);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !domainId) return;

    setIsSubmitting(true);
    onSummaryChange({ loading: true, summary: null, error: null });

    try {
      const formData = new FormData();
      formData.append("domain_id", domainId);
      formData.append("file", file);

      const res = await fetch("/api/summarize", { method: "POST", body: formData });
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || "An unknown error occurred");
      onSummaryChange({ loading: false, summary: data.summary, error: null });
    } catch (err: any) {
      onSummaryChange({ loading: false, summary: null, error: err.message });
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-8">
      {/* Domain Selector */}
      <div className="flex flex-col gap-3">
        <label htmlFor="domain" className="text-sm font-semibold text-slate-700 dark:text-slate-300 ml-1">
          Select Research Domain
        </label>
        {isDomainsLoading ? (
          <div className="h-12 w-full animate-pulse bg-slate-100 dark:bg-slate-800 rounded-xl"></div>
        ) : domainsError ? (
          <div className="text-sm text-red-500 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-4 rounded-xl border border-red-100 dark:border-red-900/50">
            {domainsError}
          </div>
        ) : (
          <div className="relative">
            <select
              id="domain"
              value={domainId}
              onChange={(e) => setDomainId(e.target.value)}
              required
              className="w-full rounded-xl border border-slate-200 dark:border-slate-700 px-5 py-3.5 text-slate-800 dark:text-slate-200 bg-slate-50/50 dark:bg-slate-800/50 hover:bg-slate-50 dark:hover:bg-slate-800 focus:bg-white dark:focus:bg-slate-900 focus:border-indigo-500 dark:focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 dark:focus:ring-indigo-500/20 outline-none transition-all appearance-none cursor-pointer font-medium"
            >
              {domains.map((d) => (
                <option key={d.id} value={d.id}>{d.label}</option>
              ))}
            </select>
            {/* Custom Dropdown Arrow */}
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-5 text-slate-400 dark:text-slate-500">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        )}
      </div>

      {/* Drag & Drop Zone */}
      <div className="flex flex-col gap-3">
        <label className="text-sm font-semibold text-slate-700 dark:text-slate-300 ml-1">Upload Document</label>
        <div
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onDrop={onDrop}
          onClick={() => !file && fileInputRef.current?.click()}
          className={`relative group overflow-hidden rounded-2xl border-2 border-dashed transition-all duration-300 ${
            file
              ? "border-indigo-500 bg-indigo-50/30 dark:bg-indigo-500/10 p-6"
              : isDragging
              ? "border-indigo-500 bg-indigo-50/50 dark:bg-indigo-500/20 p-12"
              : "border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 hover:border-indigo-300 dark:hover:border-indigo-500/50 hover:bg-slate-50/80 dark:hover:bg-slate-800 p-12 cursor-pointer"
          }`}
        >
          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            ref={fileInputRef}
            className="hidden"
            required={!file}
          />
          
          {file ? (
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-indigo-100 dark:border-indigo-900/50 text-indigo-600 dark:text-indigo-400">
                  <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-800 dark:text-slate-200 truncate max-w-[200px] sm:max-w-[300px]">
                    {file.name}
                  </p>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{formatFileSize(file.size)}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={(e) => { e.stopPropagation(); setFile(null); }}
                className="p-2 text-slate-400 dark:text-slate-500 hover:text-red-500 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center text-center">
              <div className="p-4 bg-white dark:bg-slate-900 rounded-full shadow-sm border border-slate-100 dark:border-slate-800 text-slate-400 dark:text-slate-500 group-hover:text-indigo-500 dark:group-hover:text-indigo-400 transition-colors duration-300 mb-4">
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
              </div>
              <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">Click to upload or drag and drop</p>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">PDF documents up to 10MB</p>
            </div>
          )}
        </div>
      </div>

      {/* Premium Submit Button */}
      <button
        type="submit"
        disabled={isSubmitting || isDomainsLoading || !file || !!domainsError}
        className="relative overflow-hidden mt-4 w-full flex justify-center items-center gap-3 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-500 dark:to-violet-500 px-4 py-4 text-base font-semibold text-white shadow-lg shadow-indigo-500/25 dark:shadow-indigo-900/20 hover:shadow-indigo-500/40 dark:hover:shadow-indigo-900/40 hover:-translate-y-0.5 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 disabled:opacity-50 disabled:hover:translate-y-0 disabled:shadow-none disabled:cursor-not-allowed transition-all duration-300"
      >
        {isSubmitting ? (
          <>
            <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Analyzing Document...
          </>
        ) : (
          "Generate Summary"
        )}
      </button>
    </form>
  );
}