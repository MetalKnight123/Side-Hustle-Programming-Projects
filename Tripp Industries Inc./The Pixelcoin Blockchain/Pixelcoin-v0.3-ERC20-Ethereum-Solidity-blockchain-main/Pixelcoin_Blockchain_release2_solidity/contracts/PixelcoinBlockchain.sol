// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PixelcoinBlockchain {
    string public name = "Pixelcoin Blockchain";
    address public owner;

    uint public blockCount = 0;
    uint public totalSupply = 0;
    uint public rewardPerBlock = 10 * (10 ** 18); // 10 Pixelcoins per block

    mapping(address => uint) public balances;

    struct Block {
        uint index;
        address miner;
        string data;
        uint timestamp;
        uint reward;
    }

    mapping(uint => Block) public blocks;

    event NewBlockMined(uint indexed index, address indexed miner, string data, uint reward);
    event Transfer(address indexed from, address indexed to, uint value);

    constructor() {
        owner = msg.sender;
    }

    function mineBlock(string memory data) public {
        blockCount++;

        // Reward the miner
        balances[msg.sender] += rewardPerBlock;
        totalSupply += rewardPerBlock;

        // Store the block
        blocks[blockCount] = Block({
            index: blockCount,
            miner: msg.sender,
            data: data,
            timestamp: block.timestamp,
            reward: rewardPerBlock
        });

        emit NewBlockMined(blockCount, msg.sender, data, rewardPerBlock);
    }

    function transfer(address to, uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(to != address(0), "Invalid recipient");

        balances[msg.sender] -= amount;
        balances[to] += amount;

        emit Transfer(msg.sender, to, amount);
    }

    function balanceOf(address account) public view returns (uint) {
        return balances[account];
    }

    function getBlock(uint index) public view returns (Block memory) {
        require(index > 0 && index <= blockCount, "Invalid block index");
        return blocks[index];
    }
}
