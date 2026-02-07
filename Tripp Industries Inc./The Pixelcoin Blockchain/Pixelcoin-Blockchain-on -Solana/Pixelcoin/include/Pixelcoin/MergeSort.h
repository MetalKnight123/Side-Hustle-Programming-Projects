#pragma once
#include <vector>
#include "Transaction.h"

class MergeSort {
public:
    static void Sort(std::vector<Transaction>& txs);

private:
    static void Merge(
        std::vector<Transaction>& left,
        std::vector<Transaction>& right,
        std::vector<Transaction>& result
    );
};
