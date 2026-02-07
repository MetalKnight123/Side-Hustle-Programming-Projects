#pragma once
#include <string>

class Transaction {
public:
    std::string From;
    std::string To;
    double Amount;
    double Fee;
    long Timestamp;

    Transaction(
        const std::string& from,
        const std::string& to,
        double amount,
        long timestamp
    );

    bool operator<(const Transaction& other) const;
};
