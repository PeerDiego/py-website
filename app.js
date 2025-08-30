// Python Interactive Chat - Clean and Simple

// Debug mode detection
const urlParams = new URLSearchParams(window.location.search);
const debugMode = urlParams.get('debug') === 'true';

// Early debug access
const earlyLog = window.earlyLog || (() => {});
const APP_VERSION = '2025.08.23.1'; // YYYY.MM.DD.version_number
earlyLog(`app.js v${APP_VERSION} starting initialization`);

// Add debug output div if in debug mode
let debugOutput;
if (debugMode) {
    debugOutput = document.createElement('div');
    debugOutput.id = 'debug-output';
    debugOutput.style.cssText = `
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 300px;
        height: 200px;
        background: rgba(0, 0, 0, 0.8);
        color: #00ff00;
        font-family: monospace;
        padding: 10px;
        overflow-y: auto;
        z-index: 1000;
        border: 1px solid #00ff00;
        font-size: 12px;
    `;
    document.body.appendChild(debugOutput);
}

// Wrap console methods to also output to debug div
const originalConsole = { ...console };
if (debugMode) {
    ['log', 'error', 'warn', 'info'].forEach(method => {
        console[method] = (...args) => {
            // Call original console method
            originalConsole[method](...args);
            // Add to debug output
            const text = args.map(arg => 
                typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
            ).join(' ');
            const timestamp = new Date().toLocaleTimeString();
            debugOutput.innerHTML += `<div style="color: ${method === 'error' ? '#ff0000' : method === 'warn' ? '#ffff00' : '#00ff00'}">
                [${timestamp}] ${method.toUpperCase()}: ${text}</div>`;
            debugOutput.scrollTop = debugOutput.scrollHeight;
        };
    });
}

let pyodide;
let isInitialized = false;

// Log that we're starting Pyodide setup
earlyLog('Starting Pyodide setup');

// Track global Pyodide instance
if (window.pyodide) {
    earlyLog('Found existing Pyodide instance');
    pyodide = window.pyodide;
} else {
    earlyLog('No existing Pyodide instance found');
}
let pythonProgram = '';
let isWaitingForInput = false;
let inputResolver = null;

