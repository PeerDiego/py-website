// transformInputToAsync.js
// Node.js script to transform Python functions using input() to async/await style
// Usage: node transformInputToAsync.js <python_file.py>

// List of additional function names that should be transformed to use await
const ALSO_TRANSFORM = ["custom_function_name"];  // Add function names without parentheses

import { debug } from './debugUtils.js';
const MODULE_NAME = 'transformInputToAsync.js';

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

function findFunctionsWithInputOrSleep(code) {
    debug(MODULE_NAME, '=== findFunctionsWithInputOrSleep START ===');
    const lines = code.split(/\r?\n/);
    debug(MODULE_NAME, `Processing ${lines.length} lines of code`);
    const functionRegex = /^([ \t]*)def\s+(\w+)\s*\([^)]*\):/;
    const results = [];
    
    for (let i = 0; i < lines.length; i++) {
        const match = lines[i].match(functionRegex);
        if (match) {
            const [_, indent, name] = match;
            debug(MODULE_NAME, `Found function '${name}' at line ${i + 1} with indent '${indent}'`);
            
            // Collect the function body (naive: until next non-indented line or EOF)
            let bodyLines = [];
            let j = i + 1;
            while (j < lines.length && (/^\s/.test(lines[j]) || lines[j].trim() === '')) {
                bodyLines.push(lines[j]);
                j++;
            }
            const bodyNoComments = bodyLines.join('\n').replace(/#.*$/gm, '');
            debug(MODULE_NAME, `Function '${name}' body has ${bodyLines.length} lines`);
            
            // Check for built-in async calls (input and sleep)
            const hasInput = /\binput\s*\(/.test(bodyNoComments);
            const hasSleep = /\btime\.sleep\s*\(/.test(bodyNoComments);
            
            // Check for additional transforms from configuration
            const customTransforms = ALSO_TRANSFORM.map(fnName => {
                return {
                    name: fnName,
                    // More precise regex that only matches function calls
                    has: new RegExp(`(?<!["'\`])\\b${fnName}\\s*\\(`).test(bodyNoComments)
                };
            });
            
            const hasCustom = customTransforms.some(t => t.has);
            
            // Debug output
            const checks = [
                `hasInput=${hasInput}`,
                `hasSleep=${hasSleep}`,
                ...customTransforms.map(t => `has${t.name}=${t.has}`)
            ].join(', ');
            debug(MODULE_NAME, `Function '${name}': ${checks}`);
            
            if (hasInput || hasSleep || hasCustom) {
                const reason = [
                    hasInput && 'input()',
                    hasSleep && 'time.sleep()',
                    ...customTransforms.filter(t => t.has).map(t => `${t.name}()`)
                ].filter(Boolean).join(', ');
                debug(MODULE_NAME, `✓ Adding function '${name}' to results (contains ${reason})`);
                results.push({ name, line: i + 1 });
            } else {
                debug(MODULE_NAME, `✗ Skipping function '${name}' (no async calls found)`);
            }
        }
    }
    
    debug(MODULE_NAME, `=== findFunctionsWithInputOrSleep END: Found ${results.length} functions ===`);
    return results;
}

function findFunctionCalls(code, functionNames) {
    debug(MODULE_NAME, '=== findFunctionCalls START ===');
    debug(MODULE_NAME, `Looking for calls to functions: ${functionNames.join(', ')}`);
    const lines = code.split(/\r?\n/);
    const calls = {};
    
    // Initialize all function names with empty arrays
    for (const name of functionNames) {
        calls[name] = [];
        debug(MODULE_NAME, `Initialized call tracking for function '${name}'`);
    }
    
    lines.forEach((line, idx) => {
        for (const name of functionNames) {
            // More robust regex that handles function calls better
            const callRegex = new RegExp(`(?<!def\\s+)\\b${name}\\s*\\(`, 'g');
            let match;
            while ((match = callRegex.exec(line)) !== null) {
                debug(MODULE_NAME, `Found call to '${name}' at line ${idx + 1}: ${line.trim()}`);
                calls[name].push({ line: idx + 1, text: line.trim() });
            }
        }
    });
    
    debug(MODULE_NAME, '=== findFunctionCalls SUMMARY ===');
    for (const [name, callList] of Object.entries(calls)) {
        debug(MODULE_NAME, `Function '${name}': ${callList.length} calls found`);
    }
    debug(MODULE_NAME, '=== findFunctionCalls END ===');
    
    return calls;
}

function transformPythonCode(code, functionInfos, calls) {
    debug(MODULE_NAME, '=== transformPythonCode START ===');
    debug(MODULE_NAME, `Transforming code with ${functionInfos.length} async functions`);
    
    // functionInfos: [{ name, line }]
    let lines = code.split(/\r?\n/);
    debug(MODULE_NAME, `Code has ${lines.length} lines`);
    
    // Insert 'async' before 'def' for each function definition line
    debug(MODULE_NAME, '--- Adding async keywords to function definitions ---');
    for (const fn of functionInfos) {
        const idx = fn.line - 1;
        if (idx >= 0 && idx < lines.length && !/^\s*async\s+def\b/.test(lines[idx])) {
            const oldLine = lines[idx];
            lines[idx] = lines[idx].replace(/^(\s*)def\b/, '$1async def');
            debug(MODULE_NAME, `Line ${fn.line}: '${oldLine}' → '${lines[idx]}'`);
        } else {
            debug(MODULE_NAME, `Skipping line ${fn.line}: already async or invalid index`);
        }
    }
    
    // Now add 'await' to function calls
    debug(MODULE_NAME, '--- Adding await to function calls ---');
    for (const fn of functionInfos) {
        const fnEscaped = fn.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        // Check if calls[fn.name] exists and has elements
        if (calls[fn.name] && calls[fn.name].length > 0) {
            debug(MODULE_NAME, `Processing ${calls[fn.name].length} calls to function '${fn.name}'`);
            for (const call of calls[fn.name]) {
                const idx = call.line - 1;
                if (idx >= 0 && idx < lines.length && !/\bawait\s+/.test(lines[idx])) {
                    const oldLine = lines[idx];
                    lines[idx] = lines[idx].replace(new RegExp(`\\b${fnEscaped}\\s*\\(`), `await ${fn.name}(`);
                    debug(MODULE_NAME, `Line ${call.line}: '${oldLine}' → '${lines[idx]}'`);
                } else {
                    debug(MODULE_NAME, `Skipping call at line ${call.line}: already has await or invalid`);
                }
            }
        } else {
            debug(MODULE_NAME, `No calls found for function '${fn.name}'`);
        }
    }
    
    // Transform all input() calls to await input() calls
    debug(MODULE_NAME, '--- Adding await to input() calls ---');
    let inputTransforms = 0;
    for (let i = 0; i < lines.length; i++) {
        // Only add await if it's not already there
        if (/\binput\s*\(/.test(lines[i]) && !/\bawait\s+input\s*\(/.test(lines[i])) {
            const oldLine = lines[i];
            lines[i] = lines[i].replace(/\binput\s*\(/g, 'await input(');
            debug(MODULE_NAME, `Line ${i + 1}: '${oldLine}' → '${lines[i]}'`);
            inputTransforms++;
        }
    }
    debug(MODULE_NAME, `Applied await to ${inputTransforms} input() calls`);
    
    // Also transform time.sleep() calls to await time.sleep() calls
    debug(MODULE_NAME, '--- Adding await to time.sleep() calls ---');
    let sleepTransforms = 0;
    for (let i = 0; i < lines.length; i++) {
        // Only add await if it's not already there
        if (/\btime\.sleep\s*\(/.test(lines[i]) && !/\bawait\s+time\.sleep\s*\(/.test(lines[i])) {
            const oldLine = lines[i];
            lines[i] = lines[i].replace(/\btime\.sleep\s*\(/g, 'await time.sleep(');
            debug(MODULE_NAME, `Line ${i + 1}: '${oldLine}' → '${lines[i]}'`);
            sleepTransforms++;
        }
    }
    debug(MODULE_NAME, `Applied await to ${sleepTransforms} time.sleep() calls`);

    // Transform configured custom function calls to await calls
    for (const fnName of ALSO_TRANSFORM) {
        debug(MODULE_NAME, `--- Adding await to ${fnName}() calls ---`);
        let transforms = 0;
        
        for (let i = 0; i < lines.length; i++) {
            // More precise regex that only matches function calls, not strings
            const fnRegex = new RegExp(`(?<!["'\`])\\b${fnName}\\s*\\(`);
            const awaitRegex = new RegExp(`(?<!["'\`])\\bawait\\s+${fnName}\\s*\\(`);
            
            // Only add await if it's not already there
            if (fnRegex.test(lines[i]) && !awaitRegex.test(lines[i])) {
                const oldLine = lines[i];
                lines[i] = lines[i].replace(fnRegex, `await ${fnName}(`);
                debug(MODULE_NAME, `Line ${i + 1}: '${oldLine}' → '${lines[i]}'`);
                transforms++;
            }
        }
        debug(MODULE_NAME, `Applied await to ${transforms} ${fnName}() calls`);
    }
    
    debug(MODULE_NAME, '=== transformPythonCode END ===');
    return lines.join('\n');
}

// Helper function to find functions that contain await calls
function findFunctionsWithAwait(code) {
    debug(MODULE_NAME, '=== findFunctionsWithAwait START ===');
    const lines = code.split(/\r?\n/);
    const functionRegex = /^([ \t]*)def\s+(\w+)\s*\([^)]*\):/;
    const results = [];
    
    for (let i = 0; i < lines.length; i++) {
        const match = lines[i].match(functionRegex);
        if (match) {
            const [_, indent, name] = match;
            debug(MODULE_NAME, `Checking function '${name}' at line ${i + 1} for await calls`);
            
            // Collect the function body (naive: until next non-indented line or EOF)
            let bodyLines = [];
            let j = i + 1;
            while (j < lines.length && (/^\s/.test(lines[j]) || lines[j].trim() === '')) {
                bodyLines.push(lines[j]);
                j++;
            }
            const bodyNoComments = bodyLines.join('\n').replace(/#.*$/gm, '');
            debug(MODULE_NAME, `Function '${name}' body has ${bodyLines.length} lines`);
            
            // Check for await calls
            const hasAwait = /\bawait\s+/.test(bodyNoComments);
            debug(MODULE_NAME, `Function '${name}': hasAwait=${hasAwait}`);
            
            if (hasAwait) {
                debug(MODULE_NAME, `✓ Adding function '${name}' to results (contains await)`);
                results.push({ name, line: i + 1 });
            } else {
                debug(MODULE_NAME, `✗ Skipping function '${name}' (no await calls)`);
            }
        }
    }
    
    debug(MODULE_NAME, `=== findFunctionsWithAwait END: Found ${results.length} functions ===`);
    return results;
}

// Helper function to transform if __name__ == "__main__" block
function transformMainBlock(code) {
    debug(MODULE_NAME, '=== transformMainBlock START ===');
    const lines = code.split(/\r?\n/);
    const transformedLines = [];
    let inMainBlock = false;
    let inElifElseBlock = false;
    let mainBlockIndent = '';
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const mainBlockMatch = line.match(/^(\s*)if\s+__name__\s*==\s*["']__main__["']\s*:/);
        const lineContent = line.trim();
        const currentIndent = line.match(/^(\s*)/)[1];
        
        if (mainBlockMatch) {
            // Found the main block, comment it out and add explanation
            debug(MODULE_NAME, `Found __main__ block at line ${i + 1}`);
            mainBlockIndent = mainBlockMatch[1];
            inMainBlock = true;
            inElifElseBlock = false;
            transformedLines.push(mainBlockIndent + '# The following code was originally in a __main__ block but has been');
            transformedLines.push(mainBlockIndent + '# moved to the global scope for compatibility with Pyodide');
            transformedLines.push(mainBlockIndent + '#' + line.slice(mainBlockIndent.length));
            continue;
        }
        
        if (inMainBlock) {
            if (lineContent === '') {
                // Preserve empty lines as-is
                transformedLines.push('');
                continue;
            }
            
            // Check if we're starting an elif/else block
            if (lineContent.startsWith('elif ') || lineContent.startsWith('else:')) {
                inElifElseBlock = true;
                debug(MODULE_NAME, `Commenting out elif/else at line ${i + 1}`);
                transformedLines.push(mainBlockIndent + '#' + line.slice(mainBlockIndent.length));
                continue;
            }
            
            // Check if we're leaving the main block
            if (currentIndent.length < mainBlockIndent.length) {
                inMainBlock = false;
                inElifElseBlock = false;
                transformedLines.push(line);
                continue;
            }
            
            // Handle content within the main block
            if (inElifElseBlock) {
                // Comment out everything in elif/else blocks
                transformedLines.push(mainBlockIndent + '#' + line.slice(mainBlockIndent.length));
            } else {
                // For content in the main 'if' block:
                // First get the current line's indentation relative to the if __name__ block
                const relativeIndent = currentIndent.slice(mainBlockIndent.length);
                // The content should be at the same level as its if __name__ block, so:
                // 1. Keep the original if __name__ indentation (mainBlockIndent)
                // 2. Remove one level of nesting from the relative indent (the if block's indent)
                const finalIndent = mainBlockIndent + (relativeIndent.length >= 4 ? relativeIndent.slice(4) : '');
                transformedLines.push(finalIndent + lineContent);
                debug(MODULE_NAME, `Un-indenting line ${i + 1} from '${line}' to '${finalIndent + lineContent}'`);
            }
        } else {
            transformedLines.push(line);
        }
    }
    
    debug(MODULE_NAME, '=== transformMainBlock END ===');
    return transformedLines.join('\n');
}

// Main function to transform Python code for Pyodide compatibility with recursive async propagation
function transformPythonForPyodide(code) {
    debug(MODULE_NAME, '🚀 === transformPythonForPyodide START ===');
    debug(MODULE_NAME, 'Input code length:', code.length);
    
    let currentCode = code;
    let previousAsyncFunctions = new Set();
    let maxIterations = 10; // Prevent infinite loops
    let iteration = 0;
    
    // Always run at least one iteration to handle top-level input() and time.sleep() calls
    do {
        iteration++;
        debug(MODULE_NAME, `\n🔄 === Iteration ${iteration} ===`);
        
        // Find functions with input() or time.sleep() (base case)
        const foundFunctions = findFunctionsWithInputOrSleep(currentCode);
        debug(MODULE_NAME, `Found ${foundFunctions.length} functions with input()/time.sleep()`);
        
        // Find functions that contain await calls (cascading case)
        const awaitFunctions = findFunctionsWithAwait(currentCode);
        debug(MODULE_NAME, `Found ${awaitFunctions.length} functions with await calls`);
        
        // Combine both sets of functions that need to be async
        const allAsyncFunctions = [...foundFunctions, ...awaitFunctions];
        debug(MODULE_NAME, `Total potential async functions: ${allAsyncFunctions.length}`);
        
        // Remove duplicates
        const uniqueAsyncFunctions = allAsyncFunctions.filter((fn, index, self) => 
            index === self.findIndex(f => f.name === fn.name)
        );
        debug(MODULE_NAME, `Unique async functions after deduplication: ${uniqueAsyncFunctions.length}`);
        
        const currentAsyncFunctions = new Set(uniqueAsyncFunctions.map(f => f.name));
        
        debug(MODULE_NAME, 'Functions needing async:', Array.from(currentAsyncFunctions));
        debug(MODULE_NAME, 'Previous async functions:', Array.from(previousAsyncFunctions));
        
        // Find all calls to async functions
        const functionNames = uniqueAsyncFunctions.map(f => f.name);
        const calls = findFunctionCalls(currentCode, functionNames);
        
        // Transform the code (this will always run at least once, handling top-level calls)
        debug(MODULE_NAME, '🔧 Starting code transformation...');
        const beforeTransform = currentCode.length;
        currentCode = transformPythonCode(currentCode, uniqueAsyncFunctions, calls);
        const afterTransform = currentCode.length;
        debug(MODULE_NAME, `Code length: ${beforeTransform} → ${afterTransform}`);
        
        // If no new async functions were found, we're done
        const noNewFunctions = currentAsyncFunctions.size === previousAsyncFunctions.size && 
            [...currentAsyncFunctions].every(fn => previousAsyncFunctions.has(fn));
        
        debug(MODULE_NAME, `No new async functions found: ${noNewFunctions}`);
        
        if (noNewFunctions) {
            debug(MODULE_NAME, '✅ No new async functions found. Transformation complete.');
            break;
        }
        
        // Update the set of async functions for next iteration
        previousAsyncFunctions = new Set(currentAsyncFunctions);
        debug(MODULE_NAME, `Updated previous async functions for next iteration: ${Array.from(previousAsyncFunctions)}`);
        
    } while (iteration < maxIterations);
    
    if (iteration >= maxIterations) {
        debug(MODULE_NAME, '⚠️ Warning: Maximum iterations reached. Transformation may be incomplete.');
    }
    
    // After all async transformations are done, handle the main block
    debug(MODULE_NAME, '🔧 Transforming main block...');
    currentCode = transformMainBlock(currentCode);
    
    debug(MODULE_NAME, `🏁 === transformPythonForPyodide END (${iteration} iterations) ===`);
    debug(MODULE_NAME, 'Final code length:', currentCode.length);
    
    return currentCode;
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
                debug(MODULE_NAME, `Loaded Python code from: ${filePath}`);
            } catch (err) {
                debug(MODULE_NAME, `Error reading file '${filename}':`, err.message);
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

        debug(MODULE_NAME, '\n' + '='.repeat(80));
        debug(MODULE_NAME, '=== Original Code ===');
        debug(MODULE_NAME, '='.repeat(80));
        debug(MODULE_NAME, pythonCode);
        
        // Always transform the code regardless of source
        const transformed = transformPythonForPyodide(pythonCode);
        
        debug(MODULE_NAME, '\n' + '='.repeat(80));
        debug(MODULE_NAME, '=== Transformed Code ===');
        debug(MODULE_NAME, '='.repeat(80));
        debug(MODULE_NAME, transformed);
        
        // Show detailed analysis after the transformed code
        debug(MODULE_NAME, '\n' + '='.repeat(80));
        debug(MODULE_NAME, '=== Detailed Analysis ===');
        debug(MODULE_NAME, '='.repeat(80));
        
        const foundFunctions = findFunctionsWithInputOrSleep(pythonCode);
        const functionNamesArray = foundFunctions.map(f => f.name);
        const calls = findFunctionCalls(pythonCode, functionNamesArray);
        
        if (foundFunctions.length > 0) {
            debug(MODULE_NAME, '\nFunctions containing input() or time.sleep():', 
                foundFunctions.map(f => f.name).join(', '));
            
            debug(MODULE_NAME, '\nFunction Call Analysis:');
            for (const fn of foundFunctions) {
                debug(MODULE_NAME, `\nCalls to function '${fn.name}':`);
                if (!calls[fn.name] || calls[fn.name].length === 0) {
                    debug(MODULE_NAME, '  (No calls found)');
                } else {
                    for (const call of calls[fn.name]) {
                        debug(MODULE_NAME, `  Line ${call.line}: ${call.text}`);
                    }
                }
            }
        } else {
            debug(MODULE_NAME, 'No functions with input() or time.sleep() found.');
        }
    }
}