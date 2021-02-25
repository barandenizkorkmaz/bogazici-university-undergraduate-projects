var hasher = [
    {
        "inputs": [],
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
                "internalType": "uint256",
                "name": "randomNumber",
                "type": "uint256"
            }
        ],
        "name": "getHash",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "hashValue",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
