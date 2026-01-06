import fs from "fs";
import path from "path";
import dotenv from "dotenv";

const ENV = process.env.NODE_ENV || "local";


const envFileMap = {
  local: ".env.local",
  dev: ".env.dev",
  prod: ".env.prod",
};

const envFile = envFileMap[ENV];

if (!envFile) {
  throw new Error(`Invalid NODE_ENV: ${ENV}`);
}

const envPath = path.resolve(process.cwd(), envFile);


if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath });
} else {
  console.warn(`[config] ${envFile} not found, using process.env`);
}


dotenv.config({ path: envPath });


const config = {
  env: ENV,
  port: Number(process.env.PORT),
  databaseUrl: process.env.DATABASE_URL,
  logLevel: process.env.LOG_LEVEL || "info",
};


const required = ["port", "databaseUrl"];

required.forEach((key) => {
  if (!config[key]) {
    throw new Error(`Missing required config: ${key}`);
  }
});

Object.freeze(config);

export default config;
