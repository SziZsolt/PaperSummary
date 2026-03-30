export interface Domain {
  id: string;
  label: string;
}

export interface SummaryResult {
  loading: boolean;
  summary: string | null;
  error: string | null;
}