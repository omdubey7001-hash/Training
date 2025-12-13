const fs = require('fs');  // To work with files
const path = require('path');  // To handle file paths

// Function to get the current time in a readable format
function getCurrentTime() {
  return new Date().toISOString(); // For example: 2025-12-02T14:45:12.000Z
}

// Function to log system usage data
function logSystemMetrics() {
  const cpuUsage = process.cpuUsage();  // Get how much CPU the program is using
  const resourceUsage = process.resourceUsage();  // Get how much memory the program is using
  
  const logData = {
    timestamp: getCurrentTime(),  // Current time of this log
    cpuUsage: {
      user: cpuUsage.user,  // Time in microseconds spent doing user tasks
      system: cpuUsage.system,  // Time in microseconds spent doing system tasks
    },
    resourceUsage: {
      heapTotal: resourceUsage.heapTotal,  // Total memory allocated for your program's use
      heapUsed: resourceUsage.heapUsed,  // Memory your program is actually using
      external: resourceUsage.external,  // Memory used by things outside of JavaScript objects
      rss: resourceUsage.rss,  // Total memory used by the program (includes all resources)
    },
  };

  // Path to where the logs are saved (in logs/day1/sysmetrics.json)
  const logFilePath = path.join(__dirname, '/logs/day1/sysmetrics.json');
  
  // Check if the logs folder exists, create it if it doesn't
  if (!fs.existsSync(path.dirname(logFilePath))) {
    fs.mkdirSync(path.dirname(logFilePath), { recursive: true });
  }

  // Read existing logs and add new data to it
  let existingLogs = [];
  if (fs.existsSync(logFilePath)) {
    existingLogs = JSON.parse(fs.readFileSync(logFilePath, 'utf-8'));  // Read previous logs
  }

  existingLogs.push(logData);  // Add the new log data

  // Write the new data back to the file
  fs.writeFileSync(logFilePath, JSON.stringify(existingLogs, null, 2));  // Save logs in pretty JSON format
  console.log(`Logged system metrics at ${logData.timestamp}`);
}

// Set an interval to log data every 10 seconds (10000 milliseconds)
setInterval(logSystemMetrics, 10000);
