// A demo call to the Ropsten network

async function main() {
  const { createAlchemyWeb3 } = require("@alch/alchemy-web3");
  const web3 = createAlchemyWeb3("https://eth-ropsten.alchemyapi.io/v2/Ny_9tXio-d0yeKZE3qMm28TXEhcSqgXk");
  const blockNumber = await web3.eth.getBlockNumber();
  console.log("The latest block number is " + blockNumber);
}
main();
