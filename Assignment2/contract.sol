pragma solidity ^0.4.18;

contract Creator {

  // Event to notify 
  event received_payment(address consumer, uint media_id);

  struct StakeHolder {
    address stake_holder_address; // Address of stake_holder
    uint8 share;  // share given to stake_holder
  }

  struct Media {
    uint uid;
    uint cost_individual;
    uint cost_company;
    uint num_stake_holder;
    mapping (uint => StakeHolder) stake_holder_map;
    mapping (address => bool) consumers; // all customers who bought this media
    mapping (address => bytes32) encrypted_url;
  }

  address owner;
  MainContract main_contract;
  Media[] media_array;

  // Consturctor takes main_contract address
  function Creator(address main_contract_addr) public {
    owner = msg.sender;
    main_contract = MainContract(main_contract_addr);
  }

  // Add a new media
  function add_media(uint cost_individual, uint cost_company, address[] stake_addr, uint8[] stakes) public {
    // Basic checks
    require(msg.sender == owner);
    require(stake_addr.length == stakes.length);
    require(stake_addr.length > 0);
    require(cost_individual > 0);
    require(cost_company > 0);
    require(media_array.length <= 10);
    
    media_array.push(Media(media_array.length, cost_individual, cost_company, stake_addr.length));
    Media storage m = media_array[media_array.length - 1];

    // Populate the stake_holders
    for (uint i = 0; i < stake_addr.length; ++i) {
      m.stake_holder_map[i] = StakeHolder(stake_addr[i], stakes[i]);
    }
  }

  // Get all media for consumer
  // Limited to 10 media per creator
  // Returns (size, media_id, cost)
  function get_all_media(bool is_individual) view public returns (uint, uint[10], uint[10]) {
    uint[10] memory media_ids;
    uint[10] memory costs;

    for(uint i=0; i<media_array.length; ++i){
      media_ids[i] = media_array[i].uid;
      if(media_array[i].consumers[tx.origin]) costs[i] = 0;
      else if(is_individual) costs[i] = media_array[i].cost_individual;
      else costs[i] = media_array[i].cost_company;
    }
    return (media_array.length, media_ids, costs);
  }

  // Consumer can buy media
  function buy_media(uint media_id, bool is_individual) public payable {
    require(media_id < media_array.length);
    
    Media storage m = media_array[media_id];
    require(!m.consumers[tx.origin]);
    if(is_individual) require(msg.value == m.cost_individual);
    else require(msg.value == m.cost_company);

    m.consumers[tx.origin] = true;
    
    uint total_shares = 0;
    for(uint8 i=0; i<m.num_stake_holder; ++i){
      total_shares += m.stake_holder_map[i].share;
    }
    
    for(i=0; i<m.num_stake_holder; ++i){
      uint amount = (msg.value * uint(m.stake_holder_map[i].share)) / uint(total_shares);
      m.stake_holder_map[i].stake_holder_address.transfer(amount);
    }
    received_payment(tx.origin, media_id);
  }

  // Creator to publish encrypted url
  // Notify main_contract that the url has been published
  function publish_url(address consumers_id, uint media_id, bytes32 url) public {
    require(msg.sender == owner);
    require(media_id < media_array.length);
    media_array[media_id].encrypted_url[consumers_id] = url;
    main_contract.notify_consumer(consumers_id, media_id);
  }

  // Consumer can get the url
  function get_media(uint media_id) view public returns (bytes32) {
    require(media_id < media_array.length);
    return media_array[media_id].encrypted_url[tx.origin];
  }
}


contract MainContract {
  
  // Address and mapping of creators
  address[] creator_addr;
  mapping(address => bool) creator_exist;
  mapping(address => Creator) creator_map;

  // Event to notify consumer that his media url has been published
  event received_media(address creator, address consumer, uint media_id);

  // Calls event received_media
  function notify_consumer(address consumer, uint media_id) public {
    require(creator_exist[msg.sender]);
    received_media(msg.sender, consumer, media_id);
  }

  // Add a new creator
  function add_creator(address c_addr) public {
    require(!creator_exist[c_addr]);
    creator_exist[c_addr] = true;
    creator_map[c_addr] = Creator(c_addr);
    creator_addr.push(c_addr);
  }

  // Get all media for consumer
  function get_all_media(bool is_individual) view public returns (address[], uint[], uint[10][], uint[10][]) {
    uint[] memory sizes = new uint[](creator_addr.length);
    uint[10][] memory media_id_array = new uint[10][](creator_addr.length);
    uint[10][] memory cost_array = new uint[10][](creator_addr.length);

    for(uint i=0; i<creator_addr.length; ++i){
      uint size;
      uint[10] memory media_id;
      uint[10] memory cost;
      (size, media_id, cost) = creator_map[creator_addr[i]].get_all_media(is_individual);
      sizes[i] = size;
      media_id_array[i] = media_id;
      cost_array[i] = cost;
    }
    return (creator_addr, sizes, media_id_array, cost_array);
  }

  // Consumer can buy media
  function buy_media(address creator, uint media_id, bool is_individual) public payable {
    require(creator_exist[creator]);
    creator_map[creator].buy_media.value(msg.value)(media_id, is_individual);
  }

  // Consumer can get the url
  function get_media(address creator, uint media_id) view public returns (bytes32) {
    require(creator_exist[creator]);
    return creator_map[creator].get_media(media_id);
  }
}