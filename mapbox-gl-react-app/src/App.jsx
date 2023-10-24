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
            setNpBylawMarkers(createMarkers(npBylaws, true));
            setRpBylawMarkers(createMarkers(rpBylaws, false));
        }
    }, [loading, npBylaws, rpBylaws])
    const createMarkers = (bylaws, isNpBylaws) => {
        const markers = bylaws.results.map((bylaw) => {
            const color = isNpBylaws ? "#ff0000" : "#50C878";
            let marker_a = new mapboxgl.Marker({color: color})
                .setLngLat([bylaw.midpoint[1], bylaw.midpoint[0]])
                .addTo(map.current)
            return marker_a
        })
        console.log(markers)
        return markers
    }
    const addMarkers = (bylawMarkers) => {
        bylawMarkers.forEach((marker) => {
            marker.addTo(map.current);
        })
    }
    const removeMarkers = (bylawMarkers) => {
        bylawMarkers.forEach((marker) => {
            marker.remove();
        })
    }

    const toggleMarkers = (isNPMarkers, isChecked) => {
        let markers = isNPMarkers ? npBylawMarkers : rpBylawMarkers;
        if (isChecked) {
            removeMarkers(markers);
        } else {
            addMarkers(markers);
        }
    }

    return (
        <div>
            <BylawToggle toggleHandler={toggleMarkers}></BylawToggle>
            <div ref={mapContainer} className="map-container" />
        </div>
    );
}

export default App;
