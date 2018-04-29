Web3 = require('web3')
fs = require('fs');
solc = require('solc')

web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:8545"))
code = fs.readFileSync('contract.sol').toString()
compiledCode = solc.compile(code)

console.log(compiledCode)

abi_main_contract = JSON.parse(compiledCode.contracts[':MainContract'].interface)
MainContract = web3.eth.contract(abi_main_contract)
bytecode_main_contract = compiledCode.contracts[':MainContract'].bytecode

abi_creator = JSON.parse(compiledCode.contracts[':Creator'].interface)
Creator = web3.eth.contract(abi_creator)
bytecode_creator = compiledCode.contracts[':Creator'].bytecode

mc = MainContract.new({data: bytecode_main_contract, from: web3.eth.accounts[0], gas: 4700000},
  (err, contract) => {
    if (contract.address != undefined) {
      console.log("MainContract address : ", contract.address)
      main_contract = MainContract.at(contract.address)

      main_contract.received_media((err, res) => {
        console.log("YO RECEIVED MEDIA", err, res);
      })


      console.log("Making creator", contract.address)
      c1 = Creator.new(contract.address, {data: bytecode_creator, from: web3.eth.accounts[1], gas: 4700000},
        (err, creator) => {
          if (creator.address != undefined) {
            console.log("Creator1 address : ", creator.address)
            creator1 = Creator.at(creator.address)
            creator1.received_payment((err, res) => {
              console.log("YO RECEIVED PAYMENT", err, res);
              creator1.publish_url(web3.eth.accounts[9], 0, "LOL_URL", {from: web3.eth.accounts[1], gas: 4700000});
            })
            main_contract.add_creator(creator.address, {from: web3.eth.accounts[1], gas: 4700000})
            console.log("Done making creator")

            res = main_contract.get_all_media(true, {from: web3.eth.accounts[9]})
            console.log("Before adding media", res[0], res[1], res[2], res[3])
            
            console.log(creator1.add_media(web3.toWei(1, 'ether'), web3.toWei(4, 'ether'), [web3.eth.accounts[6], web3.eth.accounts[5]], [5, 3], {from: web3.eth.accounts[1], gas: 4700000}))
            console.log(creator1.add_media(web3.toWei(2, 'ether'), web3.toWei(5, 'ether'), [web3.eth.accounts[6], web3.eth.accounts[5]], [5, 3], {from: web3.eth.accounts[1], gas: 4700000}))
            console.log(creator1.add_media(web3.toWei(3, 'ether'), web3.toWei(6, 'ether'), [web3.eth.accounts[6], web3.eth.accounts[5]], [5, 3], {from: web3.eth.accounts[1], gas: 4700000}))


            res = main_contract.get_all_media(true, {from: web3.eth.accounts[9]})
            console.log("After adding media", res[0], res[1], res[2], res[3])
          
            // console.log("Payment", main_contract.buy_media(creator.address, 0, true, {from: web3.eth.accounts[9], value: web3.toWei(5, 'ether'), gas: 4700000}))

          }
        }
      )

      // acct_address = web3.eth.accounts[0]
      // main_contract.make_creator({data: byteCode, from: acct_address, gas: 4700000})
      // console.log("Testing get_all_creators", main_contract.get_all_creators({data: byteCode, from: acct_address, gas: 4700000}))
      // main_contract.add_media(web3.toWei(5, 'ether'), web3.toWei(4, 'ether'), [web3.eth.accounts[6], web3.eth.accounts[5]], [50, 30], {data: byteCode, from: acct_address, gas: 4700000})
      // media_list = main_contract.get_all_media('true', {data: byteCode, from: web3.eth.accounts[5], gas: 4700000})
      // console.log("Testing get_all_media", media_list)
      // media_id = 0
      // wei_value = media_list[2][media_id]
      // console.log("Value in wei : ", wei_value)
      // console.log(web3.eth.getBalance(web3.eth.accounts[6]), web3.eth.getBalance(web3.eth.accounts[5]), 'Before');
      // console.log("Testing buy media", main_contract.buy_media(media_list[0][media_id], media_list[1][media_id], true, {data: byteCode, from: web3.eth.accounts[4], gas: 4700000, value: wei_value}))
      // console.log(web3.eth.getBalance(web3.eth.accounts[6]), web3.eth.getBalance(web3.eth.accounts[5]), 'After buy media', web3.eth.getBalance(web3.eth.accounts[4]));
    }
  }
)

