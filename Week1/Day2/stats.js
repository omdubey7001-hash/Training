#!/usr/bin/env node
const fs = require('fs');
const readline = require('readline');
const path = require('path');

// Promisified function to process a single file and return metrics/counts
function processFile(type,filePath, removeDuplicates = false) {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();
        const startMem = process.memoryUsage().heapUsed;

        //if file not existing or mismatched file path it terminates here.
        if (!fs.existsSync(filePath)) {
            return reject(new Error(`File not found: ${filePath}`));
        }

        const rl = readline.createInterface({// rl containinf the data in the files
            input: fs.createReadStream(filePath),//read the file here
            crlfDelay: Infinity
        });

        let linesCount = 0;
        let wordsCount = 0;
        let charsCount = 0;
        const uniqueLines = new Set();// using a set to counter uniqueness 
        const lines = [];// to store the unique lines

        rl.on('line', (line) => {
            linesCount++;
            charsCount += line.length + 1; // +1 for the newline character
            wordsCount += line.trim().split(/\s+/).filter(word => word.length > 0).length;

            if (removeDuplicates) {
                if (!uniqueLines.has(line)) {
                    uniqueLines.add(line);
                    lines.push(line);
                }
            }
        });

        rl.on('close', async () => {
            const endTime = Date.now();
            const endMem = process.memoryUsage().heapUsed;
            const executionTimeMs = endTime - startTime;
            const memoryMB = (endMem - startMem) / 1024 / 1024;

            const results = {
                file: path.basename(filePath),
                executionTimeMs,
                memoryMB,
                counts: {}
            };

            if (type === "lines") {
                results.counts.lines = linesCount;
            } else if (type === "words") {
                results.counts.words = wordsCount;
            } else if (type === "chars") {
                results.counts.chars = charsCount;
            }


            // Bonus: Handle unique lines output
            if (removeDuplicates) {
                const outputDir = path.join(process.cwd(), 'output');
                if (!fs.existsSync(outputDir)) {
                    fs.mkdirSync(outputDir, { recursive: true });
                }
                const outputFileName = `unique-${path.basename(filePath)}`;
                const outputPath = path.join(outputDir, outputFileName);
                await fs.promises.writeFile(outputPath, lines.join('\n') + '\n');
                console.log(`\nBonus: Unique lines written to: ${outputPath}`);
            }

            resolve(results);
        });

        rl.on('error', reject);
    });
}



// Main CLI logic to handle arguments and parallel processing
async function main() {
    // Parse command line arguments: --lines <file> --chars <file> ...
    const args = process.argv.slice(2);
    const filesToProcess= [];// type:lines,chars, words -> file:filename
    let removeDuplicatesFlag = false;
    //./stats.js --lines data1.txt --chars data2.txt --words data1.txt --unique

    function validateFile(file) {
    return file && !file.startsWith('--');
    }

    for (let i = 0; i < args.length; i++) {
        if (['--lines', '--chars', '--words'].includes(args[i])) {
            const next = args[i + 1];
            if (validateFile(next)) {
                filesToProcess.push({
                    type: args[i].substring(2),
                    file: next
                });
                i++;
            } else {
                console.error(`Missing or invalid filename after ${args[i]}`);
            }
        } else if (args[i] === '--unique') {
            removeDuplicatesFlag = true;
        }
    }


    if (filesToProcess.length === 0) {
        console.log("Usage: node stats.js --lines <file1> [--words <file2> ...] [--unique]");
        process.exit(1);
    }

    console.log(`\nProcessing ${filesToProcess.length} file(s) in parallel...`);

    // Process files in parallel using Promise.all
    const processingPromises = filesToProcess.map(item => 
        processFile(item.type,item.file, removeDuplicatesFlag)
    );

    try {
        const results = await Promise.all(processingPromises);
        
        console.log("\n--- Performance Report & Stats ---");
        
        // Ensure logs directory exists for performance reports
        const logsDir = path.join(process.cwd(), 'logs');
        if (!fs.existsSync(logsDir)) {
            fs.mkdirSync(logsDir, { recursive: true });
        }

        // Output results and save individual JSON reports
        results.forEach(result => {
            console.log(JSON.stringify(result, null, 2));

            // Save performance report to logs/performance-*.json
            const t = Date.now();
            const logFileName = `performance-${t}${result.file }.json`;
            const logPath = path.join(logsDir, logFileName);
            fs.writeFileSync(logPath, JSON.stringify(result, null, 2));
            console.log(`(Report saved to ${logPath})\n`);
        });

    } catch (error) {
        console.error(`\nAn error occurred during processing: ${error.message}`);
        process.exit(1);
    }
}

main();
