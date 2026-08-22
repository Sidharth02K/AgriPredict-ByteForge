import { useEffect, useState } from 'react'
import { getPredictionHistory } from './services/api'
import {
  LayoutDashboard,
  History,
  BarChart3,
  Sprout,
} from 'lucide-react'
import HistoryPage from './pages/History'
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

import Prediction from './pages/Prediction'

    function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [latestPrediction, setLatestPrediction] = useState(null)

  useEffect(() => {
    async function loadLatestPrediction() {
      try {
        const result = await getPredictionHistory()
        setLatestPrediction(result.items?.[0] || null)
      } catch (error) {
        console.error('Failed to load latest prediction:', error)
      }
    }

    loadLatestPrediction()
  }, [])
  return (
    <div className="min-h-screen bg-[#f6f8f3] text-slate-800">

      {/* Animated wind layer */}
      <WindAnimation />

      {/* Sidebar */}
      <aside className="fixed left-0 top-0 z-10 h-screen w-64 border-r border-green-100 bg-white">

        {/* Logo */}
        <div className="flex items-center gap-3 border-b border-green-100 p-6">
          <div className="rounded-xl bg-green-100 p-2.5 text-green-700">
            <Sprout size={22} />
          </div>

          <div>
            <h1 className="font-bold text-slate-800">
              AgriPredict
            </h1>

            <p className="text-xs text-slate-400">
              Your farming companion
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="p-4">

          <button
  type="button"
  onClick={() => setCurrentPage('dashboard')}
  className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm transition ${
    currentPage === 'dashboard'
      ? 'bg-green-100 font-semibold text-green-800'
      : 'text-slate-500 hover:bg-green-50 hover:text-green-700'
  }`}
>
  <LayoutDashboard size={18} />
  Dashboard
</button>
          <button
  type="button"
  onClick={() => setCurrentPage('prediction')}
  className={`mt-2 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm transition ${
    currentPage === 'prediction'
      ? 'bg-green-100 font-semibold text-green-800'
      : 'text-slate-500 hover:bg-green-50 hover:text-green-700'
  }`}
>
  <Sprout size={18} />
  Prediction
</button>

          <button
  type="button"
  onClick={() => setCurrentPage('history')}
  className={`mt-2 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm transition ${
    currentPage === 'history'
      ? 'bg-green-100 font-semibold text-green-800'
      : 'text-slate-500 hover:bg-green-50 hover:text-green-700'
  }`}
>
  <History size={18} />
  History
</button>

          <button
  type="button"
  onClick={() => setCurrentPage('analytics')}
  className={`mt-2 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm transition ${
    currentPage === 'analytics'
      ? 'bg-green-100 font-semibold text-green-800'
      : 'text-slate-500 hover:bg-green-50 hover:text-green-700'
  }`}
>
  <BarChart3 size={18} />
  Analytics
</button>

        </nav>

      </aside>

      {/* Main content */}
      <main className="relative z-0 ml-64 min-h-screen p-8">

        <div className="mx-auto max-w-7xl">

          {currentPage === 'dashboard' && (
  <>
    {/* Greeting */}
    <div className="mb-8">

      <p className="text-sm font-medium text-green-600">
        AGRIPREDICT 🌱
      </p>

      <div className="mt-2 flex items-center gap-4">

        <h1 className="text-3xl font-bold tracking-tight text-slate-800">
          Good morning!
        </h1>

        <AnimatedPlant />

      </div>

      <p className="mt-2 text-slate-500">
        Let&apos;s predict your harvest.
      </p>

    </div>
        {/* Dashboard overview cards */}
    <div className="grid gap-5 md:grid-cols-2">

      {/* Last prediction */}
      <div className="rounded-2xl border border-green-100 bg-white p-6 shadow-sm">

        <p className="text-sm font-medium text-slate-500">
          Last prediction
        </p>

        <div className="mt-3 flex items-baseline gap-2">
          <span className="text-3xl font-bold text-slate-800">
  {latestPrediction
    ? latestPrediction.expected_yield_tonnes_per_ha.toFixed(2)
    : '—'}
</span>

          <span className="text-sm text-slate-400">
            tonnes / hectare
          </span>
        </div>

        <p className="mt-2 text-sm text-slate-500">
  {latestPrediction
    ? `${latestPrediction.crop_type} · ${latestPrediction.location}`
    : 'No predictions yet'}
</p>

      </div>

      {/* Current risk */}
      <div className="rounded-2xl border border-green-100 bg-white p-6 shadow-sm">

        <p className="text-sm font-medium text-slate-500">
          Current risk
        </p>

        <div className="mt-3">
          <span
  className={`inline-flex rounded-full px-4 py-2 text-sm font-semibold ${
    latestPrediction?.risk_level === 'LOW'
      ? 'bg-green-100 text-green-700'
      : latestPrediction?.risk_level === 'HIGH'
        ? 'bg-red-100 text-red-700'
        : 'bg-yellow-100 text-yellow-700'
  }`}
>
  {latestPrediction?.risk_level === 'LOW'
    ? '🟢 Low Risk'
    : latestPrediction?.risk_level === 'HIGH'
      ? '🔴 High Risk'
      : '🟡 Moderate Risk'}
</span>
        </div>

        <p className="mt-3 text-sm text-slate-500">
  {latestPrediction?.risk_level === 'HIGH'
    ? 'Current conditions may negatively affect the selected crop.'
    : latestPrediction?.risk_level === 'LOW'
      ? 'Conditions currently look favorable.'
      : 'Conditions require some attention.'}
</p>
      </div>

    </div>

    {/* Yield prediction heading */}
    
    <div className="mb-8">
  <p className="text-sm font-semibold uppercase tracking-wider text-green-600">
    Yield prediction
  </p>

  <h2 className="mt-2 text-3xl font-bold tracking-tight text-slate-800">
    Predict your crop yield
  </h2>

  <p className="mt-2 max-w-2xl text-slate-500">
    Enter your crop, environmental, and soil conditions to generate
    an AI-powered yield forecast.
  </p>
</div>
{/* Quick prediction */}
<div className="rounded-2xl border border-green-100 bg-white p-6 shadow-sm">

  <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">

    <div>
      <div className="flex items-center gap-2">
        <Sprout size={20} className="text-green-600" />

        <h3 className="text-lg font-semibold text-slate-800">
          Ready to predict your next harvest?
        </h3>
      </div>

      <p className="mt-2 max-w-2xl text-sm text-slate-500">
        Enter your crop, location, weather, and soil conditions
        to get an AI-powered yield estimate.
      </p>
    </div>

    <button
      type="button"
      onClick={() => setCurrentPage('prediction')}
      className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-green-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-green-700 active:scale-[0.98]"
    >
      Start prediction
      <span>→</span>
    </button>

  </div>

</div>
  </>
)}

                    {currentPage === 'prediction' && (
  <Prediction />
)}
{currentPage === 'history' && (
  <HistoryPage />
)}
{currentPage === 'analytics' && (
  <AnalyticsPage />
)}

        </div>

    </main>

    </div>
  )
}


/* ================================= */
/* Animated plant                    */
/* ================================= */

function AnimatedPlant() {
  return (
    <div className="relative h-16 w-20">

      <svg
        viewBox="0 0 100 100"
        className="h-full w-full overflow-visible"
      >

        {/* Pot */}
        <path
          d="M32 73 L68 73 L62 92 L38 92 Z"
          fill="#c58b5c"
        />

        <ellipse
          cx="50"
          cy="73"
          rx="18"
          ry="5"
          fill="#8b5e3c"
        />

        {/* Plant group that sways */}
        <g className="plant-sway">

          {/* Stem */}
          <path
            d="M50 74 C50 58 48 42 51 27"
            fill="none"
            stroke="#4d9b54"
            strokeWidth="4"
            strokeLinecap="round"
          />

          {/* Left leaf */}
          <path
            d="M49 49 C34 47 25 38 29 28 C40 29 48 36 49 49 Z"
            fill="#69b96b"
          />

          {/* Right leaf */}
          <path
            d="M51 39 C62 26 75 25 82 32 C76 43 65 46 51 39 Z"
            fill="#4f9f55"
          />

          {/* Top leaf */}
          <path
            d="M51 28 C46 16 51 8 61 5 C67 15 63 24 51 28 Z"
            fill="#79c879"
          />

        </g>

      </svg>

    </div>
  )
}


/* ================================= */
/* Wind animation                     */
/* ================================= */

function WindAnimation() {
  return (
    <div
      className="pointer-events-none fixed left-0 top-0 z-50 h-28 w-full overflow-hidden"
      aria-hidden="true"
    >

      {/* Wind stream 1 */}
      <div className="wind wind-one">
        <span />
        <span />
        <span />
      </div>

      {/* Wind stream 2 */}
      <div className="wind wind-two">
        <span />
        <span />
        <span />
      </div>

      {/* Wind stream 3 */}
      <div className="wind wind-three">
        <span />
        <span />
        <span />
      </div>

      {/* Small drifting leaves */}
      <div className="floating-leaf leaf-one">🍃</div>
      <div className="floating-leaf leaf-two">🍃</div>
      <div className="floating-leaf leaf-three">🍃</div>

      <style>{`

        /* ========================= */
        /* Plant movement             */
        /* ========================= */

        .plant-sway {
          transform-origin: 50px 74px;
          animation: plantSway 4s ease-in-out infinite;
        }

        @keyframes plantSway {

          0% {
            transform: rotate(0deg);
          }

          20% {
            transform: rotate(2deg);
          }

          45% {
            transform: rotate(-3deg);
          }

          70% {
            transform: rotate(2deg);
          }

          100% {
            transform: rotate(0deg);
          }

        }


        /* ========================= */
        /* Wind streams               */
        /* ========================= */

        .wind {
          position: absolute;
          left: -35%;
          width: 70%;
          height: 30px;
          opacity: 0;
          animation-name: windFlow;
          animation-timing-function: linear;
          animation-iteration-count: infinite;
        }

        .wind span {
          position: absolute;
          display: block;
          width: 100%;
          height: 2px;
          border-radius: 999px;
          background: linear-gradient(
            90deg,
            transparent,
            rgba(100, 190, 125, 0.05),
            rgba(100, 190, 125, 0.32),
            rgba(100, 190, 125, 0.08),
            transparent
          );
        }

        .wind span:nth-child(1) {
          top: 2px;
        }

        .wind span:nth-child(2) {
          top: 12px;
          width: 75%;
        }

        .wind span:nth-child(3) {
          top: 22px;
          width: 55%;
        }

        .wind-one {
          top: 22px;
          animation-duration: 9s;
        }

        .wind-two {
          top: 55px;
          animation-duration: 12s;
          animation-delay: 3s;
        }

        .wind-three {
          top: 88px;
          animation-duration: 10s;
          animation-delay: 6s;
        }

        @keyframes windFlow {

          0% {
            transform: translateX(0);
            opacity: 0;
          }

          15% {
            opacity: 0.8;
          }

          70% {
            opacity: 0.55;
          }

          100% {
            transform: translateX(200%);
            opacity: 0;
          }

        }


        /* ========================= */
        /* Floating leaves            */
        /* ========================= */

        .floating-leaf {
          position: absolute;
          left: -5%;
          font-size: 14px;
          opacity: 0;
          animation: leafFlow 14s linear infinite;
        }

        .leaf-one {
          top: 25px;
          animation-delay: 4s;
        }

        .leaf-two {
          top: 65px;
          animation-delay: 9s;
          font-size: 11px;
        }

        .leaf-three {
          top: 40px;
          animation-delay: 14s;
          font-size: 12px;
        }

        @keyframes leafFlow {

          0% {
            transform: translateX(0) translateY(0) rotate(0deg);
            opacity: 0;
          }

          10% {
            opacity: 0.6;
          }

          50% {
            transform: translateX(90vw) translateY(-8px) rotate(180deg);
            opacity: 0.5;
          }

          85% {
            opacity: 0.3;
          }

          100% {
            transform: translateX(120vw) translateY(12px) rotate(360deg);
            opacity: 0;
          }

        }

      `}</style>

    </div>
  )
}

function AnalyticsPage() {
  const [history, setHistory] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function loadAnalyticsData() {
      try {
        const result = await getPredictionHistory()
        setHistory(result.items || [])
      } catch (error) {
        console.error('Failed to load analytics data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    loadAnalyticsData()
  }, [])

  const cropTotals = {}

  history.forEach((prediction) => {
    const crop = prediction.crop_type

    if (!cropTotals[crop]) {
      cropTotals[crop] = {
        total: 0,
        count: 0,
      }
    }

    cropTotals[crop].total += prediction.expected_yield_tonnes_per_ha
    cropTotals[crop].count += 1
  })

  const cropData = Object.entries(cropTotals).map(
    ([crop, data]) => ({
      crop,
      yield: Number((data.total / data.count).toFixed(2)),
    })
  )

  const trendData = [...history]
    .reverse()
    .map((prediction, index) => ({
      prediction: String(index + 1),
      yield: Number(
        prediction.expected_yield_tonnes_per_ha.toFixed(2)
      ),
    }))

  const riskCounts = {
    LOW: 0,
    MODERATE: 0,
    HIGH: 0,
  }

  history.forEach((prediction) => {
    if (riskCounts[prediction.risk_level] !== undefined) {
      riskCounts[prediction.risk_level] += 1
    }
  })

  const totalPredictions = history.length

  const riskData = [
    {
      name: 'Low Risk',
      value: totalPredictions
        ? Math.round((riskCounts.LOW / totalPredictions) * 100)
        : 0,
    },
    {
      name: 'Moderate Risk',
      value: totalPredictions
        ? Math.round((riskCounts.MODERATE / totalPredictions) * 100)
        : 0,
    },
    {
      name: 'High Risk',
      value: totalPredictions
        ? Math.round((riskCounts.HIGH / totalPredictions) * 100)
        : 0,
    },
  ]

  return (
    <div className="space-y-8">

      {/* Header */}
      <div>
        <p className="text-sm font-semibold uppercase tracking-wider text-green-600">
          Analytics
        </p>

        <h2 className="mt-2 text-3xl font-bold tracking-tight text-slate-800">
          Understand your predictions
        </h2>

        <p className="mt-2 text-slate-500">
          Track yield patterns and environmental trends across your predictions.
        </p>
      </div>

      {/* Summary cards */}
      <div className="grid gap-5 md:grid-cols-3">

        <div className="rounded-2xl border border-green-100 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-slate-500">
            Average yield
          </p>

          <p className="mt-3 text-3xl font-bold text-slate-800">
            3.84
          </p>

          <p className="mt-1 text-sm text-slate-400">
            tonnes / hectare
          </p>
        </div>

        <div className="rounded-2xl border border-green-100 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-slate-500">
            Predictions made
          </p>

          <p className="mt-3 text-3xl font-bold text-slate-800">
            12
          </p>

          <p className="mt-1 text-sm text-slate-400">
            total predictions
          </p>
        </div>

        <div className="rounded-2xl border border-green-100 bg-white p-6 shadow-sm">
          <p className="text-sm font-medium text-slate-500">
            Low risk predictions
          </p>

          <p className="mt-3 text-3xl font-bold text-green-600">
            75%
          </p>

          <p className="mt-1 text-sm text-slate-400">
            of your predictions
          </p>
        </div>

      </div>
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2"></div>

      {/* Yield by crop */}
      <div className="rounded-2xl border border-green-100 bg-white p-6 shadow-sm">

        <h3 className="text-lg font-semibold text-slate-800">
          Yield by crop
        </h3>

        <p className="mt-1 text-sm text-slate-500">
          Average predicted yield for each crop.
        </p>

        <div className="mt-6 h-72 w-full">

          <ResponsiveContainer width="100%" height="100%">

            <BarChart data={cropData}>

              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="crop"
                tickLine={false}
                axisLine={false}
              />

              <YAxis
                tickLine={false}
                axisLine={false}
              />

              <Tooltip
                formatter={(value) => [`${value} t/ha`, 'Yield']}
              />

              <Bar
                dataKey="yield"
                name="Yield"
                radius={[8, 8, 0, 0]}
                fill="#4d9b54"
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

      {/* Yield prediction trend */}
      <div className="rounded-2xl border border-green-100 bg-white p-6 shadow-sm">

        <h3 className="text-lg font-semibold text-slate-800">
          Yield prediction trend
        </h3>

        <p className="mt-1 text-sm text-slate-500">
          Yield values across recent predictions.
        </p>

        <div className="mt-6 h-72 w-full">

          <ResponsiveContainer width="100%" height="100%">

            <LineChart data={trendData}>

              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="prediction"
                tickLine={false}
                axisLine={false}
                tickFormatter={(value) => `#${value}`}
              />

              <YAxis
                tickLine={false}
                axisLine={false}
              />

              <Tooltip
                formatter={(value) => [`${value} t/ha`, 'Yield']}
                labelFormatter={(value) => `Prediction #${value}`}
              />

              <Line
                type="monotone"
                dataKey="yield"
                name="Yield"
                stroke="#4d9b54"
                strokeWidth={3}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

      </div>
      

      {/* Risk overview */}
      <div className="rounded-2xl border border-green-100 bg-white p-6 shadow-sm">

        <h3 className="text-lg font-semibold text-slate-800">
          Risk overview
        </h3>

        <p className="mt-1 text-sm text-slate-500">
          Breakdown of your prediction risk levels.
        </p>

        <div className="mt-6 grid items-center gap-8 md:grid-cols-2">

          {/* Donut chart */}
          <div className="h-72 w-full">

            <ResponsiveContainer width="100%" height="100%">

              <PieChart>

                <Pie
                  data={riskData}
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={105}
                  paddingAngle={3}
                  dataKey="value"
                >

                  <Cell fill="#4d9b54" />
                  <Cell fill="#eab308" />
                  <Cell fill="#ef4444" />

                </Pie>

                <Tooltip
                  formatter={(value) => [`${value}%`, 'Predictions']}
                />

              </PieChart>

            </ResponsiveContainer>

          </div>

          {/* Legend */}
          <div className="space-y-5">

            <div className="flex items-center justify-between">

              <div className="flex items-center gap-3">
                <span className="h-3 w-3 rounded-full bg-green-500" />

                <span className="text-sm text-slate-600">
                  Low Risk
                </span>
              </div>

              <span className="font-semibold text-slate-800">
                75%
              </span>

            </div>

            <div className="flex items-center justify-between">

              <div className="flex items-center gap-3">
                <span className="h-3 w-3 rounded-full bg-yellow-500" />

                <span className="text-sm text-slate-600">
                  Moderate Risk
                </span>
              </div>

              <span className="font-semibold text-slate-800">
                20%
              </span>

            </div>

            <div className="flex items-center justify-between">

              <div className="flex items-center gap-3">
                <span className="h-3 w-3 rounded-full bg-red-500" />

                <span className="text-sm text-slate-600">
                  High Risk
                </span>
              </div>

              <span className="font-semibold text-slate-800">
                5%
              </span>

            </div>

          </div>

        </div>

      </div>

    </div>
  )
}
export default App