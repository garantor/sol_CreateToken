const AFOLABI_BEP20 = artifacts.require("AFOLABI_BEP20");

module.exports = function (deployer) {
    deployer.deploy(AFOLABI_BEP20);
};
