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
      
      console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");

      contractInstance.received_payment((err, res) => {
        console.log("YO RECEIVED PAYMENT", err, res);
        contractInstance.publish_url(res.args.media_id, res.args.consumer, "RANDOM URL", {data: byteCode, from: res.args.creator, gas: 4700000})
      })

      contractInstance.received_media((err, res) => {
        console.log("YO RECEIVED MEDIA", err, res);
      })

      acct_address = web3.eth.accounts[0]
      contractInstance.make_creator({data: byteCode, from: acct_address, gas: 4700000})
      console.log("Testing get_all_creators", contractInstance.get_all_creators({data: byteCode, from: acct_address, gas: 4700000}))
      contractInstance.add_media(web3.toWei(5, 'ether'), web3.toWei(4, 'ether'), [web3.eth.accounts[6], web3.eth.accounts[5]], [50, 30], {data: byteCode, from: acct_address, gas: 4700000})
      media_list = contractInstance.get_all_media('true', {data: byteCode, from: web3.eth.accounts[5], gas: 4700000})
      console.log("Testing get_all_media", media_list)
      media_id = 0
      wei_value = media_list[2][media_id]
      console.log("Value in wei : ", wei_value)
      console.log(web3.eth.getBalance(web3.eth.accounts[6]), web3.eth.getBalance(web3.eth.accounts[5]), 'Before');
      console.log("Testing buy media", contractInstance.buy_media(media_list[0][media_id], media_list[1][media_id], true, {data: byteCode, from: web3.eth.accounts[4], gas: 4700000, value: wei_value}))
      console.log(web3.eth.getBalance(web3.eth.accounts[6]), web3.eth.getBalance(web3.eth.accounts[5]), 'After buy media', web3.eth.getBalance(web3.eth.accounts[4]));
    }
  }
)

