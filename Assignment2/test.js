Web3 = require('web3')
fs = require('fs');
solc = require('solc')

web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
code = fs.readFileSync('contract.sol').toString()

compiledCode = solc.compile(code)

console.log(compiledCode)

abiDefinition = JSON.parse(compiledCode.contracts[':MainContract'].interface)
// VotingContract = web3.eth.contract(abiDefinition)
// byteCode = compiledCode.contracts[':Voting'].bytecode
// deployedContract = VotingContract.new(['Rama','Nick','Jose'],{data: byteCode, from: web3.eth.accounts[0], gas: 4700000})
// deployedContract.address
// contractInstance = VotingContract.at(deployedContract.address)

// console.log("done till line 19")
// console.log(contractInstance) 

// console.log(contractInstance.totalVotesFor.call('Rama'))