pragma solidity ^0.4.18;

contract MainContract {
  
  event received_payment(address creator, address consumer, uint media_id);
  event received_media(address creator, address consumer, uint media_id);

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
  
  struct Creator {
    bool exists;
    uint num_media;
    mapping (uint => Media) media_map;
  }

  // Address and mapping of creators
  address[] creator_addresses;
  mapping (address => Creator) creator_map;

  // Checks if sender is creator
  function is_creator() view public returns(bool) {
    return creator_map[msg.sender].exists;
  }

  // Initializes a new creator with sender's address
  function make_creator() public {
    require(!creator_map[msg.sender].exists);
    creator_map[msg.sender] = Creator(true, 0);
    creator_addresses.push(msg.sender);
  }

  // Adds media to creator with sender's address
  function add_media(uint cost_individual, uint cost_company, address[] stake_addr, uint8[] stakes) public {
    address cid = msg.sender;

    // Creator should exist
    require(creator_map[cid].exists);
    require(stake_addr.length == stakes.length);
    
    // Get media uid
    uint m_id = creator_map[cid].num_media;
    creator_map[cid].media_map[m_id] = Media(m_id, cost_individual, cost_company, stake_addr.length);
    Media storage m = creator_map[cid].media_map[m_id];

    // Populate the stake_holders
    for (uint i = 0; i < stake_addr.length; ++i) {
      m.stake_holder_map[i] = StakeHolder(stake_addr[i], stakes[i]);
    }
    
    // Assign m to media_map
    creator_map[cid].media_map[m_id] = m;
    creator_map[cid].num_media += 1;
  }

  // Get's all media for consumer
  function get_all_media(bool is_individual) view public returns (address[], uint[], uint[]) {
    uint size = 0;
    Creator storage creator;
    Media storage m;
    
    // Get the number of media to return
    for(uint i=0; i<creator_addresses.length; ++i){
      creator = creator_map[creator_addresses[i]];
      for(uint j=0; j<creator.num_media; ++j){
        m = creator.media_map[j];
        if(m.consumers[msg.sender]) continue;
        size += 1;
      }
    }

    // Init the arrays
    address[] memory creators = new address[](size);
    uint[] memory media_ids = new uint[](size);
    uint[] memory costs = new uint[](size);
    size = 0;

    // Populate the arrays
    for(i=0; i<creator_addresses.length; ++i){
      creator = creator_map[creator_addresses[i]];
      for(j=0; j<creator.num_media; ++j){
        m = creator.media_map[j];
        if(m.consumers[msg.sender]) continue;
        creators[size] = creator_addresses[i];
        media_ids[size] = m.uid;
        if(is_individual) costs[size] = m.cost_individual;
        else costs[size] = m.cost_company;
        size += 1;
      }
    }
    return (creators, media_ids, costs);
  }

  function buy_media(address creator, uint media_id, bool is_individual) public payable {
    require(creator_map[creator].exists);
    require(media_id < creator_map[creator].num_media);
    
    Media storage m = creator_map[creator].media_map[media_id];
    if(is_individual) require(msg.value == m.cost_individual);
    else require(msg.value == m.cost_company);

    m.consumers[msg.sender] = true;
    
    uint total_shares = 0;
    for(uint8 i=0; i<m.num_stake_holder; ++i){
      total_shares += m.stake_holder_map[i].share;
    }
    
    for(i=0; i<m.num_stake_holder; ++i){
      uint amount = (msg.value * uint(m.stake_holder_map[i].share)) / uint(total_shares);
      m.stake_holder_map[i].stake_holder_address.transfer(amount);
    }
    received_payment(creator, msg.sender, media_id);
  }

  function publish_url(uint media_id, address consumers_id, bytes32 url) public {
    require(creator_map[msg.sender].exists);
    require(media_id < creator_map[msg.sender].num_media);
    creator_map[msg.sender].media_map[media_id].encrypted_url[consumers_id] = url;
    received_media(msg.sender, consumers_id, media_id);
  }

  function get_media(address creator, uint media_id) view public returns (bytes32) {
    require(creator_map[creator].exists);
    require(media_id < creator_map[creator].num_media);
    return creator_map[creator].media_map[media_id].encrypted_url[msg.sender];
  }

  // ****************************************************

  // For debugging
  function get_num_media() view public returns (uint) {
    return creator_map[msg.sender].num_media;
  }

  // For debugging
  function get_all_creators() view public returns (address[]) {
    return creator_addresses;
  }

  // ****************************************************
}