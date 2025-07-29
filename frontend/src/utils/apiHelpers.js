/**********************************************************************************************************
 * @file        apiHelpers.js 
 * @description Helper Utility, to request for different services (login/register/etc)
 * @team        SheCodes-Hub (MSITM'26 @ McComb School of Business, UT Austin)
 * @created     2025-07-24
 * @version     v1.0.0
 **********************************************************************************************************/
import { BASE_URL } from './apiConfig';

export async function postToEndpoint(endpoint, payload) {
  const response = await fetch(`${BASE_URL}/${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  return { ok: response.ok, data };
}
