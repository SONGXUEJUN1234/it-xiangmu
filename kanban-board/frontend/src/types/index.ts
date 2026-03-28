// User Types
export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  avatar_url: string | null;
  is_active?: boolean;
  is_verified?: boolean;
  created_at: string;
}

export interface AuthTokens {
  access: {
    token: string;
    expires_in: number;
  };
  refresh: {
    token: string;
    expires_in: number;
  };
}

export interface AuthResponse {
  user: User;
  tokens: AuthTokens;
}

// Board Types
export interface BoardMember {
  user: User;
  role: 'owner' | 'admin' | 'member';
  joined_at: string;
}

export interface Board {
  id: string;
  title: string;
  description: string;
  owner?: {
    id: string;
    username: string;
    avatar_url: string | null;
  };
  owner_id?: string;
  background_color: string;
  background_url: string | null;
  is_public: boolean;
  is_archived: boolean;
  member_count?: number;
  members?: BoardMember[];
  lists?: List[];
  labels?: Label[];
  created_at: string;
}

// List Types
export interface List {
  id: string;
  title: string;
  position: number;
  card_count?: number;
  cards?: Card[];
  created_at?: string;
}

// Card Types
export interface Card {
  id: string;
  title: string;
  description: string | null;
  list_id: string;
  board?: {
    id: string;
    title: string;
  };
  list?: {
    id: string;
    title: string;
  };
  position: number;
  assignee?: User | null;
  priority: 'low' | 'medium' | 'high' | 'critical';
  due_date: string | null;
  labels?: Label[];
  comment_count?: number;
  attachment_count?: number;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

// Label Types
export interface Label {
  id: string;
  name: string;
  color: string;
}

// Comment Types
export interface Comment {
  id: string;
  content: string;
  card_id: string;
  author: {
    id: string;
    username: string;
    avatar_url: string | null;
  };
  parent_id: string | null;
  is_edited: boolean;
  created_at: string;
  updated_at: string;
  replies?: Comment[];
}

// Activity Types
export interface Activity {
  id: string;
  user: {
    id: string;
    username: string;
    avatar_url: string | null;
  };
  action: string;
  entity_type: string;
  entity_id: string;
  entity_title: string;
  changes: Record<string, any> | null;
  created_at: string;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  pagination: {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
  };
}

// Form Types
export interface LoginFormData {
  email: string;
  password: string;
}

export interface RegisterFormData {
  email: string;
  username: string;
  password: string;
  full_name: string;
}

export interface CreateBoardFormData {
  title: string;
  description: string;
  background_color: string;
}

export interface CreateListFormData {
  title: string;
  position?: number;
}

export interface CreateCardFormData {
  title: string;
  description?: string;
  position?: number;
  priority?: string;
  due_date?: string;
  label_ids?: string[];
}

export interface CreateCommentFormData {
  content: string;
  parent_id?: string;
}
