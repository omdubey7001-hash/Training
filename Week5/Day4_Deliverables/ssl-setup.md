# Day 4 – SSL Setup using mkcert (Step by Step)

This file documents the exact steps followed to enable HTTPS
using self-signed certificates with mkcert and NGINX.

---

## Step 1: Install mkcert

Install mkcert on the local system.

```bash
sudo apt update
sudo apt install mkcert
```

## Step 2: Install Local Certificate Authority

Install a local trusted Certificate Authority.
This step is required only once per machine.
```bash
mkcert -install
```

### Result:

- A local CA is created

- The CA is added to the system trust store

- Browsers can trust local certificates

## Step 3: Create Directory for Certificates

Create a directory to store SSL certificates.
```bash
mkdir -p nginx/certs
```

## Step 4: Generate SSL Certificate for Localhost

Generate a self-signed certificate and private key for localhost.
```bash
mkcert \
  -key-file nginx/certs/localhost-key.pem \
  -cert-file nginx/certs/localhost.pem \
  localhost
```

This generates:

- `localhost.pem` → SSL certificate

- `localhost-key.pem` → Private key

## Step 5: Verify Certificate Files

Confirm that the certificate files exist.
```bash
ls nginx/certs
```

Expected output:
```vbnet
localhost.pem
localhost-key.pem
```

## Step 6: Configure NGINX for HTTPS

Open the NGINX configuration file.
```bash
nano nginx/nginx.conf
```

Configure:

- Port 80 to redirect HTTP → HTTPS

- Port 443 to enable SSL using the generated certificates

(Actual configuration is stored in nginx.conf)

## Step 7: Mount Certificates into NGINX Container

Ensure certificates are mounted into the NGINX container
via Docker volumes.

Configured in `docker-compose.yml`:
```yaml
- ./nginx/certs:/etc/nginx/certs:ro
```

## Step 8: Restart Containers

Stop running containers.
```bash
docker compose down
```

Start containers again so NGINX loads the certificates.
```bash
docker compose up -d
```

(or with profile)
```bash
docker compose --profile dev up -d
```
## Step 9: Verify HTTP to HTTPS Redirect

Test that HTTP requests are redirected to HTTPS.
```bash
curl -I http://localhost
```

Expected response:
```arduino
HTTP/1.1 301 Moved Permanently
Location: https://localhost
```

## Step 10: Verify HTTPS Endpoint

Test HTTPS endpoint.
```bash
curl -k https://localhost/api
```

Expected result:

- Successful response from NGINX

- No connection failure

## Step 11: Verify in Browser

Open a browser and visit:
```arduino
https://localhost/api
```

Expected result:

- 🔒 Lock icon visible

- Certificate trusted

- HTTPS working correctly

## Step 12: Completion

HTTPS setup using mkcert is complete.

- Local CA installed

- SSL certificates generated

- HTTPS enabled in NGINX

- HTTP redirected to HTTPS

## Output response

![Lock Output](images/Screenshot%20from%202026-01-13%2013-28-55.png)