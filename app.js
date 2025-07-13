// Python Interactive Chat - Clean and Simple
let pyodide;
let isInitialized = false;
let pythonProgram = '';
let isWaitingForInput = false;
let inputResolver = null;

// Import from the transformInputToAsync module
import { transformPythonForPyodide } from './transformInputToAsync.js';
// Import from the concatenatePrints module
import { concatenateConsecutivePrints } from './concatenatePrints.js';
// Import debug utilities
import { debug, setDebugModules } from './debugUtils.js';

// Configure which modules should show debug output
setDebugModules({
    'app.js': true,
    'concatenatePrints.js': false,
    'transformInputToAsync.js': false
});

// DOM elements
const chatOutput = document.getElementById('chat-output');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const runScriptButton = document.getElementById('run-script-button');
const clearButton = document.getElementById('clear-button');
const status = document.getElementById('status');
const pythonVersion = document.getElementById('python-version');

// Initialize Pyodide
async function initializePyodide() {
    try {
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
        
        await pyodide.runPythonAsync(`
import builtins
import asyncio

# Get JS functions
js_print = globals()['js_print']
js_input = globals()['js_input']

# Override print
def new_print(*args, **kwargs):
    text = ' '.join(str(arg) for arg in args)
    js_print(text)
    # Also log to browser console for debugging
    from js import console
    console.log(f"Python print: {text}")

# Override input - this will work with await in the async context
async def new_input(prompt=""):
    result = await js_input(str(prompt) if prompt else "")
    return str(result) if result is not None else ""

# Override time.sleep with async version
async def new_sleep(seconds):
    await asyncio.sleep(seconds)

builtins.print = new_print
builtins.input = new_input

# Override time.sleep when time module is imported
import time
time.sleep = new_sleep

print("Python environment ready!")
        `);
        
        isInitialized = true;
        status.textContent = 'Python environment ready!';
        status.className = '';
        pythonVersion.textContent = `Python ${pyodide.runPython('import sys; sys.version.split()[0]')}`;
        
        userInput.disabled = false;
        sendButton.disabled = false;
        runScriptButton.disabled = false;
        userInput.placeholder = 'Type a message...';
        
        addMessage('system', 'Python environment initialized successfully! Click "Run Python Program" to start the interactive program.');
        
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
            debug('app.js', transformedCode);
            // Further optimize by concatenating consecutive print statements
            pythonProgram = concatenateConsecutivePrints(transformedCode);
            debug('app.js', `Concatenate consecutive print statements successfully:\n${pythonProgram}`);
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.log('Using fallback program');
        pythonProgram = `
print("🎉 Welcome to Python Interactive Chat!")

name = input("What's your name? ")
print(f"Hello, {name}! Nice to meet you!")

age = input("How old are you? ")
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
function displayPythonOutput(text) {
    addMessage('python', text);
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
    
    addMessage('system', 'Starting Python program...');
    
    try {
        // Wrap the transformed program in an async function
        // This allows synchronous Python input() and time.sleep() calls to work with async JavaScript Promises
        const asyncProgram = `
async def main():
${pythonProgram.split('\n').map(line => '    ' + line).join('\n')}

await main()
        `;
        
        await pyodide.runPythonAsync(asyncProgram);
        addMessage('system', 'Program finished. Click "Run Python Program" to start again.');
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
        addMessage('system', 'No input expected right now. Click "Run Python Program" to start the program.');
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
document.addEventListener('DOMContentLoaded', () => {
    initializePyodide();
});