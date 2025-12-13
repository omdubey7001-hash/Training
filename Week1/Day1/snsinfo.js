
// // --- 5. Logged-in User Count ---
// function getUserCount() {
//   const cmd =
//     process.platform === "win32"
//       ? "query user"
//       : "who";

//   exec(cmd, (err, stdout) => {
//     if (err) return console.log("\nUser Count Error:", err);

//     const lines = stdout.trim().split("\n").filter(Boolean);
//     console.log("\nLogged-in User Count:", lines.length);
//     console.log("User Sessions:\n" + stdout);
//   });
// }
// getUserCount();


const os = require("os");

// Print Hostname

console.log("Hostname:", os.hostname());

const { execSync } = require("child_process");


// Print available disk space

try {
  const output = execSync("df -k /").toString().split(/\s+/);
  const availableKB = parseInt(output[10], 10);
  console.log("Available space:", (availableKB / (1024 * 1024)).toFixed(2), "GB");
} catch(err){
  console.error("Error:", err);
}

//Print 
const net = require("net");

const portNames = {
  20: "FTP Data",
  21: "FTP Control",
  22: "SSH",
  23: "Telnet",
  25: "SMTP",
  53: "DNS",
  67: "DHCP",
  68: "DHCP",
  69: "TFTP",
  80: "HTTP",
  110: "POP3",
  123: "NTP",
  143: "IMAP",
  161: "SNMP",
  389: "LDAP",
  443: "HTTPS",
  587: "SMTP (TLS)",
  631: "IPP",
  993: "IMAP (SSL)",
  995: "POP3 (SSL)",
  1433: "MSSQL",
  1521: "Oracle DB",
  1723: "PPTP",
  1883: "MQTT",
  3306: "MySQL",
  3389: "RDP",
  5432: "PostgreSQL",
  5900: "VNC",
  6379: "Redis",
  8080: "HTTP-Alternate",
  27017: "MongoDB",
};

async function scanPorts(){
  const openports =[];

  for(let port =1; port <= 65535; port++){
    if(openports.length >= 5) break;
    const isOpen = await checkPort(port);
    if(isOpen){
      console.log(`Open: ${port} (${portNames[port] || "Unknown"})`);
      openports.push(port);
    }
  }

  console.log("\nOpen ports:");
  console.log(openports);
}

function checkPort(port){
  return new Promise((resolve) => {
    const socket = new net.Socket();

    socket.setTimeout(200);

    socket.connect(port, "127.0.0.1", () => {
      socket.destroy();
      resolve(true);
    });

    socket.on("error", () => resolve(false));
    socket.on("timeout", () => {
      socket.destroy();
      resolve(false);
    });
  });
}

scanPorts();


//Default Gateway

const { exec } = require("child_process");

function getDefaultGateway() {
  const cmd =
    process.platform === "win32"
      ? "ipconfig"
      : "ip route | grep default";

  exec(cmd, (err, stdout) => {
    if (err) return console.log("\nDefault Gateway Error:", err);
    console.log("\nDefault Gateway Info:\n" + stdout);
  });
}
getDefaultGateway();

function getUserCount(){
  let cmd;

  if(process.platform === "win32"){
    cmd = "query user";
  }else{
    cmd = "who";
  }

  exec(cmd, (err, stdout) => {
    if(err){ 
      return console.error("Error",err);
    }
    const users = stdout.split("\n").filter((line) => line.trim() != " ");

    console.log("Number of logged-in users:", users.length);
  });
}
getUserCount();