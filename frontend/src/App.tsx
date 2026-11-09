import { useCallback, useEffect, useState, type FormEvent, type ReactNode } from 'react'
import { call, errorText, setLogger, type Log } from './api'

type Row = { id: number; [key: string]: string | number }
type Field = {
  name: string
  label: string
  type?: 'text' | 'email' | 'number'
  options?: { value: number; label: string }[]
}
type Column = { label: string; value: (row: Row) => ReactNode }

function Crud(props: {
  title: string
  path: string
  fields: Field[]
  columns: Column[]
  rows: Row[]
  deleteWarning: string
  reload: () => void
}) {
  const { title, path, fields, columns, rows, deleteWarning, reload } = props
  const blank = () => Object.fromEntries(fields.map((f) => [f.name, '']))
  const [form, setForm] = useState<Record<string, string>>(blank)
  const [editing, setEditing] = useState<Row | null>(null)
  const [error, setError] = useState('')

  const reset = () => {
    setForm(blank())
    setEditing(null)
    setError('')
  }

  const startEdit = (row: Row) => {
    setEditing(row)
    setError('')
    setForm(Object.fromEntries(fields.map((f) => [f.name, String(row[f.name])])))
  }

  const convert = (f: Field) =>
    f.type === 'number' || f.options ? Number(form[f.name]) : form[f.name]

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    let result
    if (editing) {
      // PATCH estándar de DRF: /recurso/id/
      const changed = fields.filter((f) => form[f.name] !== String(editing[f.name]))
      if (changed.length === 0) return reset()
      const body = Object.fromEntries(changed.map((f) => [f.name, convert(f)]))
      result = await call('PATCH', `/${path}/${editing.id}/`, body)
    } else {
      // POST estándar de DRF: /recurso/
      const body = Object.fromEntries(fields.map((f) => [f.name, convert(f)]))
      result = await call('POST', `/${path}/`, body)
    }
    if (!result.ok) return setError(errorText(result))
    reset()
    reload()
  }

  const remove = async (row: Row) => {
    if (!window.confirm(deleteWarning)) return
    // DELETE estándar de DRF: /recurso/id/
    const result = await call('DELETE', `/${path}/${row.id}/`)
    if (!result.ok) return setError(errorText(result))
    if (editing?.id === row.id) reset()
    reload()
  }

  return (
    <section className="card">
      <h2>{title}</h2>
      <form onSubmit={submit}>
        {fields?.map((f) => (
          <label key={f.name}>
            {f.label}
            {f.options ? (
              <select
                required
                value={form[f.name] || ''}
                onChange={(e) => setForm({ ...form, [f.name]: e.target.value })}
              >
                <option value="">Elegir</option>
                {f.options?.map((o) => (
                  <option key={o.value} value={o.value}>
                    {o.label}
                  </option>
                ))}
              </select>
            ) : (
              <input
                required
                type={f.type ?? 'text'}
                value={form[f.name] || ''}
                onChange={(e) => setForm({ ...form, [f.name]: e.target.value })}
              />
            )}
          </label>
        ))}
        <div className="actions">
          <button type="submit">{editing ? `Guardar #${editing.id}` : 'Crear'}</button>
          {editing && (
            <button type="button" className="ghost" onClick={reset}>
              Cancelar
            </button>
          )}
        </div>
        {error && <p className="error">{error}</p>}
      </form>

      <table>
        <thead>
          <tr>
            {columns?.map((c) => (
              <th key={c.label}>{c.label}</th>
            ))}
            <th />
          </tr>
        </thead>
        <tbody>
          {rows?.map((row) => (
            <tr key={row.id} className={editing?.id === row.id ? 'active' : ''}>
              {columns?.map((c) => (
                <td key={c.label}>{c.value(row)}</td>
              ))}
              <td className="row-actions">
                <button className="ghost" onClick={() => startEdit(row)}>
                  Editar
                </button>
                <button className="danger" onClick={() => remove(row)}>
                  Borrar
                </button>
              </td>
            </tr>
          ))}
          {(!rows || rows.length === 0) && (
            <tr>
              <td colSpan={columns.length + 1} className="empty">
                Sin datos
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </section>
  )
}

export default function App() {
  const [responsables, setResponsables] = useState<Row[]>([])
  const [mascotas, setMascotas] = useState<Row[]>([])
  const [logs, setLogs] = useState<Log[]>([])
  const [loadError, setLoadError] = useState('')

  const reload = useCallback(async () => {
    const [r, m] = await Promise.all([call('GET', '/responsables'), call('GET', '/mascotas')])
    if (r.ok) setResponsables(r.data as Row[])
    if (m.ok) setMascotas(m.data as Row[])
    setLoadError(r.ok && m.ok ? '' : errorText(r.ok ? m : r))
  }, [])

  useEffect(() => {
    setLogger((log) => setLogs((prev) => [log, ...prev].slice(0, 8)))
    reload()
  }, [reload])

  const nombreResponsable = (id: number) =>
    String(responsables?.find((r) => r.id === id)?.nombre ?? `#${id}`)

  return (
    <main>
      <header>
        <h1>Mascotas</h1>
        <p>CRUD de la API Django</p>
      </header>

      {loadError && <p className="banner">{loadError}</p>}

      <div className="grid">
        <Crud
          title="Responsables"
          path="responsables"
          rows={responsables}
          reload={reload}
          deleteWarning="¿Borrar este responsable y todas sus mascotas?"
          fields={[
            { name: 'nombre', label: 'Nombre' },
            { name: 'correo', label: 'Correo', type: 'email' },
            { name: 'rut', label: 'RUT' },
          ]}
          columns={[
            { label: 'ID', value: (r) => r.id },
            { label: 'Nombre', value: (r) => r.nombre },
            { label: 'Correo', value: (r) => r.correo },
            { label: 'RUT', value: (r) => r.rut },
          ]}
        />

        <Crud
          title="Mascotas"
          path="mascotas"
          rows={mascotas}
          reload={reload}
          deleteWarning="¿Borrar esta mascota?"
          fields={[
            { name: 'nombre', label: 'Nombre' },
            { name: 'anio_nacimiento', label: 'Año nacimiento', type: 'number' },
            { name: 'especie', label: 'Especie' },
            {
              name: 'responsable',
              label: 'Responsable',
              options: responsables?.map((r) => ({ value: r.id, label: String(r.nombre) })) || [],
            },
          ]}
          columns={[
            { label: 'ID', value: (m) => m.id },
            { label: 'Nombre', value: (m) => m.nombre },
            { label: 'Año', value: (m) => m.anio_nacimiento },
            { label: 'Especie', value: (m) => m.especie },
            { label: 'Responsable', value: (m) => nombreResponsable(Number(m.responsable)) },
          ]}
        />
      </div>

      <section className="card log">
        <h2>Últimas peticiones</h2>
        {logs?.map((l, i) => (
          <div key={i} className="log-row">
            <span className={`method ${l.method}`}>{l.method}</span>
            <code>{l.url}</code>
            <span className={`status s${String(l.status)[0]}`}>{l.status || 'sin respuesta'}</span>
          </div>
        ))}
      </section>
    </main>
  )
}