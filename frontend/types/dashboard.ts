export interface DashboardStats {
  total_tasks: number;
  completed_tasks: number;
  pending_tasks: number;
  readiness_score: number;
  study_hours_today: number;
  upcoming_tasks: number;
  recent_activities: Array<{
    activity: string;
    subject: string;
    time: string;
  }>;
}

export interface DashboardData {
  success: boolean;
  data: DashboardStats;
}

export interface UserProfile {
  name?: string;
  email?: string;
  exam?: string;
  readiness_score?: number;
  available_hours_per_day?: number;
  weak_subjects?: string[];
  study_goals?: string[];
}

export interface AgentStatus {
  name: string;
  status: string;
  last_run?: string;
  success_rate: number;
}

// Research Types
export interface FrequentTopic {
  topic: string;
  frequency: number;
}

export interface ResearchSummary {
  exam_overview: string;
  high_priority_subjects: string[];
  frequent_topics: FrequentTopic[];
}

export interface Metadata {
  conducted_by: string;
  stages: string[];
  qualification: string;
  difficulty: string;
  preparation_duration?: string;
  exam_type?: string;
}

export interface ResearchData {
  research_summary: ResearchSummary;
  metadata: Metadata;
  actionable_insights: string[];
}

export interface ResearchResponse {
  success: boolean;
  data: ResearchData;
  usage: Record<string, number>;
}

// Student Analysis Types
export interface StrengthWeakness {
  subject: string;
  score: number;
  weightage: number;
  priority: string;
  recommendation: string;
}

export interface Recommendation {
  type: string;
  priority: string;
  action: string;
}

export interface RiskIndicator {
  type: string;
  severity: string;
  message: string;
}

export interface StudentAnalysisData {
  readiness_score: number;
  strengths: StrengthWeakness[];
  weaknesses: StrengthWeakness[];
  recommendations: Recommendation[];
  risk_indicators: RiskIndicator[];
  performance_summary: Record<string, any>;
}

export interface StudentAnalysisResponse {
  success: boolean;
  data: StudentAnalysisData;
  usage: Record<string, number>;
}

// Combined Dashboard Data
export interface FullDashboardData {
  research: ResearchData;
  studentAnalysis: StudentAnalysisData;
}

// Planning Types
export interface Topic {
  name: string;
  hours: number;
  priority: string;
  [key: string]: any;
}

export interface SubjectPlan {
  subject: string;
  priority: string;
  allocated_hours: number;
  topics: Topic[];
  [key: string]: any;
}

export interface Stage {
  stage_name: string;
  duration_weeks: number;
  focus_subjects: string[];
  weekly_hours: number;
  objectives?: string;
  [key: string]: any;
}

export interface PreparationRoadmap {
  duration_months: number;
  stages: Stage[];
  [key: string]: any;
}

export interface WeeklySchedule {
  daily_targets: string[];
  mock_test_frequency: string;
  study_days_per_week?: number;
  daily_hours?: number;
  [key: string]: any;
}

export interface DailyScheduleItem {
  time_slot: string;
  subject: string;
  activity: string;
  [key: string]: any;
}

export interface DailySchedule {
  day: string;
  items: DailyScheduleItem[];
  [key: string]: any;
}

export interface Milestone {
  type?: string;
  description: string;
  criteria: string[];
  reward?: string;
  target_stage?: string;
  [key: string]: any;
}

export interface RevisionCycle {
  subject: string;
  priority_score: number;
  revision_frequency: string;
  revision_days: number[];
  [key: string]: any;
}

export interface MockSchedule {
  mock_type: string;
  frequency: string;
  focus_subjects: string[];
  post_mock_analysis: boolean;
  [key: string]: any;
}

export interface PlanningData {
  preparation_roadmap: PreparationRoadmap;
  subject_plan: SubjectPlan[];
  weekly_schedule: WeeklySchedule;
  daily_schedule?: DailySchedule[];
  milestones?: Milestone[];
  revision_cycles?: RevisionCycle[];
  mock_schedule?: MockSchedule;
  [key: string]: any;
}

export interface PlanningRequest {
  exam?: string;
  readiness_score?: number;
  available_hours_per_day?: number;
  exam_date_distance_days?: number;
  weak_subjects?: string[];
}

export interface PlanningResponse {
  success: boolean;
  data: PlanningData;
  usage: Record<string, number>;
}

// Task Types
export interface TaskBase {
  title: string;
  description?: string;
  subject: string;
  topic?: string;
  priority: string;
  estimated_hours: number;
  due_date?: string;
  tags?: string[];
}

export interface TaskCreate extends TaskBase {}

export interface TaskUpdate {
  title?: string;
  description?: string;
  subject?: string;
  topic?: string;
  priority?: string;
  estimated_hours?: number;
  due_date?: string;
  tags?: string[];
  status?: string;
  progress?: number;
  completed_at?: string;
}

export interface Task extends TaskBase {
  id: string;
  status: string;
  progress: number;
  created_at: string;
  updated_at: string;
  completed_at?: string;
}

export interface TaskListResponse {
  success: boolean;
  data: Task[];
  count: number;
}

export interface TaskResponse {
  success: boolean;
  data: Task;
}

// Revision Types
export interface RevisionRequest {
  subject?: string;
  recent_tasks?: string[];
  current_readiness?: number;
}

export interface RevisionResponse {
  success: boolean;
  data: Record<string, unknown>;
}

// Replanning Types
export interface ReplanningRequest {
  current_tasks?: Task[];
  missed_tasks?: string[];
  new_availability?: number;
  readiness_change?: number;
}

export interface ReplanningResponse {
  success: boolean;
  data: Record<string, unknown>;
}

// Insights Types
export interface BurnoutAlert {
  type: string;
  severity: string;
  message: string;
}

export interface InsightsData {
  generated_at: string;
  burnout_alerts: BurnoutAlert[];
  weak_subjects: StrengthWeakness[];
  performance_summary: {
    total_tasks: number;
    completed_tasks: number;
    completion_rate: number;
    current_readiness: number;
    study_streak: number;
    last_updated: string;
  };
  recommendations: Recommendation[];
  trends: {
    high_frequency_topics: string[];
    high_priority_subjects: string[];
  };
}

export interface InsightsResponse {
  success: boolean;
  data: InsightsData;
}

// Agent Status Types
export interface AgentsStatusResponse {
  success: boolean;
  data: AgentStatus[];
}

