import { useState, useEffect, FormEvent } from 'react'
import { Region } from './components/Region'
import { Accordion } from './components/Accordion';
import './App.css'


const REGION_OPTIONS = [
  'Vinnytsia',
  'Lutsk',
  'Dnipro',
  'Donetsk',
  'Zhytomyr',
  'Uzhhorod',
  'Zaporizhzhia',
  'Ivano-Frankivsk',
  'Kyiv',
  'Kropyvnytskyi',
  'Lviv',
  'Mykolaiv',
  'Odesa',
  'Poltava',
  'Rivne',
  'Sumy',
  'Ternopil',
  'Kharkiv',
  'Kherson',
  'Khmelnytskyi Oblast',
  'Cherkasy',
  'Chernivtsi',
  'Chernihiv'
]


function App() {
  const [regions, setRegions] = useState({})
  const [selectedRegions, setSelectedRegions] = useState<string[]>([]);
  const [selectAll, setSelectAll] = useState(false);

  const fetchData = async () => {
    const resp = await fetch('http://34.238.154.241:8000/predict', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ token: String(import.meta.env.VITE_TOKEN), locations: selectedRegions })
    })

    const data = await resp.json()
    setRegions(data)
  }

  const handleRegionChange = (e: FormEvent<HTMLInputElement>) => {
    const { value, checked } = e.target as HTMLInputElement;

    if (value === 'all') {
      setSelectAll(checked);
    } else {
      if (checked) {
        setSelectedRegions([...selectedRegions, value]);
      } else {
        setSelectedRegions(selectedRegions.filter(region => region !== value));
      }
    }
  }; 

  const handleClick = () => {
    fetchData()
  }

  useEffect(() => {
    fetchData()
  }, [])

  useEffect(() => {
    if (selectAll) {
      setSelectedRegions(REGION_OPTIONS);
    } else {
      setSelectedRegions([]);
    }
  }, [selectAll]);

  return (
    <>
      <h1>Alarms Prediction System</h1>

      <div className="container">
        <div className="region-checkboxes">
          <label>Select regions:</label>

          <div>
            <input
              type="checkbox"
              id="select-all"
              checked={selectAll}
              onChange={handleRegionChange}
              value="all"
            />
            <label htmlFor="select-all">Select All</label>
          </div>

          {REGION_OPTIONS.map((region) => (
            <div key={region}>
              <input
                type="checkbox"
                id={region}
                value={region}
                checked={selectedRegions.includes(region)}
                onChange={handleRegionChange}
              />
              <label htmlFor={region}>{region}</label>
            </div>
          ))}

          <button onClick={handleClick}>Submit</button>
        </div>


        <div className="read-the-docs accordion">
          {Object.entries(regions).map(([name, alarms]) => (
            <Accordion key={name} title={name}>
              <Region key={name} alarms={alarms as object} />
            </Accordion>
          ))}
        </div >
      </div >
    </>
  )
}

export default App