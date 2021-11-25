// interact.js

require("dotenv").config();

const API_KEY = process.env.API_KEY;
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;

const contract = require("./blockchain/build/contracts/Election.json");
const { ethers } = require("ethers");

// Provider
const alchemyProvider = new ethers.providers.AlchemyProvider(
  (network = "ropsten"),
  API_KEY
);

// Signer
const signer = new ethers.Wallet(PRIVATE_KEY, alchemyProvider);

// Contract
const electionContract = new ethers.Contract(
  CONTRACT_ADDRESS,
  contract.abi,
  signer
);

async function main() {
  const count = await electionContract.candidatesCount();
  console.log("The candidate count is: " + count);
  const vote1 = await electionContract.candidates(1);
  console.log("The vote status of candidate 1 is: " + vote1);
  console.log("Voter 2 is voting to candidate 1...");
  const tx = await electionContract.vote(1, 5);
  await tx.wait();
  const newVoteCount1 = await electionContract.candidates(1);
  console.log("The vote status of candidate 1 is: " + newVoteCount1);
}
main();
