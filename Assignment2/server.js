var express = require('express');
var app = express();

Web3 = require('web3')
fs = require('fs');
solc = require('solc')

web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:8545"))
code = fs.readFileSync('contract.sol').toString()
compiledCode = solc.compile(code)

console.log({"yo2" : web3.eth.accounts})

abi_main_contract = JSON.parse(compiledCode.contracts[':MainContract'].interface)
MainContract = web3.eth.contract(abi_main_contract)
bytecode_main_contract = compiledCode.contracts[':MainContract'].bytecode

abi_creator = JSON.parse(compiledCode.contracts[':Creator'].interface)
Creator = web3.eth.contract(abi_creator)
bytecode_creator = compiledCode.contracts[':Creator'].bytecode

deployedContract = MainContract.new({data: bytecode_main_contract, from: web3.eth.accounts[0], gas: 4700000},
  (err, contract) => {
    console.log("ERROR?? ", err, contract)
    if (contract.address != undefined){
      contractInstance = MainContract.at(deployedContract.address)
      // contractInstance.make_creator({from: web3.eth.accounts[0], gas: 470000})
      // make new creator : 
      new_creator = Creator.new(contract.address, {data: bytecode_creator, from: web3.eth.accounts[0], gas: 4700000},
        (err, creator) => {
          if (creator.address != undefined) {
            console.log("Creator1 address : ", creator.address)
            creator1 = Creator.at(creator.address)
            // creator1.received_payment((err, res) => {
            //   console.log("YO RECEIVED PAYMENT", err, res);
            //   creator1.publish_url(web3.eth.accounts[9], 0, "LOL_URL", {from: web3.eth.accounts[1], gas: 4700000});
            // })

          }
        }
      )
    }
  }
)

// get_abi_addr
app.get('/get_abi_addr', function(req, res){
  result = {};
  result["abi"] = abi_main_contract;
  result["addr"] = deployedContract.address;
  res.send(result)
});


// is_creator
// app.get('/is_creator', function(req, res){
//   console.log(req.query)
//   is_creator = contractInstance.is_creator({from: req.query.address, gas: 470000})
//   res.send(is_creator)
// });

// make_creator
app.get('/make_creator', function(req, res){
  contractInstance.make_creator({from : req.query.address})
  res.send("done")
})

// multi contract make creator
app.get('/make_creator', function(req, res){
  c1 = Creator.new(deployedContract.address, {data: bytecode_creator, from: req.query.address, gas: 4700000},
        (err, creator) => {
          if (creator.address != undefined)
          {
            console.log("New creator made. Address : ", creator.address)
            contractInstance.add_creator(creator.address, {from: web3.eth.accounts[1], gas: 4700000})
            resp = {success: true, creator_contract_addr: creator.address, creator_abi: abi_creator}
            res.send(resp)
          }
        }
      )
  res.send({success: false})
})

// add_media
// app.get('/add_media', function(req, res){
//   console.log(req.query)
//   var new_stakes = []
//   for (var i = 0; i < req.query.stake.length; i++)
//     new_stakes.push(parseInt(req.query.stake[i]))
//   console.log(web3.toWei(parseInt(req.query.cost_individual), 'ether'), new_stakes)
//   contractInstance.add_media(
//     web3.toWei(parseInt(req.query.cost_individual), 'ether'), 
//     web3.toWei(parseInt(req.query.cost_company), 'ether'),
//     req.query.stake_addr,
//     new_stakes,
//     {data: byteCode, from: req.query.address, gas: 4700000}
//   )
//   res.send("done")
// })

// multi contract add media
app.get('/add_media', function(req, res){
  console.log(req.query)
  var new_stakes = []
  for (var i = 0; i < req.query.stake.length; i++)
    new_stakes.push(parseInt(req.query.stake[i]))
  console.log(web3.toWei(parseInt(req.query.cost_individual), 'ether'), new_stakes)
  creatorInstance = Creator.at(req.query.creator_contract_addr)
  creatorInstance.add_media(
    web3.toWei(parseInt(req.query.cost_individual), 'ether'), 
    web3.toWei(parseInt(req.query.cost_company), 'ether'),
    req.query.stake_addr,
    new_stakes,
    {data: byteCode, from: req.query.address, gas: 4700000}
  )
})

// get_all_media
app.get('/get_all_media', function(req, res){
  console.log(req.query.address)
  all_media = contractInstance.get_all_media(
    (req.query.is_individual == 'true'),
    {from : req.query.address}
  )
  res.send(all_media)
})

// buy_media
app.get('/buy_media', function(req, res){
  console.log(req.query)
  all_media = contractInstance.buy_media(
    req.query.creator, // TODO parse to addr
    parseInt(req.query.media_id),
    (req.query.is_individual == 'true'),
    {from : req.query.address, value: parseInt(req.query.cost), gas: 470000}
  )
  res.send(all_media)
})

// publish_url
app.get('/publish_url', function(req, res){
  console.log("Publish URL called, ", req.query)
  creatorInstance = Creator.at(req.query.creator_contract_addr)
  creatorInstance.publish_url(
    req.query.consumer,
    parseInt(req.query.media_id),
    req.query.url,
    {from : req.query.address}
  )
  res.send("done")
})

// get_media
app.get('/get_media', function(req, res){
  media_url = contractInstance.get_media(
    req.query.creator,
    parseInt(req.query.media_id),
    {from : req.query.address}
  )
  console.log(media_url)
  res.send(media_url)
})

var server = app.listen(8081, function () {
  var host = server.address().address
  var port = server.address().port
  console.log("App listening at http://%s:%s", host, port)
})