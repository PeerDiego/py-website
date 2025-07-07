// transformInputToAsync.js
// Node.js script to transform Python functions using input() to async/await style
// Usage: node transformInputToAsync.js <python_file.py>

let fs, path, fileURLToPath;
if (typeof process !== 'undefined' && process.versions && process.versions.node) {
    // We're in Node.js
    // ES6 import syntax
    // This allows the script to be used as a module in other scripts or run directly
    // Only import Node.js modules if we're running in Node.js
    fs = (await import('fs')).default;
    path = (await import('path')).default;
    fileURLToPath = (await import('url')).fileURLToPath;
}

function findFunctionsWithInput(code) {
    const lines = code.split(/\r?\n/);
    const functionRegex = /^([ \t]*)def\s+(\w+)\s*\([^)]*\):/;
    const results = [];
    for (let i = 0; i < lines.length; i++) {
        const match = lines[i].match(functionRegex);
        if (match) {
            const [_, indent, name] = match;
            // Collect the function body (naive: until next non-indented line or EOF)
            let bodyLines = [];
            let j = i + 1;
            while (j < lines.length && (/^\s/.test(lines[j]) || lines[j].trim() === '')) {
                bodyLines.push(lines[j]);
                j++;
            }
            const bodyNoComments = bodyLines.join('\n').replace(/#.*$/gm, '');
            if (/\binput\s*\(/.test(bodyNoComments)) {
                results.push({ name, line: i + 1 });
            }
        }
    }
    return results;
}

function findFunctionCalls(code, functionNames) {
    const lines = code.split(/\r?\n/);
    const calls = {};
    
    // Initialize all function names with empty arrays
    for (const name of functionNames) {
        calls[name] = [];
    }
    
    lines.forEach((line, idx) => {
        for (const name of functionNames) {
            // More robust regex that handles function calls better
            const callRegex = new RegExp(`(?<!def\\s+)\\b${name}\\s*\\(`, 'g');
            let match;
            while ((match = callRegex.exec(line)) !== null) {
                calls[name].push({ line: idx + 1, text: line.trim() });
            }
        }
    });
    
    return calls;
}

function transformPythonCode(code, functionInfos, calls) {
    // functionInfos: [{ name, line }]
    let lines = code.split(/\r?\n/);
    
    // Insert 'async' before 'def' for each function definition line
    for (const fn of functionInfos) {
        const idx = fn.line - 1;
        if (idx >= 0 && idx < lines.length && !/^\s*async\s+def\b/.test(lines[idx])) {
            lines[idx] = lines[idx].replace(/^(\s*)def\b/, '$1async def');
        }
    }
    
    // Now add 'await' to function calls
    for (const fn of functionInfos) {
        const fnEscaped = fn.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        // Check if calls[fn.name] exists and has elements
        if (calls[fn.name] && calls[fn.name].length > 0) {
            for (const call of calls[fn.name]) {
                const idx = call.line - 1;
                if (idx >= 0 && idx < lines.length && !/\bawait\s+/.test(lines[idx])) {
                    lines[idx] = lines[idx].replace(new RegExp(`\\b${fnEscaped}\\s*\\(`), `await ${fn.name}(`);
                }
            }
        }
    }
    
    // Transform all input() calls to await input() calls
    // This handles input() calls that aren't inside async functions
    for (let i = 0; i < lines.length; i++) {
        // Only add await if it's not already there
        if (/\binput\s*\(/.test(lines[i]) && !/\bawait\s+input\s*\(/.test(lines[i])) {
            lines[i] = lines[i].replace(/\binput\s*\(/g, 'await input(');
        }
    }
    
    // Also transform time.sleep() calls to await time.sleep() calls
    for (let i = 0; i < lines.length; i++) {
        // Only add await if it's not already there
        if (/\btime\.sleep\s*\(/.test(lines[i]) && !/\bawait\s+time\.sleep\s*\(/.test(lines[i])) {
            lines[i] = lines[i].replace(/\btime\.sleep\s*\(/g, 'await time.sleep(');
        }
    }
    
    return lines.join('\n');
}

// Main function to transform Python code for Pyodide compatibility
function transformPythonForPyodide(code) {
    const foundFunctions = findFunctionsWithInput(code);
    const functionNames = foundFunctions.map(f => f.name);
    const calls = findFunctionCalls(code, functionNames);
    return transformPythonCode(code, foundFunctions, calls);
}

// Export for use in other scripts using ES6 syntax. module.exports = { ... }; won't work
export { transformPythonForPyodide };

// If run directly, process a file or sample code (Node.js only)
if (typeof process !== 'undefined' && process.versions && process.versions.node) {
    const __filename = fileURLToPath(import.meta.url);
    if (process.argv[1] === __filename) {
        const filename = process.argv[2];
        let pythonCode;
        
        if (filename) {
            try {
                const filePath = path.resolve(process.cwd(), filename);
                pythonCode = fs.readFileSync(filePath, 'utf8');
                console.log(`Loaded Python code from: ${filePath}`);
            } catch (err) {
                console.error(`Error reading file '${filename}':`, err.message);
                process.exit(1);
            }
        } else {
            pythonCode = `def menu(title, options):
    print(f"\\n{title}")
    for i, (label, _) in enumerate(options, 1):
        print(f"  {i}. {label}")
    while True:
        try:
            choice = int(input("Choose: "))
            if 1 <= choice <= len(options):
                return options[choice-1][1]
        except ValueError:
            pass
        print("Invalid choice. Try again.")

def foo():
    print("No input here!")

def bar():
    x = input("Enter something: ")
    return x

def baz():
    # input() in a comment should not count
    pass

def qux():
    if True:
        input("Nested input!")

# Test calls
menu("Test Menu", [("Option 1", lambda: None)])
bar()
foo()
qux()`;
        }
        
        console.log('=== Original Code ===');
        console.log(pythonCode);
        console.log('\n=== Analysis ===');
        
        const foundFunctions = findFunctionsWithInput(pythonCode);
        console.log('Functions containing input():', foundFunctions);
        
        if (foundFunctions.length > 0) {
            const functionNamesArray = foundFunctions.map(f => f.name);
            const calls = findFunctionCalls(pythonCode, functionNamesArray);
            
            console.log('\n=== Function Call Analysis ===');
            for (const fn of foundFunctions) {
                console.log(`\nCalls to function '${fn.name}':`);
                if (!calls[fn.name] || calls[fn.name].length === 0) {
                    console.log('  (No calls found)');
                } else {
                    for (const call of calls[fn.name]) {
                        console.log(`  Line ${call.line}: ${call.text}`);
                    }
                }
            }
            
            // const transformed = transformPythonCode(pythonCode, foundFunctions, calls);
            // refactoring to this:
            const transformed = transformPythonForPyodide(pythonCode);
            console.log('\n=== Transformed Code ===');
            console.log(transformed);
        } else {
            console.log('No functions with input() found.');
        }
    }
}