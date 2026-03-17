
export default function DegreeSelector( {degree, setDegree}) {

    return <select
        value={degree}
        onChange={(e) => setDegree(e.target.value)}
    >
        <option key="f">f</option>
        <option key="c">c</option>
    </select>
}
