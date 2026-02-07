#include "Pixelcoin/Transaction.h"

Transaction::Transaction(
    const std::string& from,
    const std::string& to,
    double amount,
    long timestamp
)
{
    From = from;
    To = to;
    Amount = amount;
    Fee = 0.001; // fixed fee, no games
    Timestamp = timestamp;
}

bool Transaction::operator<(const Transaction& other) const
{
    if (Timestamp == other.Timestamp)
        return Fee > other.Fee; // higher fee first if same time

    return Timestamp < other.Timestamp;
}
