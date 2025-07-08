// testConcatenatePrints.js
// Test script for the concatenateConsecutivePrints function

import { concatenateConsecutivePrints } from './concatenatePrints.js';
import fs from 'fs';
import path from 'path';

// Test with a Python file (either specified as argument or default to main.py)
async function testWithPythonFile(filename = 'main.py') {
    try {
        const filePath = path.resolve(process.cwd(), filename);
        const pythonCode = fs.readFileSync(filePath, 'utf8');
        
        console.log(`=== Original ${filename} ===`);
        console.log(pythonCode);
        
        console.log(`\n=== After concatenateConsecutivePrints ===`);
        const result = concatenateConsecutivePrints(pythonCode);
        console.log(result);
        
        console.log('\n=== Changes Made ===');
        const originalLines = pythonCode.split('\n');
        const resultLines = result.split('\n');
        
        if (originalLines.length !== resultLines.length) {
            console.log(`Line count changed: ${originalLines.length} → ${resultLines.length}`);
        } else {
            console.log('No line count changes (no consecutive prints found)');
        }
        
    } catch (error) {
        console.error(`Error reading ${filename}:`, error.message);
    }
}

// Test with a custom example that has consecutive prints
function testWithCustomExample() {
    const testCode = `print("Hello")
print("world")
print("How are you?")

def test():
    print("Line 1")
    print("Line 2")
    print("Line 3")
    
    if True:
        print("Indented 1")
        print("Indented 2")
        
print("Final line")`;

    console.log('\n=== Custom Test Example ===');
    console.log('Original:');
    console.log(testCode);
    
    console.log('\nAfter concatenation:');
    const result = concatenateConsecutivePrints(testCode);
    console.log(result);
}

// Run tests
console.log('Testing concatenateConsecutivePrints function...\n');

// Get filename from command line argument or default to main.py
const filename = process.argv[2] || 'main.py';
console.log(`Using file: ${filename}\n`);

await testWithPythonFile(filename);

// Only run custom example if no specific file was provided
if (!process.argv[2]) {
    testWithCustomExample();
}
