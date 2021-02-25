loadScript('ERC20.js');
console.log("ERC20 LOADED")
loadScript('BULOT.js');
console.log("BULOT LOADED")
loadScript('hashHelper.js');
console.log("HashHelper LOADED")

// reference: https://github.com/srknzl/BULOT-Smart-Contract/blob/master/test1.js for lines 22-28 and 42-66

var erc20address = "0x9bC7097Df2127f52AAb38DbAf6805eAE761FAb33";
var erc20network = web3.eth.contract(erc20).at(erc20address);
console.log('erc20network   '+erc20network)
var bulotAddress = "0x734B0153029F57FE8e1360dC2Bcf352eF7DD106c";
var bulotNetwork = web3.eth.contract(bulotC).at(bulotAddress);

var hashHelperAddress = "0x05dA05017F65Df613d56493A8f51Cf15f933FF97";
var hashNetwork = web3.eth.contract(hasher).at(hashHelperAddress);

console.log('bulotNetwork    '+bulotNetwork)
var totalPrize = 0;
var totalMoneySpent = 0;
var MAXACCCOUNT = 10;                                                       // We would like to simulate our lottery with 10 users
console.log("Lenth of array for accounts:", eth.accounts.length);

var ticketList = {};                                                        // Mapping of which user bought which ticket, technically more than 1 ticket per user is possible
                                                                            // However we did not simulated with only 1 ticket for our testing purposes
var size = eth.accounts.length;
if (size < MAXACCCOUNT) {                                                   // If there are less than 10 accounts in the network, add new accounts until there are 10
    console.log("WE NEED TO CREATE NEW ACCOUNTS");
    for (var i = 0; i < MAXACCCOUNT - size; i++) {
        personal.newAccount("");
    }
}


eth.defaultAccount=eth.accounts[0] ;

for (var i = 0; i<eth.accounts.length; i++) {                                // Unlock the accounts and approve our 0'th account to send 100 tokens to all other accounts
    personal.unlockAccount(eth.accounts[i], '');
    console.log('Account:' +eth.accounts[i] + 'is unlocked');
    var bool = erc20network.approve(eth.accounts[i], 100, {
        from: eth.accounts[0],
    });
    console.log('100 tokens approved for ' + eth.accounts[i] );
}

eth.accounts.forEach(function (account,index) {                             // Sometimes the index of the coinbase account changes, find it
    if(eth.getBalance(account) > 1e30 ){
        coinBaseIndex = index;
    }
});
console.log("Coinbase account: ", coinBaseIndex);
eth.accounts.forEach(function (account, index) {                            // Send 10 ethers from account 0 to other accounts, we need this for the gas costs
    var balance = eth.getBalance(account);
    if (balance < 1e9 && index != coinBaseIndex) {
        var tx = { from: eth.accounts[coinBaseIndex], to: account, value: 1e19 };
        personal.sendTransaction(tx, "");
    }
});

var blockCreationInterval = setInterval(function () {               // Interval created to pass ether back and forth between accounts 0 and 1
                                                                            // We need this so that new blocks are mined and block.timestamp doesnt get stuck
    personal.unlockAccount(eth.accounts[0], '');
    var tx = { from: eth.accounts[0], to: eth.accounts[1], value: new BigNumber(1e18) };
    personal.sendTransaction(tx, "");

    personal.unlockAccount(eth.accounts[1], '');
    var tx = { from: eth.accounts[1], to: eth.accounts[0], value: new BigNumber(1e18) };
    personal.sendTransaction(tx, "");

}, 500);


for (var i = 0; i<eth.accounts.length; i++) {                               // Send 100 tokens to each account from our 0'th account, it has all the originally created tokens
    erc20network.transfer(eth.accounts[i], 100, {
        from: eth.accounts[0],
    });
    console.log('100 tokens transferred to ' + eth.accounts[i] );
}

for (var i = 0; i<eth.accounts.length; i++) {                               // Check token balances of all the accounts to confirm
    var balance = erc20network.balanceOf.call(eth.accounts[i], {
        from: eth.defaultAccount
    });
    console.log(eth.accounts[i] + ' has the balance of ' + balance);

}

