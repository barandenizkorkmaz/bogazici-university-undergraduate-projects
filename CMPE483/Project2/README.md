# CMPE483: Blockchain Programming - Project 1

## 1. Smart Contracts

### 1.1 Compilation

1. Add `bulot.sol`, `EIP20.sol`, and `hashHelper.sol` files into `Remix Ethereum IDE` that are provided in `Project 1`.
2. Compile contract files.

### 1.2 Deployment

The deployment environment must be selected as `Injected Web3`.

1. Deploy `EIP20.sol` by entering the following parameters:
   1. initialAmount: uint256
   2. tokenName: string
   3. decimalUnits: uint8
   4. tokenSymbol: string
2. Deploy `bulot.sol` by entering the address of previously deployed ERC20 Token Contract.
3. Deploy `hashHelper.sol`.

## 2. Running the Web Interface

1. Install required NodeJS modules.

   ```bash
   npm install
   ```

2. In `app.js`, please enter the absolute path of `index.html` into the following
   line:

   ```javascript
   res.sendFile('path/of/index.html')
   ```

3. In `index.html`, provide the addresses of contracts you have deployed in the variables `hashHelperAddress`, `bulotAddress`, `erc20Address`.

4. Enter the following command in terminal:

   ```bash
   node app.js
   ```

5. In your web browser, you can use the web interface by entering the following address:

   ```
   http://localhost:8081/
   ```

   

NOTES:

3. In the original version of program, each random number submission
   and reveal stages last for one week. However, in order to test the contract, we
   assume that each of these stages last for 1 minutes. To do so, we re-assign the
   `LOTTERY_DURATION` variable in the contract as follows:

```
uint constant LOTTERY_DURATION = 1 minutes;
```
