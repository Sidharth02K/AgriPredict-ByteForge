import { useState } from 'react'

import {
  CloudRain,
  MapPin,
  Sprout,
  Thermometer,
  FlaskConical,
  Leaf,
} from 'lucide-react'

function Prediction() {
  const [formData, setFormData] = useState({
    crop: '',
    location: '',
    season: 'Kharif',
    rainfall: '',
    temperature: '',
    soilPh: '',
    nitrogen: '',
    phosphorus: '',
    potassium: '',
  })
  const [prediction, setPrediction] = useState(null)

  const handleChange = (field, value) => {
    setFormData((previous) => ({
      ...previous,
      [field]: value,
    }))
  }

  const handlePredict = () => {
  setPrediction({
    yield: 4.26,
    risk: 'Low',
  })
}

  return (
  <div className="space-y-8">
    

      {/* Page header */}
            {prediction ? (
  <PredictionResult prediction={prediction} />
) : (
      <div className="rounded-3xl border border-green-100 bg-white p-8 shadow-sm">

        {/* Crop information */}
        <div>
          <div className="flex items-center gap-3">

            <div className="rounded-xl bg-green-100 p-2.5 text-green-700">
              <Sprout size={20} />
            </div>

            <div>
              <h2 className="font-semibold text-slate-800">
                Crop information
              </h2>

              <p className="text-sm text-slate-500">
                Select the crop and growing conditions.
              </p>
            </div>

          </div>

          <div className="mt-6 grid gap-5 md:grid-cols-3">

            <CropInput
              value={formData.crop}
              onChange={(value) => handleChange('crop', value)}
            />

            <LocationInput
              value={formData.location}
              onChange={(value) => handleChange('location', value)}
            />

            <FormSelect
              label="Season"
              icon={<Leaf size={17} />}
              options={['Kharif', 'Whole Year', 'Autumn', 'Summer', 'Winter', 'Rabi']}
              value={formData.season}
              onChange={(value) => handleChange('season', value)}
            />

          </div>
        </div>

        <div className="my-8 border-t border-slate-100" />

        {/* Environmental conditions */}
        <div>

          <div className="flex items-center gap-3">

            <div className="rounded-xl bg-blue-100 p-2.5 text-blue-700">
              <CloudRain size={20} />
            </div>

            <div>
              <h2 className="font-semibold text-slate-800">
                Environmental Conditions
              </h2>

              <p className="text-sm text-slate-500">
                Enter the current environmental measurements.
              </p>
            </div>

          </div>

          <div className="mt-6 grid gap-5 md:grid-cols-2">

            <FormInput
              label="Rainfall"
              unit="mm"
              placeholder="480"
              icon={<CloudRain size={17} />}
              value={formData.rainfall}
              onChange={(value) => handleChange('rainfall', value)}
            />

            <FormInput
              label="Temperature"
              unit="°C"
              placeholder="24"
              icon={<Thermometer size={17} />}
              value={formData.temperature}
              onChange={(value) => handleChange('temperature', value)}
            />

          </div>

        </div>

        <div className="my-8 border-t border-slate-100" />

        {/* Soil conditions */}
        <div>

          <div className="flex items-center gap-3">

            <div className="rounded-xl bg-amber-100 p-2.5 text-amber-700">
              <FlaskConical size={20} />
            </div>

            <div>
              <h2 className="font-semibold text-slate-800">
                Tell us about your soil 🌱
              </h2>

              <p className="text-sm text-slate-500">
                Enter the soil pH and nutrient levels.
              </p>
            </div>

          </div>

          <div className="mt-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">

            <FormInput
              label="Soil pH"
              placeholder="6.8"
              value={formData.soilPh}
              onChange={(value) => handleChange('soilPh', value)}
            />

            <FormInput
              label="Nitrogen"
              unit="kg/ha"
              placeholder="75"
              value={formData.nitrogen}
              onChange={(value) => handleChange('nitrogen', value)}
            />

            <FormInput
              label="Phosphorus"
              unit="kg/ha"
              placeholder="40"
              value={formData.phosphorus}
              onChange={(value) => handleChange('phosphorus', value)}
            />

            <FormInput
              label="Potassium"
              unit="kg/ha"
              placeholder="35"
              value={formData.potassium}
              onChange={(value) => handleChange('potassium', value)}
            />

          </div>

        </div>

        {/* Submit */}
        <div className="mt-8 flex justify-end">

          <button
            type="button"
            onClick={handlePredict}
            className="flex items-center gap-2 rounded-xl bg-green-600 px-6 py-3 font-semibold text-white shadow-sm transition hover:bg-green-700 hover:shadow-md active:scale-[0.98]"
          >
            <Sprout size={18} />
            Predict my yield
          </button>

        </div>

          </div>
                )}
            
    </div>

  )
}


