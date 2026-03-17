import { useState, useEffect } from 'react'
import './App.css'

import CitySelector  from './components/CitySelector'
import WeatherMetrics from './components/WeatherMetrics'
import DegreeSelector from './components/DegreeSelector'

function App() {

  const [city, setCity] = useState(1);
  const [degree, setDegree] = useState('f');
  const [cities, setCities] = useState({});

  const grab = async () => {
      const results = await fetch('http://localhost:8000/weather');
      const d = await results.json()
      return d.data
  }

  useEffect( () => {
      const fetchCities = async () => {
          setCities( await grab() )
      }
      fetchCities()
  }, [])

  return (
    <>
        <h1>le weather</h1>

      <CitySelector city={city} setCity={setCity} cities={cities} ></CitySelector>
      <br />
      <DegreeSelector value={degree} setDegree={setDegree}></DegreeSelector>

      <br />
      <WeatherMetrics city={city} degree={degree}
      
      ></WeatherMetrics>

      
    
    </>
  )
}

export default App
