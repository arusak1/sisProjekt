import React, { useState, useEffect } from 'react';

const ScanAll = () => {
    const [results, setResults] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchScanResults = async () => {
        try {
            setLoading(true);
            setError(null);

            const response = await fetch('http://127.0.0.1:5001/api/scanAll');
            const data = await response.json();
            setResults(data.scanAll_result);
        } catch (error) {
            console.error('Error fetching scan results:', error);
            setError('An error occurred while fetching scan results.');
        } finally {
            setLoading(false);
        }
    };

    const handleStartScan = async () => {
        await fetchScanResults();
    };

    useEffect(() => {
        fetchScanResults();
        const intervalId = setInterval(fetchScanResults, 300000); 

        return () => clearInterval(intervalId);
    }, []);

    return (
        <div>
            <h2>Scan Results:</h2>
            <button onClick={handleStartScan} disabled={loading}>
                {loading ? 'Scanning...' : 'Start Scan'}
            </button>
            {loading ? (
                <p>Loading scans... <span role="img" aria-label="Loading">⌛</span></p>
            ) : (
                <>
                    {error ? (
                        <p>Error fetching scan results: {error}</p>
                    ) : (
                        <pre>{results}</pre>
                    )}
                </>
            )}
        </div>
    );
};

export default ScanAll;
