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
    if (contract.address !== undefined) {
      console.log("Contract address : ", contract.address)
      console.log("DepContract address : ", deployedContract.address)
      contractInstance = MainContract.at(deployedContract.address)
      contractInstance.make_creator.call((err, x) => {
        console.log("Creator made", err, x);
        contractInstance.get_all_creators.call((err, resp) => {
          console.log("get all creators", err, resp)
          // contractInstance.get_all_creators.call((err, resp) => {
          //   console.log("get all creators II", err, resp)
          // })
        })
      });
    }
  }
)

// setTimeout(console.log(contractInstance.get_all_creators.call()), 3000);
// contractInstance = MainContract.at(deployedContract.address)

// console.log(contractInstance)
// contractInstance.make_creator.call();

// contractInstance
// contractInstance.add_media.call();
// console.log(contractInstance.totalVotesFor.call('Rama'))