import api from '@/lib/api';
import { User, PaginatedResponse } from '@/types';

export type UserPayload = {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  group?: string;
  password?: string;
  is_active?: boolean;
};

export const usersService = {
  async list(params?: { search?: string; ordering?: string; page?: number; page_size?: number }): Promise<PaginatedResponse<User>> {
    const { data } = await api.get<PaginatedResponse<User>>('/users/', { params });
    return data;
  },

  async detail(id: string): Promise<User> {
    const { data } = await api.get<User>(`/users/${id}/`);
    return data;
  },

  async create(payload: UserPayload): Promise<unknown> {
    const { data } = await api.post('/users/', payload);
    return data;
  },

  async update(id: string, payload: Partial<UserPayload>): Promise<unknown> {
    const { data } = await api.patch(`/users/${id}/`, payload);
    return data;
  },

  async remove(id: string): Promise<void> {
    await api.delete(`/users/${id}/`);
  },
};
