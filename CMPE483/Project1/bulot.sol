pragma solidity ^0.8.0;

// SPDX-License-Identifier: AGPL-3.0-only

import "./EIP20.sol";

contract BULOT{
    // Structure for each lottery round.
    struct Lottery {
          uint moneyInPool;
          mapping (address => uint[]) ticketsBoughtByUserList;
          mapping (address => mapping(uint => bool)) ticketsBoughtByUserDict;
          mapping (uint => bytes32) ticketNuToRndNumber ;
          mapping (uint => bool) isTicketRevealed;
          mapping (uint => bool) isPrizeWithdrawn;
          uint[] winningTickets;
          uint[] prizes ;
          uint[] ticketsInLottery;
          uint currentXORResult;
          bool isPrizesDetermined;
          bool isLotteryStructInitialized;
      }
    
    // Sets the duration of each random number submission and reveal stage.
    uint constant LOTTERY_DURATION = 1 minutes;

    // State variables.
    mapping (uint => Lottery) lotteries;
    uint ticketsCount;
    uint initialTimeStamp;
    address public contractaddr;

    // Constuctor that takes the address of ERC20 Token Contract as argument.
    // It also initializes the state variables for the first lottery round.
    constructor(address conaddr) {
        contractaddr = conaddr;
        initialTimeStamp = block.timestamp;
        ticketsCount = 0;
        Lottery storage l = lotteries[1];
        lotteries[1].moneyInPool = 0;
        lotteries[1].currentXORResult = 0;
        lotteries[1].isPrizesDetermined = false;
        lotteries[1].isLotteryStructInitialized = true;
     }
     
    //  Fallback function prevents vulnerability to malicious attacks.
    fallback () external {
        revert();
    }

    // Allows buying ticket for current lottery round by providing the hash value of the address of user and submitted random number.
    function buyTicket(bytes32 hash_rnd_number) public {
        ERC20Token contractobj = ERC20Token(contractaddr) ;
        require(contractobj.transferFrom(msg.sender,address(this),10),"Please allow for money transfer in ERC20Token contract.") ;
        uint currentLotteryNo = getCurrentLotteryNo();
        if(!lotteries[currentLotteryNo].isLotteryStructInitialized){
          Lottery storage l = lotteries[currentLotteryNo];
          lotteries[currentLotteryNo].isLotteryStructInitialized = true;
          lotteries[currentLotteryNo].moneyInPool = 0;
          lotteries[currentLotteryNo].currentXORResult = 0;
          lotteries[currentLotteryNo].isPrizesDetermined = false;
        }
        lotteries[currentLotteryNo].moneyInPool += 10;
        ++ticketsCount;
        lotteries[currentLotteryNo].ticketsBoughtByUserDict[msg.sender][ticketsCount] = true;
        lotteries[currentLotteryNo].ticketsBoughtByUserList[msg.sender].push(ticketsCount);
        lotteries[currentLotteryNo].ticketNuToRndNumber[ticketsCount] = hash_rnd_number;
        lotteries[currentLotteryNo].isTicketRevealed[ticketsCount] = false;
    }
    
    // Allows revealing a ticket for the current reveal stage. The function dynamically computes the winning tickets each time a ticket is successfully revealed.
    function revealRndNumber(uint ticketno, uint rnd_number) public {
        uint revealLotteryNo = getCurrentLotteryNo() - 1;
        bool isTicketBoughtBySender = lotteries[revealLotteryNo].ticketsBoughtByUserDict[msg.sender][ticketno];
        bytes32 hashRndNumber = lotteries[revealLotteryNo].ticketNuToRndNumber[ticketno];
        bytes32 expectedHashRndNumber = keccak256(abi.encode(msg.sender, rnd_number));
        bool verify = (hashRndNumber == expectedHashRndNumber) && isTicketBoughtBySender;
        require(verify,"Check your ticketno and random number.");
        require(lotteries[revealLotteryNo].isTicketRevealed[ticketno] == false, "This ticket has already been revealed.");
        lotteries[revealLotteryNo].isTicketRevealed[ticketno] == true;
        lotteries[revealLotteryNo].currentXORResult = lotteries[revealLotteryNo].currentXORResult ^ rnd_number;
        lotteries[revealLotteryNo].ticketsInLottery.push(ticketno);
        uint range = log2ToInt(lotteries[revealLotteryNo].moneyInPool);
        if (!isPowerOf2(lotteries[revealLotteryNo].moneyInPool)){
            range++;
        }
        for(uint i=1; i<= range; i++) {
            uint winnerIndexNumber = (lotteries[revealLotteryNo].currentXORResult ^ i) % lotteries[revealLotteryNo].ticketsInLottery.length; //TO-DO: Requires improvement!
            if(!lotteries[revealLotteryNo].isPrizesDetermined){
                uint iThPrize = (lotteries[revealLotteryNo].moneyInPool / (2**i)) + ((lotteries[revealLotteryNo].moneyInPool / (2**(i-1))) % 2 );
                lotteries[revealLotteryNo].prizes.push(iThPrize);
		        lotteries[revealLotteryNo].winningTickets.push(lotteries[revealLotteryNo].ticketsInLottery[winnerIndexNumber]);
            }
            else{
                lotteries[revealLotteryNo].winningTickets[i-1] = lotteries[revealLotteryNo].ticketsInLottery[winnerIndexNumber];
            }
        }
        lotteries[revealLotteryNo].isPrizesDetermined = true;
    }

    // Returns the number of latest ticket bought by calling user.
    function getLastBoughtTicketNo(uint	lottery_no) public view	returns(uint) {
        uint currentLotteryNo = getCurrentLotteryNo();
        require(lottery_no > 0 && lottery_no <= currentLotteryNo,"Please enter a valid lottery number.");
        require(lotteries[lottery_no].ticketsBoughtByUserList[msg.sender].length>0,"You have not purchased any tickets currently.");
        return lotteries[lottery_no].ticketsBoughtByUserList[msg.sender][lotteries[lottery_no].ticketsBoughtByUserList[msg.sender].length - 1];
    }

    // Returns the number of ith ticket bought by calling user.
    function getIthBoughtTicketNo(uint i, uint lottery_no) public view	returns(uint) {
        uint currentLotteryNo = getCurrentLotteryNo();
        require(lottery_no > 0 && lottery_no <= currentLotteryNo,"Please enter a valid lottery number.");
        require(i<=lotteries[lottery_no].ticketsBoughtByUserList[msg.sender].length,"Please enter a valid ticket number.");
        return lotteries[lottery_no].ticketsBoughtByUserList[msg.sender][i-1];
    }

    // Returns the total amount of prize won by the provided ticket for the provided lottery round.
    function checkIfTicketWon(uint lottery_no, uint ticket_no) public view returns (uint amount) {
        uint currentLotteryNo = getCurrentLotteryNo();
        require(lottery_no <= currentLotteryNo - 2 && lottery_no > 0,"Please enter a valid lottery number.");
        require(lotteries[lottery_no].ticketsBoughtByUserDict[msg.sender][ticket_no],"Please enter a ticket number that you are authorized.");
        uint totalPrize = 0;
        uint size = lotteries[lottery_no].winningTickets.length;
        for(uint i=0; i< size; i++) {
            if(lotteries[lottery_no].winningTickets[i] == ticket_no) {
                totalPrize += lotteries[lottery_no].prizes[i];
            }
        }
        return totalPrize;
    }

    // Allows withdrawing the prize that the ticket has earned for the provided lottery round.
    function withdrawTicketPrize(uint lottery_no, uint ticket_no) public {
        uint currentLotteryNo = getCurrentLotteryNo();
        require((lottery_no <= currentLotteryNo - 2) && (lottery_no > 0),"Please enter a valid lottery number.");
        require(lotteries[lottery_no].isPrizeWithdrawn[ticket_no]==false,"The prize for this ticket has already been withdrawn.");
        lotteries[lottery_no].isPrizeWithdrawn[ticket_no] = true;
        uint amount = checkIfTicketWon(lottery_no,ticket_no);
        require(amount > 0,"This ticket has not won any prizes.");
        ERC20Token contractobj = ERC20Token(contractaddr) ;
        contractobj.transfer(msg.sender, amount);
    }

    // Returns the id of ticket winning the ith prize and the amount of ith prize.
    function getIthWinningTicket(uint i, uint lottery_no) public view returns (uint ticket_no, uint amount) {
        uint currentLotteryNo = getCurrentLotteryNo();
        require((lottery_no <= currentLotteryNo - 2) && (lottery_no > 0),"Please enter a valid lottery number.");
        require(i <= lotteries[lottery_no].winningTickets.length,"Please enter a valid prize index.");
        return (lotteries[lottery_no].winningTickets[i-1], lotteries[lottery_no].prizes[i-1]);
    }

    // Returns the id of current lottery round.
    function getCurrentLotteryNo() public view returns (uint lottery_no) {
        uint currentTimeStamp = block.timestamp;
        return ((currentTimeStamp - initialTimeStamp)/LOTTERY_DURATION) + 1;
    }

    // Returns the amount of money in the pool for the provided lottery round.
    function getMoneyCollected(uint	lottery_no) public view	returns	(uint amount) {
        return lotteries[lottery_no].moneyInPool;
    }

    // REFERENCE: https://medium.com/coinmonks/math-in-solidity-part-5-exponent-and-logarithm-9aef8515136e
    // Returns the ceil of log2(x).
    function log2ToInt(uint x) internal pure returns(uint result) {
        uint n = 0;
        if (x >= 2**128) { x >>= 128; n += 128; }
        if (x >= 2**64) { x >>= 64; n += 64; }
        if (x >= 2**32) { x >>= 32; n += 32; }
        if (x >= 2**16) { x >>= 16; n += 16; }
        if (x >= 2**8) { x >>= 8; n += 8; }
        if (x >= 2**4) { x >>= 4; n += 4; }
        if (x >= 2**2) { x >>= 2; n += 2; }
        if (x >= 2**1) { /* x >>= 1; */ n += 1; }
        return n;
    }

    // Checks whether an integer is power of two.
    function isPowerOf2(uint x) internal pure returns(bool result) {
        return (x & (x - 1)) == 0;
    }
}
