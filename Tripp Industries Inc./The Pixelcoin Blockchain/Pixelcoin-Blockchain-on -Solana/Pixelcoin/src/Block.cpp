#include "Pixelcoin/Block.h"
#include "Pixelcoin/MergeSort.h"

Block::Block(int index, const std::string& previousHash)
{
    Index = index;
    PreviousHash = previousHash;
    Timestamp = time(nullptr);
}

void Block::AddTransaction(const Transaction& tx)
{
    Transactions.push_back(tx);
}

void Block::Finalize()
{
    // Merge-Link rule: always merge sort before sealing
    MergeSort::Sort(Transactions);

    // Fake hash for now (real hash later)
    Hash = std::to_string(Index) + PreviousHash + std::to_string(Timestamp);
}
