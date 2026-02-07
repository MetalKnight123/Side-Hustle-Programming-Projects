#include "Pixelcoin/Blockchain.h"

Blockchain::Blockchain()
{
    CirculatingSupply = 0.0;
    Chain.push_back(CreateGenesisBlock());
}

Block Blockchain::CreateGenesisBlock()
{
    return Block(0, "GENESIS");
}

void Blockchain::AddTransaction(const Transaction& tx)
{
    if (CirculatingSupply + tx.Amount > MaxSupply)
        return; // hard cap means hard cap

    PendingTransactions.push_back(tx);
}

void Blockchain::MineBlock()
{
    Block block(
        static_cast<int>(Chain.size()),
        Chain.back().Hash
    );

    for (const auto& tx : PendingTransactions) {
        block.AddTransaction(tx);
        CirculatingSupply += tx.Amount;
    }

    block.Finalize();
    Chain.push_back(block);
    PendingTransactions.clear();
}

double Blockchain::GetCirculatingSupply() const
{
    return CirculatingSupply;
}