for (var i = 0; i<eth.accounts.length; i++) {                               // Approve all accounts to send 100 tokens to the BULOT contract
                                                                            // We need this to let all users buy tickets with tokens
    var bool = erc20network.approve(bulotAddress, 100, {
        from: eth.accounts[i],
    });
    console.log(eth.accounts[i] + ' approved for transfer to BULOT' );
}


for (var i = 0; i<eth.accounts.length; i++) {                               // For each account, get a random number, hash it, get it's ticket no
                                                                            // and save it to our dictionary to check later
    var randomNum = Math.floor(Math.random() * 1000000);
    var hash = hashNetwork.getHash.call(randomNum, { from: eth.accounts[i]});
    personal.unlockAccount(eth.accounts[i], '');
    bulotNetwork.buyTicket(hash, {from: eth.accounts[i]});
    var lotteryNum = bulotNetwork.getCurrentLotteryNo.call();

    var ticketNo = bulotNetwork.getLastBoughtTicketNo.call(lotteryNum , { from: eth.accounts[i]});
    console.log(eth.accounts[i] + ' buys the ticket with random number ' + randomNum + ' and hash ' + hash + ' and ticket no ' + ticketNo + ' on lottery ' + lotteryNum );
    ticketList[eth.accounts[i]] = {
        'ticketNo': ticketNo,
        'randomNum': randomNum,
        'hash' : hash
    }
    totalMoneySpent += 10;
}

var revealed = false;
var withdrawn = false;

var revealInterval = setInterval(function () {                      // try revealing the tickets every 60 seconds, if reveal is successful, stop the interval
    reveal();
    if (revealed) {
        clearInterval(revealInterval);
    }

},  60*1000);

var prizeInterval = setInterval(function () {                       // try claiming the prizes every 60 seconds, if claiming is successful, stop the interval
    prizeClaim();
    if (withdrawn) {
        clearInterval(prizeInterval);
    }
},  120*1000);

function reveal() {
    for (var i = 0; i < eth.accounts.length; i++) {                         // for each account, try revealing their bought ticket with the random number and ticket no
        var ticket = ticketList[eth.accounts[i]];
        lotteryNum = bulotNetwork.getCurrentLotteryNo.call();
        bulotNetwork.revealRndNumber(                                       // since contract is going fail assertion if lottery no is not appopriate the code block will stop here
            ticket.ticketNo,
            ticket.randomNum,
            {
                from: eth.accounts[i]
            }
        )
        revealed = true;                                                    // if reveal is successful make revealed true to stop the interval
        console.log(eth.accounts[i] + ' revealing ticketNo: ' + ticket.ticketNo + ' random number ' + ticket.randomNum);
    }
}

function prizeClaim() {
    for (var i = 0; i < eth.accounts.length; i++) {                         // for each account, claiming the ticket prizes
        var lotteryNum = bulotNetwork.getCurrentLotteryNo.call();
        var ticketNo = ticketList[eth.accounts[i]].ticketNo;
        var prize = bulotNetwork.checkIfTicketWon.call(lotteryNum-2, ticketNo, { from: eth.accounts[i]} );      // first we check the prize
        var balance = erc20network.balanceOf.call(eth.accounts[i], {
            from: eth.defaultAccount
        });
        console.log( eth.accounts[i] + ' has balance of ' + balance);                                           // we log the balance before claim
        console.log( eth.accounts[i] + ' won a prize of ' + prize + ' with ticket no ' + ticketNo);             // we log the amount ticket won
        if ( prize > 0) {
            bulotNetwork.withdrawTicketPrize(lotteryNum -2, ticketNo, { from: eth.accounts[i]});                // we try to claim the prize won if its greater than 0
            withdrawn = true;                                                                                   // if prize claim is successful, then its claim stage and we can stop the interval check
        }
        totalPrize += prize;
        balance = erc20network.balanceOf.call(eth.accounts[i], {
            from: eth.defaultAccount
        });
        console.log( eth.accounts[i] + ' has balance of ' + balance);                                           // we log the balance after claim
    }
}
