import React, { useRef, useEffect, useState } from 'react';
import BylawToggle from './BylawToggle.jsx';
import ZoomModal from './ZoomModal.jsx';
import mapboxgl from 'mapbox-gl'; // eslint-disable-line import/no-webpack-loader-syntax
import axios from "axios";
mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_API_KEY;


function App() {
    const mapContainer = useRef(null);
    const map = useRef(null);
    const [lng, setLng] = useState(-79.3832);
    const [lat, setLat] = useState(43.6532);
    const [zoom, setZoom] = useState(14);
    const [npBylaws, setNpBylaws] = useState([]);
    const [rpBylaws, setRpBylaws] = useState([]);
    const [loading, setLoading] = useState(true);
    const [npBylawMarkers, setNpBylawMarkers] = useState([]);
    const [rpBylawMarkers, setRpBylawMarkers] = useState([]);
    const [markersShown, setMarkersShown] = useState(false);

    const fetchNpData = async (currLat, currLng) => {
        try {
            const response = await axios.get(`/api/bylaws/?type=np&lat=${currLat}&lng=${currLng}`);
            const result = await response.data;
            setNpBylaws(result);
            setLoading(false);
        } catch (error) {
            console.error("Error fetching no parking bylaws", error);
            setLoading(false);
        }
    };

    const fetchRpData = async (currLat, currLng) => {
        try {
            const response = await axios.get(`/api/bylaws/?type=rp&lat=${currLat}&lng=${currLng}`);
            const result = await response.data;
            setRpBylaws(result);
            setLoading(false);
        } catch (error) {
            console.log("Error fetching restricted parking bylaws", error);
            setLoading(false);
        }
    };

    useEffect(() => {
        if (map.current) return;
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v12',
            center: [lng, lat],
            zoom: zoom
        });
        fetchNpData(lat, lng);
        fetchRpData(lat, lng);

        // handle map markers when zoom is changed
        map.current.on("zoomend", () => {
            const updatedZoom = map.current.getZoom().toFixed(2);
            setZoom(map.current.getZoom().toFixed(2));

            if (updatedZoom <= 13 && (npBylawMarkers.length > 0 || rpBylawMarkers.length > 0)) {
                removeMarkers(npBylawMarkers);
                removeMarkers(rpBylawMarkers);
            } else if (!markersShown && updatedZoom > 13) {
                addMarkers(npBylawMarkers);
                addMarkers(rpBylawMarkers);
            } 
        })
        map.current.on("moveend", () => {
            const updatedLat = map.current.getCenter().lat.toFixed(4);
            const updatedLng = map.current.getCenter().lng.toFixed(4)
            setLng(updatedLng);
            setLat(updatedLng);
            const updatedZoom = map.current.getZoom().toFixed(2);
            if (updatedZoom > 13) {
                fetchNpData(updatedLat, updatedLng); // only fetch data based on current lat/lng and radius
                fetchRpData(updatedLat, updatedLng); // only fetch data based on current lat/lng and radius
            }
        });
    }, []);

    useEffect(() => {
        if(!loading && npBylaws && rpBylaws && npBylaws.results && rpBylaws.results) {
            removeMarkers(npBylawMarkers);
            removeMarkers(rpBylawMarkers);
            const updatedZoom = map.current.getZoom().toFixed(2);
            if (updatedZoom > 13){
                setNpBylawMarkers(createMarkers(npBylaws, true));
                setRpBylawMarkers(createMarkers(rpBylaws, false));
            }
        }
    }, [loading, npBylaws, rpBylaws])

    const createMarkers = (bylaws, isNpBylaws) => {
        const markers = bylaws.results.map((bylaw) => {
            let popup = createPopup(bylaw);
            const color = isNpBylaws ? "#ff0000" : "#50C878";
            let marker_a = new mapboxgl.Marker({color: color})
                .setLngLat([bylaw.midpoint[1], bylaw.midpoint[0]])
                .setPopup(popup)
                .addTo(map.current)
            return marker_a
        })
        setMarkersShown(true);
        return markers
    }

    const formatBylawName = (bylaw) => {
        if (bylaw.schedule === "13"){
            return "No Parking";
        }
        return "Free Parking";
    }

    const capitalize = (sentence) => {
        if (sentence === null){
            return ""
        }
        const words = sentence.trim().split(" ");
        const capitalizedWords = words.map((word) => {
            let firstLetter = word[0];
            if (!word.startsWith("a.m.") && !word.startsWith("p.m.")){
                firstLetter = word[0].toUpperCase();
            }
            return firstLetter + word.substring(1);
        });
        return capitalizedWords.join(" ");
    }

    const formatBylawStreetDetail = (bylaw) => {
        const streetDetailText = `${capitalize(bylaw.highway.name)}, \
                                    ${bylaw.side} side, \
                                    between ${capitalize(bylaw.between)}`;
        return streetDetailText;
    }

    const getPopupHTML = (bylaw) => {
       let popup = `<div class="popup">
                        <h2 class="popup-title">${formatBylawName(bylaw)}</h2>
                        <p class="street-detail">${formatBylawStreetDetail(bylaw)}</p>
                        <p class="time-range">${capitalize(bylaw.times_and_or_days)}</p>`

        if (bylaw.schedule === "15") {
            popup += `<p class="max-time-permitted"><strong>Max Time Permitted: </strong>\
                        ${bylaw.max_period_permitted}</p>`
        }
        popup += `</div>`;
        return popup;
    }
    const createPopup = (bylaw) => {
        const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(getPopupHTML(bylaw));
        return popup
    }
    const addMarkers = (bylawMarkers) => {
        bylawMarkers.forEach((marker) => {
            marker.addTo(map.current);
        })
        setMarkersShown(true);
    }
    const removeMarkers = (bylawMarkers) => {
        bylawMarkers.forEach((marker) => {
            marker.remove();
        })
        setMarkersShown(false);
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
            <ZoomModal zoom={zoom}></ZoomModal>
            <div ref={mapContainer} className="map-container" />
        </div>
    );
}

export default App;
