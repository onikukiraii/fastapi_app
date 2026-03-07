import createClient from 'openapi-fetch'
import type { paths } from './schema'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const api = createClient<paths>({
  baseUrl: BASE_URL,
  fetch: async (input: Request) => {
    try {
      return await fetch(input)
    } catch {
      throw new Error('サーバーとの通信に失敗しました')
    }
  },
})

/** API レスポンスの data を取り出し、error があれば例外を投げる */
export function unwrap<T>(result: { data?: T; error?: unknown }): T {
  if (result.error !== undefined) {
    const err = result.error as Record<string, unknown>
    const message = typeof err.detail === 'string' ? err.detail : 'サーバーエラーが発生しました'
    throw new Error(message)
  }
  return result.data as T
}

// --- サンプル API オブジェクト ---
// import type { components } from './schema'
// type ItemResponse = components['schemas']['ItemResponse']
//
// export const itemsApi = {
//   list: async () => {
//     const res = await api.GET('/items/')
//     return unwrap<ItemResponse[]>(res)
//   },
// }

export { api }
