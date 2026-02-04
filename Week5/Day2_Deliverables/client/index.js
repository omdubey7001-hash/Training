console.log("Client started");

const SERVER_URL = "http://server:5000/";

async function callServer(retries = 5) {
  try {
    const res = await fetch(SERVER_URL);
    const data = await res.json();
    console.log("Response from server:", data);
  } catch (err) {
    if (retries > 0) {
      console.log("Server not ready, retrying...");
      await new Promise(r => setTimeout(r, 3000));
      return callServer(retries - 1);
    } else {
      console.error("Server not reachable after retries");
    }
  }
}

callServer();
