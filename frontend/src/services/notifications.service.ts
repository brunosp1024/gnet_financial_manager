import api from '@/lib/api';
import { Notification, NotificationPayload, PaginatedResponse } from '@/types';

export const notificationsService = {
  async list(params?: { is_read?: boolean; type?: string; page?: number; page_size?: number }): Promise<PaginatedResponse<Notification>> {
    const { data } = await api.get<PaginatedResponse<Notification>>('/notifications/', { params });
    return data;
  },

  async create(payload: NotificationPayload): Promise<unknown> {
    const { data } = await api.post('/notifications/', payload);
    return data;
  },

  async update(id: string, payload: Partial<NotificationPayload>): Promise<unknown> {
    const { data } = await api.patch(`/notifications/${id}/`, payload);
    return data;
  },

  async remove(id: string): Promise<void> {
    await api.delete(`/notifications/${id}/`);
  },
};
