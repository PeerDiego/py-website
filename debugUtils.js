// debugUtils.js
// Shared debug logging utilities

const debugSettings = {
    'app.js': false,
    'concatenatePrints.js': false,
    'transformInputToAsync.js': false
};

/**
 * Debug logging utility that checks if debugging is enabled for the calling module
 * @param {string} moduleName - The name of the module (e.g., 'app.js')
 * @param {...any} args - Arguments to log
 */
export function debug(moduleName, ...args) {
    if (debugSettings[moduleName]) {
        console.log(`[${moduleName}]`, ...args);
    }
}

/**
 * Enable or disable debug logging for specific modules
 * @param {Object} settings - Object with module names as keys and boolean values
 */
export function setDebugModules(settings) {
    Object.assign(debugSettings, settings);
}

// Get current debug settings
export function getDebugSettings() {
    return { ...debugSettings };
}
