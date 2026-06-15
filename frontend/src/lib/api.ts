import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import Cookies from 'js-cookie';

const baseURL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api';

const api = axios.create({
  baseURL,
});

let refreshPromise: Promise<string | null> | null = null;

function clearSession() {
  Cookies.remove('gn_access');
  Cookies.remove('gn_refresh');
}

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = Cookies.get('gn_access');
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean } | undefined;
    const status = error.response?.status;
    const refresh = Cookies.get('gn_refresh');

    if (!originalRequest || status !== 401 || originalRequest._retry || !refresh) {
      if (status === 401) clearSession();
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    if (!refreshPromise) {
      refreshPromise = axios
        .post<{ access: string }>(`${baseURL}/token/refresh/`, { refresh })
        .then(({ data }) => {
          Cookies.set('gn_access', data.access, { expires: 1 });
          return data.access;
        })
        .catch((refreshError) => {
          clearSession();
          throw refreshError;
        })
        .finally(() => {
          refreshPromise = null;
        });
    }

    const nextAccess = await refreshPromise;
    if (!nextAccess) return Promise.reject(error);

    originalRequest.headers = originalRequest.headers ?? {};
    originalRequest.headers.Authorization = `Bearer ${nextAccess}`;
    return api(originalRequest);
  }
);

export default api;