/* ================================= */
/* Number input                      */
/* ================================= */

function FormInput({
  label,
  unit,
  placeholder,
  icon,
  value,
  onChange,
}) {
  return (
    <div>

      <label className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-700">

        {icon && (
          <span className="text-slate-400">
            {icon}
          </span>
        )}

        {label}

      </label>

      <div className="relative">

        <input
          type="number"
          value={value}
          placeholder={placeholder}
          onChange={(event) => onChange(event.target.value === '' ? '' : Number(event.target.value))}
          className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-green-500 focus:bg-white focus:ring-2 focus:ring-green-500/20"
        />

        {unit && (
          <span className="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-slate-400">
            {unit}
          </span>
        )}

      </div>

    </div>
  )
}


/* ================================= */
/* Season dropdown                   */
/* ================================= */

function FormSelect({
  label,
  icon,
  options,
  value,
  onChange,
}) {
  return (
    <div>

      <label className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-700">

        <span className="text-slate-400">
          {icon}
        </span>

        {label}

      </label>

      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition focus:border-green-500 focus:bg-white focus:ring-2 focus:ring-green-500/20"
      >

        {options.map((option) => (
          <option key={option}>
            {option}
          </option>
        ))}

      </select>

    </div>
  )
}


/* ================================= */
/* Crop search                       */
/* ================================= */

function CropInput({ value, onChange }) {
  const [isOpen, setIsOpen] = useState(false)

  const crops = [
  'Maize',
  'Potato',
  'Rice',
  'Sugarcane',
  'Wheat',
]

  const filteredCrops = crops.filter((crop) =>
    crop.toLowerCase().includes(value.toLowerCase())
  )

  return (
    <div className="relative">

      <label className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-700">

        <Sprout
          size={17}
          className="text-slate-400"
        />

        Crop

      </label>

      <input
        type="text"
        value={value}
        placeholder="Search crop..."
        onChange={(event) => {
          onChange(event.target.value)
          setIsOpen(true)
        }}
        onFocus={() => setIsOpen(true)}
        onBlur={() => {
          setTimeout(() => setIsOpen(false), 150)
        }}
        className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-green-500 focus:bg-white focus:ring-2 focus:ring-green-500/20"
      />

      {isOpen && value && filteredCrops.length > 0 && (
        <div className="absolute z-20 mt-2 max-h-52 w-full overflow-y-auto rounded-xl border border-green-100 bg-white p-1 shadow-lg">

          {filteredCrops.map((crop) => (
            <button
              key={crop}
              type="button"
              onMouseDown={() => {
                onChange(crop)
                setIsOpen(false)
              }}
              className="w-full rounded-lg px-4 py-3 text-left text-sm text-slate-600 transition hover:bg-green-50 hover:text-green-700"
            >
              {crop}
            </button>
          ))}

        </div>
      )}

      {isOpen && value && filteredCrops.length === 0 && (
        <div className="absolute z-20 mt-2 w-full rounded-xl border border-green-100 bg-white p-4 text-sm text-slate-500 shadow-lg">
          No matching crops found.
        </div>
      )}

    </div>
  )
}


/* ================================= */
/* Location search                   */
/* ================================= */

