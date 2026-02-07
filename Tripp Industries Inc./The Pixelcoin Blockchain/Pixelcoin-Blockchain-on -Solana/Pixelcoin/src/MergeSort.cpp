#include "Pixelcoin/MergeSort.h"

void MergeSort::Sort(std::vector<Transaction>& txs)
{
    if (txs.size() <= 1)
        return;

    size_t mid = txs.size() / 2;
    std::vector<Transaction> left(txs.begin(), txs.begin() + mid);
    std::vector<Transaction> right(txs.begin() + mid, txs.end());

    Sort(left);
    Sort(right);

    txs.clear();
    Merge(left, right, txs);
}

void MergeSort::Merge(
    std::vector<Transaction>& left,
    std::vector<Transaction>& right,
    std::vector<Transaction>& result
)
{
    size_t i = 0, j = 0;

    while (i < left.size() && j < right.size()) {
        if (left[i] < right[j]) {
            result.push_back(left[i++]);
        } else {
            result.push_back(right[j++]);
        }
    }

    while (i < left.size())
        result.push_back(left[i++]);

    while (j < right.size())
        result.push_back(right[j++]);
}
