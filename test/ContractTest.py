from web3 import Web3, HTTPProvider



import unittest, json




class ContractTest(unittest.TestCase):
    other_test_acct = "0x6F05560Cf14ddD9569bd5636c0006A9133977516"
    main_address = "0xbCD18E8a0bD51c8F4c6E3b5b258D7e43fB4359CC" 
    key_file = open(".secret", "r")
    main_address_privateKey = key_file.read()
    PATH_TRUFFLE_WK = '/Users/afolabi/sol_CreateToken'
    truffleFile = json.load(open(PATH_TRUFFLE_WK + '/build/contracts/AFOLABI_BEP20.json'))

    contract_abi = truffleFile['abi']
    contract_address = truffleFile['networks']['97']['address']

    web3_instantce = Web3(HTTPProvider("https://data-seed-prebsc-1-s1.binance.org:8545"))
    contract_instance = web3_instantce.eth.contract(address=contract_address, abi=contract_abi)
    def setUp(self) -> None:
        self.nounce = self.web3_instantce.eth.get_transaction_count(self.main_address)
        self.app_amt = 1000

        return super().setUp()

    def test_001_Check_Connection(self):
        check_connect = self.web3_instantce.isConnected()
        self.assertTrue(check_connect == True)
        print("test_001_Check_connection Passed")

    def test_002_Check_Contract_address(self):
        deployed_contract_address = self.contract_address
        self.assertTrue(deployed_contract_address != "0x0")
        self.assertTrue(deployed_contract_address != 0x0)
        self.assertNotEqual(deployed_contract_address, '')
        self.assertTrue(deployed_contract_address != 'null')
        self.assertTrue(deployed_contract_address != 'undefined')
        print("test_002_Check_Contract_address Passed")

    def test_003_Check_token_details(self):
        balance = self.contract_instance.functions.balanceOf(self.main_address).call() # This will not be check, balance will change
        token_name = self.contract_instance.functions.name().call()
        token_symbol = self.contract_instance.functions.symbol().call()
        token_decimal = self.contract_instance.functions.decimals().call()
        token_supply = self.contract_instance.functions.totalSupply().call() #This will return +5 zeros which is numbal of our decimal places

        self.assertTrue(token_name == 'AFOLABI_BEP20 Token')
        self.assertTrue(token_symbol == 'AFOO')
        self.assertTrue(token_decimal == 5)
        self.assertEqual(token_supply, 100000000000) 

        print("test_003_Check_token_details Passed")


    def test_004_Approve_address(self):
        # ==========================
        #### Approve address
        # ==========================
        transaction = self.contract_instance.functions.approve(
            self.main_address,
            self.app_amt
        ).buildTransaction({
            "gasPrice": self.web3_instantce.eth.gas_price,
            "nonce":self.nounce,

        })
        signed_tx = self.web3_instantce.eth.account.sign_transaction(transaction, self.main_address_privateKey)
        submit_tx = self.web3_instantce.eth.send_raw_transaction(signed_tx.rawTransaction)
        hash = self.web3_instantce.toHex(submit_tx)
        
        wait_tx_complete = self.web3_instantce.eth.wait_for_transaction_receipt(hash)
        transferEvent = self.contract_instance.events.Approval().processReceipt(wait_tx_complete)

        self.assertEqual(transferEvent[0]['args']._owner, self.main_address)
        self.assertEqual(transferEvent[0]['args']._spender, self.main_address)
        self.assertEqual(transferEvent[0]['args']._value, self.app_amt)
        print("test_004_Approve_address Passed")

    def test_005_TransferToken(self):
        # =============================
        ## Send Transaction
        # =============================


    
        transaction = self.contract_instance.functions.transfer(
            self.other_test_acct,
            self.app_amt
        ).buildTransaction({
            'chainId':97,
            'gas':70000,
            'gasPrice': self.web3_instantce.eth.gas_price,
            "nonce":self.nounce,

        })
        signed_tx = self.web3_instantce.eth.account.sign_transaction(transaction, self.main_address_privateKey)
        submit_tx = self.web3_instantce.eth.send_raw_transaction(signed_tx.rawTransaction)
        hash = self.web3_instantce.toHex(submit_tx)
        
        wait_tx_complete = self.web3_instantce.eth.wait_for_transaction_receipt(hash)
        transferEvent = self.contract_instance.events.Transfer().processReceipt(wait_tx_complete)

        self.assertTrue(transferEvent[0]['args']._value == self.app_amt)
        self.assertTrue(transferEvent[0]['args']._from == self.main_address)
        self.assertTrue(transferEvent[0]['args']._to == self.other_test_acct)
        print("test_005_TransferToken Passed")


        


if __name__ == "__main__":
    unittest.main()