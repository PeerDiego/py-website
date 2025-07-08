// concatenatePrints.js
// Module for concatenating consecutive print() statements into single print() calls

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
 * print("Hello\nworld")
 */
function concatenateConsecutivePrints(code) {
    console.log('🔗 === concatenateConsecutivePrints START ===');
    console.log('Input code length:', code.length);
    
    const lines = code.split(/\r?\n/);
    console.log(`Processing ${lines.length} lines of code`);
    
    const result = [];
    let i = 0;
    let totalCombinations = 0;
    let totalLinesReduced = 0;
    
    while (i < lines.length) {
        const line = lines[i];
        const trimmedLine = line.trim();
        console.log(`Line ${i + 1}: "${trimmedLine}"`);
        
        // Check if this line is a print statement
        const printMatch = line.match(/^(\s*)print\((.+)\)$/);
        
        if (printMatch) {
            const indent = printMatch[1];
            const firstPrintContent = printMatch[2];
            console.log(`  ✓ Found print statement with indent "${indent}" and content: ${firstPrintContent}`);
            
            let printContents = [firstPrintContent];
            let j = i + 1;
            
            // Look for consecutive print statements with the same indentation
            console.log(`  🔍 Looking for consecutive prints starting from line ${j + 1}...`);
            while (j < lines.length) {
                const nextLine = lines[j];
                const nextPrintMatch = nextLine.match(/^(\s*)print\((.+)\)$/);
                
                // If next line is also a print with same indentation, collect it
                if (nextPrintMatch && nextPrintMatch[1] === indent) {
                    console.log(`  ✓ Found consecutive print at line ${j + 1}: ${nextPrintMatch[2]}`);
                    printContents.push(nextPrintMatch[2]);
                    j++;
                } else {
                    // Stop if we hit a non-print line or different indentation
                    if (nextPrintMatch) {
                        console.log(`  ✗ Print at line ${j + 1} has different indentation: "${nextPrintMatch[1]}" vs "${indent}"`);
                    } else {
                        console.log(`  ✗ Line ${j + 1} is not a print statement: "${nextLine.trim()}"`);
                    }
                    break;
                }
            }
            
            // If we found multiple consecutive prints, combine them
            if (printContents.length > 1) {
                console.log(`  🔧 Combining ${printContents.length} consecutive prints`);
                totalCombinations++;
                totalLinesReduced += printContents.length - 1;
                
                // Extract the content from each print, handling quotes properly
                const extractedContents = printContents.map((content, index) => {
                    console.log(`    Processing print content ${index + 1}: ${content}`);
                    
                    // Remove outer quotes if they exist and extract the content
                    const match = content.match(/^["'](.*)["']$/) || content.match(/^f["'](.*)["']$/);
                    if (match) {
                        const extracted = match[1];
                        console.log(`    → Extracted quoted content: "${extracted}"`);
                        return extracted;
                    }
                    // If it's not a simple quoted string, keep as is (for f-strings, variables, etc.)
                    const wrapped = `{${content}}`;
                    console.log(`    → Wrapped non-quoted content: "${wrapped}"`);
                    return wrapped;
                });
                
                // Create a multi-line string
                const combinedContent = extractedContents.join('\\n');
                const finalLine = `${indent}print("${combinedContent}")`;
                console.log(`  ✅ Combined line: ${finalLine}`);
                result.push(finalLine);
            } else {
                // Single print statement, keep as is
                console.log(`  → Single print statement, keeping as-is`);
                result.push(line);
            }
            
            i = j; // Skip the lines we've processed
            console.log(`  📍 Advanced to line ${i + 1}`);
        } else {
            // Not a print statement, keep as is
            console.log(`  → Not a print statement, keeping as-is`);
            result.push(line);
            i++;
        }
    }
    
    const finalCode = result.join('\n');
    console.log('🔗 === concatenateConsecutivePrints SUMMARY ===');
    console.log(`Input lines: ${lines.length}`);
    console.log(`Output lines: ${result.length}`);
    console.log(`Lines reduced: ${totalLinesReduced}`);
    console.log(`Total combinations made: ${totalCombinations}`);
    console.log(`Final code length: ${finalCode.length}`);
    console.log('🔗 === concatenateConsecutivePrints END ===');
    
    return finalCode;
}

// Export the function using ES6 syntax
export { concatenateConsecutivePrints };
