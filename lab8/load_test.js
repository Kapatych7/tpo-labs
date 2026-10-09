// ЛР8: нагрузочный тест учебного REST API (/api/products) с помощью k6.
// Параметры нагрузки задаются из командной строки, например:
//   k6 run --vus 10 --duration 30s lab8/load_test.js
//   k6 run --vus 50 --duration 10s lab8/load_test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:5000';

export const options = {
  // Критерии успешности теста (SLA)
  thresholds: {
    http_req_failed: ['rate<0.01'],      // ошибок меньше 1 %
    http_req_duration: ['p(95)<500'],    // 95 % ответов быстрее 500 мс
    checks: ['rate>0.99'],
  },
};

export default function () {
  const page = Math.floor(Math.random() * 5) + 1;
  const res = http.get(`${BASE_URL}/api/products?page=${page}&size=10`);
  check(res, {
    'статус 200': (r) => r.status === 200,
    'в ответе 10 товаров': (r) => r.json('items').length === 10,
    'ответ быстрее 500 мс': (r) => r.timings.duration < 500,
  });
  sleep(0.5); // пауза "пользователя" между запросами
}
