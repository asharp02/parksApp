import React, { useRef, useEffect, useState } from 'react';
import BylawToggle from './BylawToggle.jsx';
import mapboxgl from 'mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import axios from "axios";
mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_API_KEY;


function App() {
    const mapContainer = useRef(null);
    const map = useRef(null);
    const [lng, setLng] = useState(-79.3832);
    const [lat, setLat] = useState(43.6532);
    const [zoom, setZoom] = useState(12.5);
    const [npBylaws, setNpBylaws] = useState([]);
    const [rpBylaws, setRpBylaws] = useState([]);
    const [loading, setLoading] = useState(true);
    const [npBylawMarkers, setNpBylawMarkers] = useState([]);
    const [rpBylawMarkers, setRpBylawMarkers] = useState([]);

    useEffect(() => {
        if (map.current) return;
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [lng, lat],
            zoom: zoom
        });

        const fetchNpData = async () => {
            try {
                const response = await axios.get("/api/npbylaws");
                const result = await response.data;
                setNpBylaws(result);
                setLoading(false);
            } catch (error) {
                console.error("Error fetching no parking bylaws", error);
                setLoading(false);
            }
        };

        const fetchRpData = async () => {
            try {
                const response = await axios.get("/api/rpbylaws");
                const result = await response.data;
                setRpBylaws(result);
                setLoading(false);
            } catch (error) {
                console.log("Error fetching restricted parking bylaws", error);
                setLoading(false);
            }
        };
        fetchNpData();
        fetchRpData();
    }, []);

    useEffect(() => {
        if(!loading && npBylaws && rpBylaws){
            setNpBylawMarkers(addMarkers(npBylaws));
            setRpBylawMarkers(addMarkers(rpBylaws));
        }
    }, [loading, npBylaws, rpBylaws])
    const addMarkers = (bylaws) => {
        const markers = bylaws.results.map((bylaw) => {
            const color = bylaw.schedule === "13" ? "#ff0000" : "#50C878";
            let marker_a = new mapboxgl.Marker({color: color})
                .setLngLat([bylaw.midpoint[1], bylaw.midpoint[0]])
                .addTo(map.current);
            return marker_a
        })
        console.log(markers)
        return markers
    }

    return (
        <div>
            <BylawToggle></BylawToggle>
            <div ref={mapContainer} className="map-container" />
        </div>
    );
}

export default App;



// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'

// function App() {
//   const [count, setCount] = useState(0)

//   return (
//     <>
//       <div>
//         <a href="https://vitejs.dev" target="_blank">
//           <img src={viteLogo} className="logo" alt="Vite logo" />
//         </a>
//         <a href="https://react.dev" target="_blank">
//           <img src={reactLogo} className="logo react" alt="React logo" />
//         </a>
//       </div>
//       <h1>Vite + React</h1>
//       <div className="card">
//         <button onClick={() => setCount((count) => count + 1)}>
//           count is {count}
//         </button>
//         <p>
//           Edit <code>src/App.jsx</code> and save to test HMR
//         </p>
//       </div>
//       <p className="read-the-docs">
//         Click on the Vite and React logos to learn more
//       </p>
//     </>
//   )
// }

// export default App
