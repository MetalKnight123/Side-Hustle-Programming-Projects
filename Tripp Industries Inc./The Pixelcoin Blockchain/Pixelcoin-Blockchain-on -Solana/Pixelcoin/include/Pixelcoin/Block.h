#pragma once
#include <vector>
#include <string>
#include "Transaction.h"

class Block {
public:
    int Index;
    long Timestamp;
    std::vector<Transaction> Transactions;
    std::string PreviousHash;
    std::string Hash;

    Block(int index, const std::string& previousHash);

    void AddTransaction(const Transaction& tx);
    void Finalize();
};