function LocationInput({ value, onChange }) {
  const [isOpen, setIsOpen] = useState(false)

  const locations = [
  'Assam',
  'Karnataka',
  'Meghalaya',
  'West Bengal',
  'Puducherry',
  'Goa',
  'Kerala',
  'Andhra Pradesh',
  'Tamil Nadu',
  'Odisha',
  'Bihar',
  'Gujarat',
  'Madhya Pradesh',
  'Maharashtra',
  'Mizoram',
  'Punjab',
  'Uttar Pradesh',
  'Haryana',
  'Himachal Pradesh',
  'Tripura',
  'Nagaland',
  'Chhattisgarh',
  'Uttarakhand',
  'Jharkhand',
  'Delhi',
  'Manipur',
  'Jammu and Kashmir',
  'Telangana',
  'Arunachal Pradesh',
  'Sikkim',
  'Rajasthan',
]

  const filteredLocations = locations.filter((location) =>
    location.toLowerCase().includes(value.toLowerCase())
  )

  return (
    <div className="relative">

      <label className="mb-2 flex items-center gap-2 text-sm font-medium text-slate-700">

        <MapPin
          size={17}
          className="text-slate-400"
        />

        Location

      </label>

      <input
        type="text"
        value={value}
        placeholder="Search location..."
        onChange={(event) => {
          onChange(event.target.value)
          setIsOpen(true)
        }}
        onFocus={() => setIsOpen(true)}
        onBlur={() => {
          setTimeout(() => setIsOpen(false), 150)
        }}
        className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-green-500 focus:bg-white focus:ring-2 focus:ring-green-500/20"
      />

      {isOpen && value && filteredLocations.length > 0 && (
        <div className="absolute z-20 mt-2 max-h-52 w-full overflow-y-auto rounded-xl border border-green-100 bg-white p-1 shadow-lg">

          {filteredLocations.map((location) => (
            <button
              key={location}
              type="button"
              onMouseDown={() => {
                onChange(location)
                setIsOpen(false)
              }}
              className="w-full rounded-lg px-4 py-3 text-left text-sm text-slate-600 transition hover:bg-green-50 hover:text-green-700"
            >
              {location}
            </button>
          ))}

        </div>
      )}

      {isOpen && value && filteredLocations.length === 0 && (
        <div className="absolute z-20 mt-2 w-full rounded-xl border border-green-100 bg-white p-4 text-sm text-slate-500 shadow-lg">
          No matching locations found.
        </div>
      )}

    </div>
  )
}
function PredictionResult({ prediction }) {
  return (
    <div className="space-y-8">

      {/* Header */}
      <div>
        <p className="text-sm font-semibold uppercase tracking-wider text-green-600">
          Your prediction 🌱
        </p>

        <h2 className="mt-2 text-3xl font-bold text-slate-800">
          Here&apos;s how your harvest is looking
        </h2>

        <p className="mt-2 text-slate-500">
          Based on the conditions you entered.
        </p>
      </div>

      {/* Main result */}
      <div className="rounded-3xl border border-green-100 bg-white p-8 shadow-sm">

        <div className="grid gap-8 md:grid-cols-2">

          {/* Yield */}
          <div className="rounded-2xl bg-green-50 p-8">

            <p className="text-sm font-medium text-green-700">
              Predicted yield
            </p>

            <div className="mt-3 flex items-baseline gap-3">
              <span className="text-5xl font-bold text-slate-800">
                {prediction.yield}
              </span>

              <span className="text-slate-500">
                tonnes / hectare
              </span>
            </div>

            <p className="mt-4 text-sm text-slate-500">
              Your predicted crop yield based on the conditions provided.
            </p>

          </div>

          {/* Risk */}
          <div className="rounded-2xl bg-green-50 p-8">

            <p className="text-sm font-medium text-green-700">
              Environmental risk
            </p>

            <div className="mt-4">
              <span className="inline-flex rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700">
                🟢 {prediction.risk} Risk
              </span>
            </div>

            <p className="mt-4 text-sm text-slate-500">
              Current conditions appear favorable for the selected crop.
            </p>

          </div>

        </div>

      </div>

      {/* Influencing factors */}
      <div className="grid gap-6 md:grid-cols-2">

        <div className="rounded-3xl border border-green-100 bg-white p-6 shadow-sm">

          <h3 className="text-lg font-semibold text-slate-800">
            What influenced your prediction?
          </h3>

          <p className="mt-1 text-sm text-slate-500">
            The main factors considered by the model.
          </p>

          <div className="mt-6 space-y-5">

            <ImpactBar
              label="Rainfall"
              value="85%"
            />

            <ImpactBar
              label="Nitrogen"
              value="72%"
            />

            <ImpactBar
              label="Temperature"
              value="61%"
            />

            <ImpactBar
              label="Soil pH"
              value="48%"
            />

          </div>

        </div>

        {/* Decision insights */}
        <div className="rounded-3xl border border-green-100 bg-white p-6 shadow-sm">

          <h3 className="text-lg font-semibold text-slate-800">
            Decision insights
          </h3>

          <p className="mt-1 text-sm text-slate-500">
            A few things worth keeping in mind.
          </p>

          <div className="mt-6 space-y-4">

            <Insight text="Rainfall conditions look favorable." />

            <Insight text="Nitrogen levels are supporting the crop." />

            <Insight text="Temperature is within a reasonable range." />

            <Insight text="Continue monitoring soil conditions." />

          </div>

        </div>

      </div>

      {/* Back button */}
        <button
  type="button"
  onClick={() => window.location.reload()}
  className="rounded-xl border border-green-200 bg-white px-5 py-3 text-sm font-semibold text-green-700 transition hover:bg-green-50"
>
  ← Make another prediction
</button>
    </div>
  )
}
function ImpactBar({ label, value }) {
  return (
    <div>

      <div className="mb-2 flex justify-between text-sm">
        <span className="font-medium text-slate-700">
          {label}
        </span>

        <span className="text-slate-400">
          {value}
        </span>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-green-100">
        <div
          className="h-full rounded-full bg-green-500"
          style={{ width: value }}
        />
      </div>

    </div>
  )
}
function Insight({ text }) {
  return (
    <div className="flex items-start gap-3 rounded-xl bg-green-50 p-4">

      <span className="mt-0.5 text-green-600">
        ✓
      </span>

      <p className="text-sm text-slate-600">
        {text}
      </p>

    </div>
  )
}
export default Prediction