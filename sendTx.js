// A demo transaction and signing

async function main() {
  require("dotenv").config();
  const { API_URL, PRIVATE_KEY } = process.env;
  const { createAlchemyWeb3 } = require("@alch/alchemy-web3");
  const web3 = createAlchemyWeb3(API_URL);
  const myAddress = "0xa9366D1615b839E36e6034226136E1D088c8CFe3"; //TODO: replace this address with your own public address

  const nonce = await web3.eth.getTransactionCount(myAddress, "latest"); // nonce starts counting from 0

  const transaction = {
    to: "0xD3c22d0243C551d24D31bED9865E3d4899E1CB8b", // faucet address to return eth
    value: 100,
    gas: 30000,
    maxFeePerGas: 10000001080,
    nonce: nonce,
    // optional data field to send message or execute smart contract
  };

  const signedTx = await web3.eth.accounts.signTransaction(
    transaction,
    PRIVATE_KEY
  );

  web3.eth.sendSignedTransaction(
    signedTx.rawTransaction,
    function (error, hash) {
      if (!error) {
        console.log(
          "🎉 The hash of your transaction is: ",
          hash,
          "\n Check Alchemy's Mempool to view the status of your transaction!"
        );
      } else {
        console.log(
          "❗Something went wrong while submitting your transaction:",
          error
        );
      }
    }
  );
}

main();
