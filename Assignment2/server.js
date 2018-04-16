var express = require('express');
var app = express();

Web3 = require('web3')
fs = require('fs');
solc = require('solc')

web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"))
code = fs.readFileSync('contract.sol').toString()
compiledCode = solc.compile(code)

console.log({"yo" : web3.eth.accounts[0]})

abi = JSON.parse(compiledCode.contracts[':MainContract'].interface)
MainContract = web3.eth.contract(abi)
byteCode = compiledCode.contracts[':MainContract'].bytecode

deployedContract = MainContract.new({data: byteCode, from: web3.eth.accounts[0], gas: 4700000},
  (err, contract) => {
    if (contract.address != undefined){
      contractInstance = MainContract.at(deployedContract.address)
    
      contractInstance.received_payment((err, res) => {
        console.log("YO RECEIVED PAYMENT", err, res);
        // contractInstance.publish_url(res.args.media_id, res.args.consumer, "RANDOM URL", {data: byteCode, from: res.args.creator, gas: 4700000})
      })

      contractInstance.received_media((err, res) => {
        console.log("YO RECEIVED MEDIA", err, res);
      })
    }
  }
)

// is_creator
app.get('/is_creator', function(req, res){
  is_creator = contractInstance.is_creator({from : req.query.address})
  res.send(is_creator)
});

// make_creator
app.get('/make_creator', function(req, res){
  contractInstance.make_creator({from : req.query.address})
  res.send("done")
})

// add_media
app.get('/add_media', function(req, res){
  contractInstance.add_media(
    web3.toWei(parseInt(req.query.cost_individual), 'ether'), 
    web3.toWei(parseInt(req.query.cost_company), 'ether'), 
    req.query.stake_addr,/* TODO : FIGURE OUT HOW TO CONVERT THIS*/
    req.query.stakes, /* TODO : FIGURE OUT HOW TO CONVERT THIS*/
    {from : req.query.address, gas: 4700000}
  )
  res.send("done")
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
  all_media = contractInstance.get_all_media(
    (req.query.is_individual == 'true'),
    {from : req.query.address}
  )
  res.send(all_media)
})

// publish_url
app.get('/publish_url', function(req, res){
  contractInstance.publish_url(
    parseInt(req.query.media_id),
    req.query.consumer_id,
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