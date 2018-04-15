Web3 = require('web3')
fs = require('fs');
solc = require('solc')

web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
code = fs.readFileSync('contract.sol').toString()

compiledCode = solc.compile(code)
console.log(compiledCode)

abiDefinition = JSON.parse(compiledCode.contracts[':MainContract'].interface)
MainContract = web3.eth.contract(abiDefinition)
byteCode = compiledCode.contracts[':MainContract'].bytecode

deployedContract = MainContract.new({data: byteCode, from: web3.eth.accounts[0], gas: 4700000},
  (err, contract) => {
    if (contract.address != undefined) {
      console.log("Contract address : ", contract.address)
      console.log("DepContract address : ", deployedContract.address)
      contractInstance = MainContract.at(deployedContract.address)
      acct_address = web3.eth.accounts[0]
      contractInstance.make_creator({data: byteCode, from: acct_address, gas: 4700000})
      console.log(contractInstance.get_all_creators({data: byteCode, from: acct_address, gas: 4700000}))
      contractInstance.add_media(5, 4, [web3.eth.accounts[9], web3.eth.accounts[7]], [50, 30], {data: byteCode, from: acct_address, gas: 4700000})
      // console.log(contractInstance.get_num_media({data: byteCode, from: acct_address, gas: 4700000}))
      console.log(contractInstance.get_all_media(true, {data: byteCode, from: web3.eth.accounts[5], gas: 4700000}))
    }
  }
)