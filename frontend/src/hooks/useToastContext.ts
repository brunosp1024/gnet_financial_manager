'use client';

import { createContext, useContext } from 'react';
import { ToastType } from './useToast';

export const ToastContext = createContext<(msg: string, type?: ToastType) => void>(() => {});

export const useToastContext = () => useContext(ToastContext);
