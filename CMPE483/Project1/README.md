# CMPE483: Blockchain Programming - Project 1

## 1. Smart Contracts

### 1.1 Compilation

1. Add `bulot.sol`, `EIP20.sol`, and `hashHelper.sol` files into `Remix Ethereum IDE`.
2. Compile contract files.

### 1.2 Deployment

1. Deploy `EIP20.sol` by entering the following parameters:
   1. initialAmount: uint256
   2. tokenName: string
   3. decimalUnits: uint8
   4. tokenSymbol: string
2. Deploy `bulot.sol` by entering the address of previously deployed ERC20 Token Contract.
3. Deploy `hashHelper.sol`.

## 2. Testing

1. For testing purposes, you can run our contract by connecting to our local
   ethereum node through `Web3 provider`. After attaching a Geth client to
   your ethereum node, you can run our test script in Geth console.
2. Enter the following command in Geth console:

```javascript
loadScript("\test.js")
```

NOTES:

1. For testing, please make sure that you updated the addresses of all contracts, namely `bulot.sol`, `EIP20.sol`, `hashHelper.sol` in `test.js` script.
2. The testing lasts for at least 2 minutes, since it simulates random number submission and reveal stages.
3. In the original version of program, each random number submission
   and reveal stages last for one week. However, in order to test the contract, we
   assume that each of these stages last for 1 minutes. To do so, we re-assign the
   `LOTTERY_DURATION` variable in the contract as follows:

```
uint constant LOTTERY_DURATION = 1 minutes;
```

4. The script `test.js` uses `hashHelper` contract for computing the hash values to be sent during random number submission.
5. In Remix Ethereum IDE, you can use hashHelper contract provided
   by `hashHelper.sol` to obtain the hash values for buying tickets in BULOT.