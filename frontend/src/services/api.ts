/**
 * API Client
 *
 * Centralized API client for making requests to the backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return { error: error instanceof Error ? error.message : 'Unknown error' };
    }
  }

  // Project endpoints
  async createProject(data: any) {
    return this.request('/create-project-async', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getProjectInfo(projectId: string) {
    return this.request(`/get-project-info?project_id=${projectId}`);
  }

  async getProjectStatus(projectId: string) {
    return this.request(`/get-project-status?project_id=${projectId}`);
  }

  // Answer endpoints
  async generateSingleAnswer(data: any) {
    return this.request('/generate-single-answer', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async generateAllAnswers(data: any) {
    return this.request('/generate-all-answers', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateAnswer(data: any) {
    return this.request('/update-answer', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Document endpoints
  async indexDocument(data: any) {
    return this.request('/index-document-async', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Request status
  async getRequestStatus(requestId: string) {
    return this.request(`/get-request-status?request_id=${requestId}`);
  }

  // Evaluation
  async evaluateProject(projectId: string) {
    return this.request('/evaluate-project', {
      method: 'POST',
      body: JSON.stringify({ project_id: projectId }),
    });
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
export default apiClient;


