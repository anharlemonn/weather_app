export default function CitySelector( {city, setCity, cities }) {
    
    return (
        <>
        <select name="city"
            value={city}
            onChange={(e => {
                setCity(e.target.value)
            })}
        >
            {
                Object.entries(cities).map( ( [key, value]) => {
                    return (
                        <option value={Number(key)+1}>{value["name"]}</option>

                    ) 
                })
            }    
        </select>
        </>

)
}
