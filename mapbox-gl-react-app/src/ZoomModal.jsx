function ZoomModal({zoom}) {
    const style = zoom <= 13
        ? undefined
        : { display: 'none' };

    return (
        <div className="zoomModal" style={style}>Zoom in to search street parking</div>
    )
}

export default ZoomModal;
