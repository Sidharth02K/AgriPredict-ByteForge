const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'https://agripredict-byteforge.onrender.com'

export async function predictCropYield(formData) {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/predict`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        location: formData.location,
        crop_type: formData.crop,
        season: formData.season,
        rainfall_mm: formData.rainfall,
        temperature_c: formData.temperature,
        soil_ph: formData.soilPh,
        nitrogen_kgha: formData.nitrogen,
        phosphorus_kgha: formData.phosphorus,
        potassium_kgha: formData.potassium,
        farm_area_ha: 1,
      }),
    }
  )


  if (!response.ok) {
    const errorData = await response.json().catch(() => null)

    throw new Error(
      errorData?.detail ||
      'Unable to get a prediction from the server.'
    )
  }

  const data = await response.json()

return {
  ...data,
  yield: data.expected_yield_tonnes_per_ha,
  risk: data.risk_level,
}
}
export async function getPredictionHistory() {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/history?page=1&page_size=100`
  )

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)

    throw new Error(
      errorData?.detail ||
      'Unable to load prediction history.'
    )
  }

  return response.json()
}
