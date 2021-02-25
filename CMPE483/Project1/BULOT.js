var bulotC = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "conaddr",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "stateMutability": "nonpayable",
        "type": "fallback"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "hash_rnd_number",
                "type": "bytes32"
            }
        ],
        "name": "buyTicket",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "lottery_no",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "ticket_no",
                "type": "uint256"
            }
        ],
        "name": "checkIfTicketWon",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "contractaddr",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getCurrentLotteryNo",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "lottery_no",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "i",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "lottery_no",
                "type": "uint256"
            }
        ],
        "name": "getIthBoughtTicketNo",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "i",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "lottery_no",
                "type": "uint256"
            }
        ],
        "name": "getIthWinningTicket",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "ticket_no",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "lottery_no",
                "type": "uint256"
            }
        ],
        "name": "getLastBoughtTicketNo",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "lottery_no",
                "type": "uint256"
            }
        ],
        "name": "getMoneyCollected",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "ticketno",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "rnd_number",
                "type": "uint256"
            }
        ],
        "name": "revealRndNumber",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "lottery_no",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "ticket_no",
                "type": "uint256"
            }
        ],
        "name": "withdrawTicketPrize",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
