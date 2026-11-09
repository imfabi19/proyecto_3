export type Log = { method: string; url: string; status: number }
export type Result = { ok: boolean; status: number; data: unknown }

let onLog: (log: Log) => void = () => {}
export const setLogger = (fn: (log: Log) => void) => {
  onLog = fn
}

export async function call(method: string, url: string, body?: unknown): Promise<Result> {
  let status = 0
  let data: unknown = null
  try {
    const res = await fetch('/api' + url, {
      method,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    })
    status = res.status
    const text = await res.text()
    try {
      data = text ? JSON.parse(text) : null
    } catch {
      data = null
    }
  } catch {
    status = 0
  }
  onLog({ method, url, status })
  return { ok: status >= 200 && status < 300, status, data }
}

// Convierte la respuesta de error en texto corto para mostrar.
export function errorText({ status, data }: Result): string {
  if (status === 0 || status >= 500) return 'Django no responde o tiene un error. Revisa la terminal.'
  if (status === 404) return 'No existe (404).'
  if (data && typeof data === 'object') {
    return Object.entries(data)
      .map(([campo, msg]) => `${campo}: ${Array.isArray(msg) ? msg.join(' ') : msg}`)
      .join(' | ')
  }
  return `Error ${status}.`
}
