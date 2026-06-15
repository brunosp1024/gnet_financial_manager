import api from '@/lib/api';
import { Invoice, InvoicePayload, InvoiceUpdatePayload, PaginatedResponse } from '@/types';

export const invoicesService = {
  async list(params?: { ordering?: string; page?: number; page_size?: number; status?: string }): Promise<PaginatedResponse<Invoice>> {
    const { data } = await api.get<PaginatedResponse<Invoice>>('/invoices/', { params });
    return data;
  },

  async create(payload: InvoicePayload): Promise<unknown> {
    const { data } = await api.post('/invoices/', payload);
    return data;
  },

  async update(id: string, payload: InvoiceUpdatePayload): Promise<unknown> {
    const { data } = await api.patch(`/invoices/${id}/`, payload);
    return data;
  },

  async remove(id: string): Promise<void> {
    await api.delete(`/invoices/${id}/`);
  },
};
