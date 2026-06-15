import api from '@/lib/api';
import { Employee, EmployeePayload, PaginatedResponse } from '@/types';

export const employeesService = {
  async list(params?: { search?: string; ordering?: string; page?: number; page_size?: number }): Promise<PaginatedResponse<Employee>> {
    const { data } = await api.get<PaginatedResponse<Employee>>('/employees/', { params });
    return data;
  },

  async detail(id: string): Promise<Employee> {
    const { data } = await api.get<Employee>(`/employees/${id}/`);
    return data;
  },

  async create(payload: EmployeePayload): Promise<unknown> {
    const { data } = await api.post('/employees/', payload);
    return data;
  },

  async update(id: string, payload: EmployeePayload): Promise<unknown> {
    const { data } = await api.patch(`/employees/${id}/`, payload);
    return data;
  },

  async remove(id: string): Promise<void> {
    await api.delete(`/employees/${id}/`);
  },
};
