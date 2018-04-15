pragma solidity ^0.4.18;

contract MainContract {
  
  struct Media {
    uint uid;
    uint cost_individual;
    uint cost_company;
    mapping (address => uint8) stake_holders; // stakeholders address to percentage
    mapping (address => bool) consumers; // all customers who bought this media
  }
  
  struct Creator {
    bool exists;
    uint num_media;
    mapping (uint => Media) all_media;
  }

  mapping (address => Creator) creator_map;
  address[] creator_addresses;

  function make_creator() public returns (uint) {
    require(!creator_map[msg.sender].exists);
    creator_map[msg.sender] = Creator(true, 0);
    creator_addresses.push(msg.sender);
    return creator_addresses.length;
  }

  function add_media(uint cost_individual, uint cost_company, address[] stake_addr, uint8[] stakes) public {
    address cid = msg.sender;
    require(creator_map[cid].exists);
    require(stake_addr.length == stakes.length);
    uint m_id = creator_map[cid].num_media;
    creator_map[cid].all_media[m_id] = Media(m_id, cost_individual, cost_company);
    for (uint8 i = 0; i < stake_addr.length; i++) {
      creator_map[cid].all_media[m_id].stake_holders[stake_addr[i]] = stakes[i];
    }
    creator_map[cid].num_media += 1;
  }

  // function get_num_media() view public returns (uint) {
  //   return creator_map[msg.sender].num_media;
  // }

  function get_all_creators() view public returns (address[]) {
    return creator_addresses;
  }

  function get_all_media(bool is_individual) view public returns (address[], uint[], uint[]) {
    uint size = 0;
    Creator storage creator;
    Media storage m;
    for(uint i=0; i<creator_addresses.length; ++i){
      creator = creator_map[creator_addresses[i]];
      for(uint j=0; j<creator.num_media; ++j){
        m = creator.all_media[j];
        if(m.consumers[msg.sender]) continue;
        size += 1;
      }
    }
    address[] memory creators = new address[](size);
    uint[] memory media_ids = new uint[](size);
    uint[] memory costs = new uint[](size);
    size = 0;
    for(i=0; i<creator_addresses.length; ++i){
      creator = creator_map[creator_addresses[i]];
      for(j=0; j<creator.num_media; ++j){
        m = creator.all_media[j];
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

  function buy_media(bool is_individual) public {
    
  }
}