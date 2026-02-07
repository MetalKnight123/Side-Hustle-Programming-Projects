#pragma once
#include <vector>
#include "Block.h"

class Blockchain {
public:
    static constexpr double MaxSupply = 1000000000.0;

    Blockchain();

    void AddTransaction(const Transaction& tx);
    void MineBlock();

    double GetCirculatingSupply() const;

private:
    std::vector<Block> Chain;
    std::vector<Transaction> PendingTransactions;
    double CirculatingSupply;

    Block CreateGenesisBlock();
};
