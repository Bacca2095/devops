import axios from 'axios';
import { toast } from 'sonner';

export interface NormalizedError {
  type: 'NETWORK_ERROR' | 'HTTP_ERROR';
  status?: number;
  code?: string;
  message: string;
  data?: unknown;
}

const REQUEST_TIMEOUT_MS = 15_000;
const LOCALLY_HANDLED_STATUSES: number[] = [400, 422];
const isProd = import.meta.env.PROD;

export const axiosClient = axios.create({
  baseURL: isProd ? window.location.origin : import.meta.env.VITE_API_BASE_URL,
  timeout: REQUEST_TIMEOUT_MS,
  headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
});

axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      toast.error('Sin conexión', { id: 'network-error', description: 'No se pudo conectar con el servidor.' });
      return Promise.reject({ type: 'NETWORK_ERROR', message: 'Sin conexión' });
    }

    const { status, data } = error.response;
    const message = data?.detail ?? data?.message ?? 'Error inesperado';
    const code: string | undefined = data?.code;

    if (!LOCALLY_HANDLED_STATUSES.includes(status)) {
      toast.error(`Error ${status}`, { id: `http-error-${status}`, description: message });
    }

    return Promise.reject({ type: 'HTTP_ERROR', status, code, message, data });
  },
);
