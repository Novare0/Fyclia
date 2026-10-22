const DEFAULT_CONFIG = {
    minInterval: 62000,
    maxInterval: 122000,
    targetDomain: 'lat.fictionexpress.com',
    enabled: true,
    downloadEnabled: true,
    apiBaseUrl: 'http://127.0.0.1:8765'
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = DEFAULT_CONFIG;
}
