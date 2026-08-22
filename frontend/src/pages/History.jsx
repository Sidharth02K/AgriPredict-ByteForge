import { useEffect, useState } from 'react'
import {
  Clock3,
  MapPin,
  Sprout,
  TrendingUp,
  AlertTriangle,
} from 'lucide-react'

import { getPredictionHistory } from '../services/api'

function History() {
  const [history, setHistory] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const loadHistory = async () => {
      try {
        setIsLoading(true)
        setError('')

        const result = await getPredictionHistory()

        setHistory(result.items || [])
      } catch (error) {
        setError(
          error.message ||
          'Unable to load prediction history.'
        )
      } finally {
        setIsLoading(false)
      }
    }

    loadHistory()
  }, [])

  return (
    <div className="space-y-8">

      {/* Header */}
      <div>
        <p className="text-sm font-semibold uppercase tracking-wider text-green-600">
          Prediction history
        </p>

        <h1 className="mt-2 text-3xl font-bold text-slate-800">
          Your previous predictions
        </h1>

        <p className="mt-2 text-slate-500">
          Review the crop yield predictions you have made.
        </p>
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="rounded-3xl border border-green-100 bg-white p-8 text-center shadow-sm">
          <p className="text-slate-500">
            Loading your prediction history...
          </p>
        </div>
      )}

      {/* Error */}
      {!isLoading && error && (
        <div className="rounded-3xl border border-red-100 bg-white p-8 shadow-sm">
          <div className="flex items-start gap-3">
            <AlertTriangle
              className="mt-0.5 text-red-500"
              size={20}
            />

            <div>
              <h2 className="font-semibold text-slate-800">
                Unable to load history
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                {error}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Empty */}
      {!isLoading && !error && history.length === 0 && (
        <div className="rounded-3xl border border-green-100 bg-white p-10 text-center shadow-sm">
          <Clock3
            className="mx-auto text-slate-400"
            size={32}
          />

          <h2 className="mt-4 font-semibold text-slate-800">
            No predictions yet
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Your predictions will appear here after you make one.
          </p>
        </div>
      )}

      {/* History list */}
      {!isLoading && !error && history.length > 0 && (
        <div className="space-y-4">
          {history.map((item) => (
            <HistoryCard
              key={item.id}
              prediction={item}
            />
          ))}
        </div>
      )}

    </div>
  )
}

function HistoryCard({ prediction }) {
  const formattedDate = new Date(
    prediction.created_at
  ).toLocaleString()

  const isHighRisk =
    prediction.risk_level === 'HIGH'

  return (
    <div className="rounded-3xl border border-green-100 bg-white p-6 shadow-sm">

      <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">

        {/* Crop + location */}
        <div>

          <div className="flex items-center gap-3">

            <div className="rounded-xl bg-green-100 p-2.5 text-green-700">
              <Sprout size={20} />
            </div>

            <div>
              <h2 className="font-semibold text-slate-800">
                {prediction.crop_type}
              </h2>

              <div className="mt-1 flex items-center gap-2 text-sm text-slate-500">
                <MapPin size={15} />
                {prediction.location}
              </div>
            </div>

          </div>

          <div className="mt-4 flex flex-wrap gap-2">

            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
              {prediction.season}
            </span>

            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
              Prediction #{prediction.id}
            </span>

          </div>

        </div>

        {/* Result */}
        <div className="grid gap-4 sm:grid-cols-2 md:min-w-[360px]">

          <div className="rounded-2xl bg-green-50 p-4">

            <div className="flex items-center gap-2 text-sm text-green-700">
              <TrendingUp size={16} />
              Predicted yield
            </div>

            <p className="mt-2 text-2xl font-bold text-slate-800">
              {prediction.expected_yield_tonnes_per_ha.toFixed(2)}
            </p>

            <p className="text-xs text-slate-500">
              tonnes / hectare
            </p>

          </div>

          <div className="rounded-2xl bg-slate-50 p-4">

            <p className="text-sm text-slate-500">
              Risk level
            </p>

            <span
              className={`mt-2 inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
                isHighRisk
                  ? 'bg-red-100 text-red-700'
                  : prediction.risk_level === 'MODERATE'
                    ? 'bg-amber-100 text-amber-700'
                    : 'bg-green-100 text-green-700'
              }`}
            >
              {isHighRisk
                ? '🔴'
                : prediction.risk_level === 'MODERATE'
                  ? '🟡'
                  : '🟢'}{' '}
              {prediction.risk_level}
            </span>

          </div>

        </div>

      </div>

      {/* Date */}
      <div className="mt-5 flex items-center gap-2 border-t border-slate-100 pt-4 text-xs text-slate-400">
        <Clock3 size={14} />
        {formattedDate}
      </div>

    </div>
  )
}

export default History