// Get CSS custom properties for input configuration
const computedStyle = getComputedStyle(document.documentElement);
const inputType = computedStyle.getPropertyValue('--input-type').trim().replace(/['"]/g, '');
const autoAcceptNumeric = computedStyle.getPropertyValue('--auto-accept-numeric-input').trim().replace(/['"]/g, '') === 'true';

// Configure input based on CSS properties
if (inputType === 'numeric') {
    const userInput = document.getElementById('user-input');
    userInput.setAttribute('inputmode', 'numeric');
    userInput.setAttribute('pattern', '[0-9]*');
    
    // Only add auto-submit if auto-accept-numeric-input is enabled
    if (autoAcceptNumeric) {
        userInput.addEventListener('input', function(e) {
            const value = e.target.value;
            if (/^\d+$/.test(value)) {  // Check if input is numeric
                sendButton.click();  // Automatically trigger send
            }
        });
    }
}

// Import modules
earlyLog('Starting module imports...');

Promise.all([
    import('./transformInputToAsync.js')
        .then(module => {
            window.transformPythonForPyodide = module.transformPythonForPyodide;
            earlyLog('transformInputToAsync.js loaded');
        })
        .catch(err => earlyLog(`Error loading transformInputToAsync.js: ${err.message}`)),

    import('./concatenatePrints.js')
        .then(module => {
            window.concatenateConsecutivePrints = module.concatenateConsecutivePrints;
            earlyLog('concatenatePrints.js loaded');
        })
        .catch(err => earlyLog(`Error loading concatenatePrints.js: ${err.message}`)),

    import('./debugUtils.js')
        .then(module => {
            window.debug = module.debug;
            window.setDebugModules = module.setDebugModules;
            earlyLog('debugUtils.js loaded');
        })
        .catch(err => earlyLog(`Error loading debugUtils.js: ${err.message}`))
]).then(() => {
    earlyLog('All modules loaded successfully');
    // Configure which modules should show debug output after modules are loaded
    earlyLog('Configuring debug modules');
    setDebugModules({
        'app.js': true,
        'concatenatePrints.js': false,
        'transformInputToAsync.js': false,
        'storage': false
    });
}).catch(err => {
    earlyLog(`ERROR in module loading: ${err.message}`);
    if (err.stack) {
        earlyLog(`Stack trace: ${err.stack}`);
    }
});

earlyLog('Starting DOM element initialization');

// DOM elements
const chatOutput = document.getElementById('chat-output');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const runScriptButton = document.getElementById('run-script-button');
const clearButton = document.getElementById('clear-button');
const status = document.getElementById('status');
const pythonVersion = document.getElementById('python-version');
const header = document.querySelector('header');

// Log DOM element status
earlyLog('DOM elements status:');
earlyLog(`chat-output: ${chatOutput ? 'YES' : 'NO'}`);
earlyLog(`user-input: ${userInput ? 'YES' : 'NO'}`);
earlyLog(`send-button: ${sendButton ? 'YES' : 'NO'}`);
earlyLog(`run-script-button: ${runScriptButton ? 'YES' : 'NO'}`);
earlyLog(`clear-button: ${clearButton ? 'YES' : 'NO'}`);
earlyLog(`status: ${status ? 'YES' : 'NO'}`);
earlyLog(`python-version: ${pythonVersion ? 'YES' : 'NO'}`);

// Cookie utility functions
function setCookie(name, value, days = 30) {
    try {
        const expires = new Date();
        expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
        const jsonValue = JSON.stringify(value);
        debug('storage', 'Setting cookie. JSON value:', jsonValue);
        debug('storage', 'JSON length:', jsonValue.length);
        
        // More explicit cookie setting with security attributes
        const cookieValue = encodeURIComponent(jsonValue);
        const cookie = [
            `${name}=${cookieValue}`,
            `expires=${expires.toUTCString()}`,
            'path=/',
            'SameSite=Lax'
        ].join(';');
        
        debug('storage', 'Setting cookie with:', cookie);
        document.cookie = cookie;
        
        // Verify the cookie was set
        const allCookies = document.cookie;
        debug('storage', 'All cookies after set:', allCookies);
        debug('storage', 'Cookie set complete');
    } catch (e) {
        console.error('Error in setCookie:', e);
        throw e;
    }
}

function getCookie(name) {
    debug('storage', 'Getting cookie:', name);
    debug('storage', 'All cookies:', document.cookie);
    
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    debug('storage', 'Cookie array:', ca);
    
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) {
            try {
                const encodedValue = c.substring(nameEQ.length, c.length);
                const decodedValue = decodeURIComponent(encodedValue);
                debug('storage', 'Found cookie value:', decodedValue);
                return JSON.parse(decodedValue);
            } catch(e) {
                debug('storage', 'Error parsing cookie:', e);
                return null;
            }
        }
    }
    debug('storage', 'Cookie not found');
    return null;
}

function deleteCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
}

// Data persistence bridge functions
function saveAppData(data, key = 'app_data') {
    // Convert Python object to JavaScript object if needed
    let jsData;
    debug('storage', 'saveAppData received:', data);
    debug('storage', 'data type:', typeof data);
    debug('storage', 'data toJs exists:', typeof data.toJs === 'function');
    
    try {
        if (data && typeof data.toJs === 'function') {
            // If it's a PyProxy object with toJs method, convert it
            debug('storage', 'Converting PyProxy to JS...');
            jsData = data.toJs({dict_converter: Object.fromEntries});
            debug('storage', 'Conversion result:', jsData);
        } else {
            // Otherwise assume it's already a JavaScript object
            jsData = data;
        }
        
        // Try to save both ways for maximum reliability
        debug('storage', 'About to set cookie with:', jsData);
        setCookie(key, jsData);
        
        // Also save to localStorage as backup
        try {
            localStorage.setItem(key, JSON.stringify(jsData));
            debug('storage', 'Saved to localStorage');
        } catch (storageErr) {
            debug('storage', 'Could not save to localStorage:', storageErr);
        }
        
        // Verify the save
        const savedCookie = getCookie(key);
        const savedStorage = localStorage.getItem(key);
        debug('storage', 'Verification - Cookie:', savedCookie);
        debug('storage', 'Verification - localStorage:', savedStorage);
        
        return true; // Return success indicator
    } catch (e) {
        console.error('Error in saveAppData:', e);
        return false;
    }
}

function loadAppData(key = 'app_data') {
    // Try localStorage first
    let savedData = null;
    try {
        const storageData = localStorage.getItem(key);
        if (storageData) {
            savedData = JSON.parse(storageData);
            debug('storage', `App data loaded from localStorage (${key}):`, savedData);
        }
    } catch (e) {
        debug('storage', 'Error loading from localStorage:', e);
    }
    
    // If localStorage failed, try cookie as fallback
    if (!savedData) {
        savedData = getCookie(key);
        debug('storage', `App data loaded from cookie (${key}):`, savedData);
    }
    
    // Return the data as-is - it should be a proper JavaScript object
    // that Python can convert using .to_py()
    return savedData;
}

function clearAppData(key = 'app_data') {
    deleteCookie(key);
    debug('storage', `App data cleared from cookie (${key})`);
    return true; // Return success indicator
}

// Initialize Pyodide
async function initializePyodide() {
    try {
        // Early environment detection
        console.log('Environment Check:', {
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            vendor: navigator.vendor,
            isSafari: /^((?!chrome|android).)*safari/i.test(navigator.userAgent),
            isIOS: /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)
        });

        // Check if we're on iOS and warn about potential issues
        if (/iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) {
            console.warn('iOS device detected - checking WebAssembly support...');
            if (typeof WebAssembly === 'object') {
                console.log('WebAssembly is supported');
                // Check for streaming support
                if (typeof WebAssembly.instantiateStreaming === 'function') {
                    console.log('WebAssembly streaming is supported');
                } else {
                    console.warn('WebAssembly streaming is not supported - this may cause issues');
                }
            } else {
                console.error('WebAssembly is not supported on this device');
                throw new Error('WebAssembly is required but not supported on this device');
            }
        }

        console.log('Loading Pyodide...');
        addMessage('system', 'Initializing Python environment... Please wait.');
        status.textContent = 'Loading Pyodide...';
        
        pyodide = await loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/"
        });
        
        console.log('Loading Python program...');
        await loadPythonProgram();
        
        console.log('Setting up Python environment...');
        // Set up print and input overrides
        pyodide.globals.set('js_print', displayPythonOutput);
        pyodide.globals.set('js_input', getUserInput);
        
        // Set up data persistence functions (for cookie save/load)
        pyodide.globals.set('js_save_data', saveAppData);
        pyodide.globals.set('js_load_data', loadAppData);
        pyodide.globals.set('js_clear_data', clearAppData);
        
        await pyodide.runPythonAsync(`
import builtins
import asyncio

# Get JS functions
js_print = globals()['js_print']
js_input = globals()['js_input']

# Get data persistence functions
js_save_data = globals()['js_save_data']
js_load_data = globals()['js_load_data']
js_clear_data = globals()['js_clear_data']

# Override print
def new_print(*args, msg_type='python', **kwargs):
    text = ' '.join(str(arg) for arg in args)
    js_print(text, msg_type)
    # Also log to browser console for debugging
    from js import console
    console.log(f"Python print: {text} (type: {msg_type})")

# Override input - this will work with await in the async context
async def new_input(prompt=""):
    result = await js_input(str(prompt) if prompt else "")
    return str(result) if result is not None else ""

# Override time.sleep with async version
async def new_sleep(seconds):
    await asyncio.sleep(seconds)

builtins.print = new_print
builtins.input = new_input

# Use JS functions directly for simple pass-throughs (they already have default parameters)
builtins.save_data = js_save_data
builtins.clear_data = js_clear_data

# Create Python wrapper function only for load_data since it does meaningful data conversion
def load_data(key='app_data'):
    """Load data from browser cookies and convert to Python dict"""
    js_data = js_load_data(key)
    if js_data is None:
        return None
    
    # Convert JsProxy to Python object using to_py()
    try:
        # Check if it's a JsProxy object with to_py method
        if hasattr(js_data, 'to_py'):
            return js_data.to_py()
        else:
            # If it's already a Python object, return as-is
            return js_data
    except Exception as e:
        print(f"Error converting JS data to Python: {e}")
        return None

# Make the load_data wrapper available globally
builtins.load_data = load_data

# Override time.sleep when time module is imported
import time
time.sleep = new_sleep

PYODIDE_ENV = True
print("Game loaded...")
        `);
        
        isInitialized = true;
        status.textContent = 'Python environment ready!';
        status.className = '';
        pythonVersion.textContent = `Python ${pyodide.runPython('import sys; sys.version.split()[0]')}`;
        
        userInput.disabled = false;
        sendButton.disabled = false;
        runScriptButton.disabled = false;
        userInput.placeholder = 'Type a message...';
        
        addMessage('system', 'Python environment initialized successfully! Click "Play Game" to start.');
        
        // Focus the run button and add keyboard listener
        runScriptButton.focus();
        
    } catch (error) {
        console.error('Initialization error:', error);
        status.textContent = 'Failed to load Python environment';
        addMessage('error', `Failed to initialize Python environment: ${error.message}`);
    }
}

