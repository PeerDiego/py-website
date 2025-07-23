// concatenatePrints.js
// Module for concatenating consecutive print() statements into single print() calls

import { debug } from './debugUtils.js';

const MODULE_NAME = 'concatenatePrints.js';

/**
 * Concatenate consecutive print() statements into single print() calls
 * @param {string} code - Python code as a string
 * @returns {string} - Modified Python code with consecutive prints combined
 * 
 * Example:
 * print("Hello")
 * print("world")
 * 
 * becomes:
 * print("Hello", "\\n", "world")
 */
function concatenateConsecutivePrints(code) {
    debug(MODULE_NAME, '🔗 === concatenateConsecutivePrints START ===');
    debug(MODULE_NAME, 'Input code length:', code.length);
    
    const lines = code.split(/\r?\n/);
    debug(MODULE_NAME, `Processing ${lines.length} lines of code`);
    
    const result = [];
    let i = 0;
    let totalCombinations = 0;
    let totalLinesReduced = 0;
    
    while (i < lines.length) {
        const line = lines[i];
        const trimmedLine = line.trim();
        debug(MODULE_NAME, `Line ${i + 1}: "${trimmedLine}"`);
        
        // Check if this line is a print statement
        const printMatch = line.match(/^(\s*)print\((.+)\)$/);
        
        if (printMatch) {
            const indent = printMatch[1];
            const firstPrintContent = printMatch[2];
            debug(MODULE_NAME, `  ✓ Found print statement with indent "${indent}" and content: ${firstPrintContent}`);
            
            let printContents = [firstPrintContent];
            let j = i + 1;
            
            // Look for consecutive print statements with same indentation
            debug(MODULE_NAME, `  🔍 Looking for consecutive prints starting from line ${j + 1}...`);
            while (j < lines.length) {
                const nextLine = lines[j];
                const nextPrintMatch = nextLine.match(/^(\s*)print\((.+)\)$/);
                
                // If next line is also a print with same indentation, collect it
                if (nextPrintMatch && nextPrintMatch[1] === indent) {
                    debug(MODULE_NAME, `  ✓ Found consecutive print at line ${j + 1}: ${nextPrintMatch[2]}`);
                    printContents.push(nextPrintMatch[2]);
                    j++;
                } else {
                    // Stop if we hit a non-print line or different indentation
                    if (nextPrintMatch) {
                        debug(MODULE_NAME, `  ✗ Print at line ${j + 1} has different indentation: "${nextPrintMatch[1]}" vs "${indent}"`);
                    } else {
                        debug(MODULE_NAME, `  ✗ Line ${j + 1} is not a print statement: "${nextLine.trim()}"`);
                    }
                    break;
                }
            }
            
            // If we found multiple consecutive prints, combine them
            if (printContents.length > 1) {
                debug(MODULE_NAME, `  🔧 Combining ${printContents.length} consecutive prints`);
                totalCombinations++;
                totalLinesReduced += printContents.length - 1;
                
                // Create the combined print statement with commas
                const combinedContent = printContents.join(', "\\n", ');
                
                const finalLine = `${indent}print(${combinedContent})`;
                debug(MODULE_NAME, `  ✅ Combined line: ${finalLine}`);
                result.push(finalLine);
            } else {
                // Single print statement, keep as is
                debug(MODULE_NAME, `  → Single print statement, keeping as-is`);
                result.push(line);
            }
            
            i = j; // Skip the lines we've processed
            debug(MODULE_NAME, `  📍 Advanced to line ${i + 1}`);
        } else {
            debug(MODULE_NAME, `  → Not a print statement, keeping as-is`);
            result.push(line);
            i++;
        }
    }
    
    const finalCode = result.join('\n');
    // Always show summary regardless of debug setting
    debug(MODULE_NAME, '=== concatenateConsecutivePrints SUMMARY ===');
    debug(MODULE_NAME, `Lines reduced: ${totalLinesReduced}`);
    debug(MODULE_NAME, `Total combinations made: ${totalCombinations}`);
    
    debug(MODULE_NAME, '🔗 === concatenateConsecutivePrints END ===');
    return finalCode;
}

// Export the main function only - debug control is now handled by debugUtils.js
export { concatenateConsecutivePrints };
