
import { useState, useEffect } from 'react';

export default function WeatherMetrics( {city, degree}) {
    const [data, setData] = useState();

    const isF = degree === "f"

    const handleSearch = async () => {
        const response = await fetch(`http://localhost:8000/weather/${city}`)
        const dataJson = await response.json()

        const d = dataJson.data
        return d[0]
    }

    useEffect(() => {
        const fetchData = async () => {
            setData( await handleSearch())
        }
        fetchData()

    }, [city, degree])

    if (!data) return <p>loading...</p>

    const temp = isF ? data["temp_f"] : data["temp_c"]
    return (
        <>
        hi
        <h3> Current Temperature: {temp}  {isF ? 'f' : 'c'}</h3>
        </>
    )
}