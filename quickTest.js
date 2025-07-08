// quickTest.js - Simple test for transformation
import { transformPythonForPyodide } from './transformInputToAsync.js';

const testCode = `print("Hello")
name = input("What's your name? ")
print(f"Hello, {name}!")
import time
time.sleep(2)
print("Done!")`;

console.log('=== Original ===');
console.log(testCode);
console.log('\n=== Transformed ===');
console.log(transformPythonForPyodide(testCode));
