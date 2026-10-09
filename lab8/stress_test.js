// ЛР8 (дополнительно): ступенчатое увеличение нагрузки для поиска предела API.
import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:5000';

export const options = {
  stages: [
    { duration: '10s', target: 20 },
    { duration: '10s', target: 100 },
    { duration: '10s', target: 200 },
    { duration: '5s', target: 0 },
  ],
  thresholds: { http_req_failed: ['rate<0.05'], http_req_duration: ['p(95)<1000'] },
};

export default function () {
  const res = http.get(`${BASE_URL}/api/products?page=1&size=10`);
  check(res, { 'статус 200': (r) => r.status === 200 });
}
