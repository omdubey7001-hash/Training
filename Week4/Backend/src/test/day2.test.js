import mongoose from "mongoose";
import AccountRepository from "../repositories/account.repository.js";
import OrderRepository from "../repositories/order.repository.js";
import config from "../config/index.js";

async function test() {
  await mongoose.connect(config.databaseUrl);


  const account = await AccountRepository.create({
    firstName: "Om",
    lastName: "Dubey",
    email: "om@test.com",
    password: "password123",
    status: "ACTIVE"
  });

  console.log("Account created:", account._id);


  for (let i = 1; i <= 15; i++) {
    await OrderRepository.create({
      accountId: account._id,
      amount: i * 100,
      status: "COMPLETED"
    });
  }

  console.log("Orders created");

  process.exit(0);
}

test();
