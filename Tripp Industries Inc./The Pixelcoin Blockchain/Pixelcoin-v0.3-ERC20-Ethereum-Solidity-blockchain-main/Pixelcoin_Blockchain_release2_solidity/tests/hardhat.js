const [deployer] = await ethers.getSigners();
const Pixelcoin = await ethers.getContractFactory("Pixelcoin");
const token = await Pixelcoin.deploy(deployer.address);