// Load Python program
async function loadPythonProgram() {
    try {
        // Get the filename from the hidden input in the HTML
        const filename = document.getElementById('python-file').value || 'main.py';
        const response = await fetch(filename);
        if (response.ok) {
            let rawCode = await response.text();
            // Transform the code to async/await style
            let transformedCode = transformPythonForPyodide(rawCode);
            console.log(`Loaded and transformed ${filename} successfully.`);
            debug('app.js', `Transform Python code for Pyodide, pre-print-concatenation:\n${transformedCode}`);
            // Further optimize by concatenating consecutive print statements
            pythonProgram = concatenateConsecutivePrints(transformedCode);
            debug('app.js', `Transform Python code for Pyodide:\n${pythonProgram}`);
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        addMessage('error', `Error: ${error}\nUsing fallback python program`);
        pythonProgram = `
print("🎉 Welcome to Python Interactive Chat!")

name = await input("What's your name? ")
print(f"Hello, {name}! Nice to meet you!")

age = await input("How old are you? ")
print(f"You are {age} years old.")

print("Thanks for testing the interactive chat!")
        `;
    }
}

// Add message to chat
function addMessage(type, content, timestamp = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    const timestampDiv = document.createElement('div');
    timestampDiv.className = 'timestamp';
    timestampDiv.textContent = timestamp || new Date().toLocaleTimeString();
    
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timestampDiv);
    chatOutput.appendChild(messageDiv);
    
    chatOutput.scrollTop = chatOutput.scrollHeight;
}

