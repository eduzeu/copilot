export type ApplicationStatus = "applied" | "pending" | "interview" | "accepted" | "rejected";

export interface Application {
  id: number;
  user_id: number;
  company: string;
  role_title: string;
  location: string;
  date_applied: string;
  status: ApplicationStatus;
  created_at: string;
  updated_at: string;
}
