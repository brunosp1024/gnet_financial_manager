import api from '@/lib/api';
import { Customer, CustomerPayload, PaginatedResponse } from '@/types';

export const customersService = {
  async list(params?: { search?: string; ordering?: string; page?: number; page_size?: number }): Promise<PaginatedResponse<Customer>> {
    const { data } = await api.get<PaginatedResponse<Customer>>('/customers/', { params });
    return data;
  },

  async detail(id: string): Promise<Customer> {
    const { data } = await api.get<Customer>(`/customers/${id}/`);
    return data;
  },

  async create(payload: CustomerPayload): Promise<unknown> {
    const { data } = await api.post('/customers/', payload);
    return data;
  },

  async update(id: string, payload: CustomerPayload): Promise<unknown> {
    const { data } = await api.patch(`/customers/${id}/`, payload);
    return data;
  },

  async remove(id: string): Promise<void> {
    await api.delete(`/customers/${id}/`);
  },
};
