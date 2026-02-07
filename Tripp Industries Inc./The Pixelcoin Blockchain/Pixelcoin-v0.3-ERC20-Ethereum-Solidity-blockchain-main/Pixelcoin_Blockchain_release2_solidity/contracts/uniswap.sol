// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IUniswapV2Router02 {
    function addLiquidityETH(
        address token,
        uint amountTokenDesired,
        uint amountTokenMin,
        uint amountETHMin,
        address to,
        uint deadline
    ) external payable returns (
        uint amountToken,
        uint amountETH,
        uint liquidity
    );

    function WETH() external pure returns (address);
}

interface IERC20 {
    function approve(address spender, uint256 amount) external returns (bool);
}

contract PixelcoinLiquidity {

    IUniswapV2Router02 public uniswapRouter;
    address public pixelcoin;

    constructor(address _pixelcoin, address _uniswapRouter) {
        pixelcoin = _pixelcoin;
        uniswapRouter = IUniswapV2Router02(_uniswapRouter);
    }

    function addLiquidity(uint256 tokenAmount) external payable {
        // Transfer tokens from sender to this contract first (make sure sender approved this contract)
        IERC20(pixelcoin).approve(address(uniswapRouter), tokenAmount);

        // Add liquidity to Uniswap pool (token + ETH)
        uniswapRouter.addLiquidityETH{value: msg.value}(
            pixelcoin,
            tokenAmount,
            0, // slippage is ignored here for simplicity
            0,
            msg.sender, // liquidity tokens receiver
            block.timestamp + 300
        );
    }

    // to receive ETH
    receive() external payable {}
}
