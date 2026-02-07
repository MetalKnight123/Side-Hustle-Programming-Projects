// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PixelcoinMergeChain {
    struct Block {
        uint256 id;
        bytes32 prevHash;
        bytes32 blockHash;
        address miner;
        string data;
        uint256 timestamp;
    }

    mapping(uint256 => Block) public blocks;
    uint256 public latestBlockId;

    event BlockMined(uint256 indexed id, address indexed miner, bytes32 hash);

    constructor() {
        // Genesis block
        bytes32 genesisHash = keccak256(abi.encodePacked(block.timestamp, msg.sender, "Genesis Block"));
        blocks[0] = Block({
            id: 0,
            prevHash: 0x0,
            blockHash: genesisHash,
            miner: msg.sender,
            data: "Genesis Block",
            timestamp: block.timestamp
        });
        latestBlockId = 0;

        emit BlockMined(0, msg.sender, genesisHash);
    }

    function addBlock(string memory _data) public {
        uint256 newBlockId = latestBlockId + 1;
        bytes32 prevHash = blocks[latestBlockId].blockHash;
        bytes32 newHash = keccak256(abi.encodePacked(block.timestamp, msg.sender, _data, prevHash));

        blocks[newBlockId] = Block({
            id: newBlockId,
            prevHash: prevHash,
            blockHash: newHash,
            miner: msg.sender,
            data: _data,
            timestamp: block.timestamp
        });

        latestBlockId = newBlockId;

        emit BlockMined(newBlockId, msg.sender, newHash);
    }

    function getBlock(uint256 blockId) public view returns (
        uint256 id,
        bytes32 prevHash,
        bytes32 blockHash,
        address miner,
        string memory data,
        uint256 timestamp
    ) {
        Block memory b = blocks[blockId];
        return (b.id, b.prevHash, b.blockHash, b.miner, b.data, b.timestamp);
    }

    function getLatestBlockHash() public view returns (bytes32) {
        return blocks[latestBlockId].blockHash;
    }

    function getChainLength() public view returns (uint256) {
        return latestBlockId + 1;
    }
}
