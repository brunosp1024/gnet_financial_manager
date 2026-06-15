import api from '@/lib/api';
import Cookies from 'js-cookie';
import { LoginCredentials, TokenPair, User } from '@/types';

export const authService = {
  async login(credentials: LoginCredentials): Promise<{ tokens: TokenPair; user: User }> {
    const { data: tokens } = await api.post<TokenPair>('/token/', credentials);
    Cookies.set('gn_access',  tokens.access,  { expires: 1 });
    Cookies.set('gn_refresh', tokens.refresh, { expires: 7 });
    const { data: user } = await api.get<User>('/users/me/');
    return { tokens, user };
  },

  async logout(): Promise<void> {
    Cookies.remove('gn_access');
    Cookies.remove('gn_refresh');
  },

  async me(): Promise<User> {
    const { data } = await api.get<User>('/users/me/');
    return data;
  },

  isAuthenticated(): boolean {
    return !!Cookies.get('gn_access');
  },
};