// Display Python output
function displayPythonOutput(text, type = 'python') {
    addMessage(type, text);
}

// Get user input (called from Python)
function getUserInput(prompt) {
    return new Promise((resolve) => {
        console.log('getUserInput called with prompt:', prompt);
        
        // Add the prompt message to the chat
        if (prompt && prompt.trim()) {
            addMessage('system', prompt);
        }
        
        // Set up the input waiting state
        isWaitingForInput = true;
        userInput.placeholder = 'Enter your response...';
        userInput.disabled = false;
        userInput.focus();
        
        // Set up the callback for when user submits input
        inputResolver = (value) => {
            console.log('Input received:', value || "(empty input)");
            isWaitingForInput = false;
            userInput.placeholder = 'Type a message...';
            inputResolver = null;
            resolve(value || '');
        };
    });
}

// Run Python program
async function runPythonProgram() {
    if (!isInitialized || !pythonProgram) {
        addMessage('error', 'Python environment or program not ready.');
        return;
    }
    
    // Disable the Play Game button once clicked
    runScriptButton.disabled = true;
    
    // Add compact header class for mobile/tablet views
    header.classList.add('game-running');
    
    // swapping for a debug message instead
    // addMessage('system', 'Starting Python program...');
    debug('app.js', 'Starting Python program...');
    // changes status message from "Python environment ready!" to "Good luck!"
    // status.id=""; // removing #status id to let color be dictated by status-running class
    status.className = 'status-running-rainbox';
    status.innerHTML = 'Good luck!';
    pythonVersion.innerHTML = 'Brought to you by <a href="http://www.lazyspaniard.com" target="_blank">Lazy Spaniard</a>'
    
    try {
        // Wrap the transformed program in an async function
        // This allows synchronous Python input() and time.sleep() calls to work with async JavaScript Promises
        const asyncProgram = `
async def main():
${pythonProgram.split('\n').map(line => '    ' + line).join('\n')}

await main()
        `;
        
        await pyodide.runPythonAsync(asyncProgram);

        // Re-enable the Play Game button and restore header
        runScriptButton.disabled = false;
        header.classList.remove('game-running');
        addMessage('system', 'Game finished. Click "Play Game" to start again.');
        runScriptButton.focus();
    } catch (error) {
        console.error('Program execution error:', error);
        addMessage('error', `Program error: ${error.message}`);
    }
}

// Handle user input
function handleUserInput() {
    const input = userInput.value.trim();
    
    // Only proceed if we're waiting for input from Python
    if (isWaitingForInput && inputResolver) {
        if (input) addMessage('user', input);
        userInput.value = '';
        inputResolver(input);
        return;
    }
    
    // If not waiting for input, inform user
    if (input) {
        addMessage('user', input);
        userInput.value = '';
        addMessage('system', 'No input expected right now. Click "Play Game" to start the game.');
    }
}

// Clear chat
function clearChat() {
    chatOutput.innerHTML = '<div class="message system-message"><div class="message-content"><strong>System:</strong> Chat cleared.</div><div class="timestamp">' + new Date().toLocaleTimeString() + '</div></div>';
}

// Event listeners
sendButton.addEventListener('click', handleUserInput);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleUserInput();
    }
});

runScriptButton.addEventListener('click', runPythonProgram);
clearButton.addEventListener('click', clearChat);

// Initialize on page load
// Early error handler
window.addEventListener('error', function(event) {
    console.error('Global error:', {
        message: event.message,
        source: event.filename,
        lineNo: event.lineno,
        colNo: event.colno,
        error: event.error
    });
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled Promise rejection:', {
        reason: event.reason
    });
});

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Starting initialization...');
    try {
        initializePyodide().catch(err => {
            console.error('Failed to initialize Pyodide:', err);
            status.textContent = 'Failed to initialize: ' + err.message;
            addMessage('error', `Initialization failed: ${err.message}`);
        });
    } catch (err) {
        console.error('Critical initialization error:', err);
        status.textContent = 'Critical error: ' + err.message;
        addMessage('error', `Critical error: ${err.message}`);
    }
});