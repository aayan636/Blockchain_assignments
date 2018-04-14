pragma solidity ^0.4.18;
// We have to specify what version of compiler this code will compile with
// contract Creater {

// }

contract MainContract {
  
  struct Media {
    uint uid;
    uint cost_individual;
    uint cost_company;
    mapping (address => uint8) stake_holders; // stakeholders address to %age
    mapping (address => bool) consumers; // all customers who bought this media 
  }
  
  struct Creator {
    uint num_media;
    bool exists;
    mapping (uint => Media) all_media;
  }

  mapping (address => Creator) creator_map;

  function make_creator() public {
    require(!creator_map[msg.sender].exists);
    creator_map[msg.sender] = Creator(0, true);
  }

  function add_media(address cid, uint cost_individual, uint cost_company, address[] stake_addr, uint8[] stakes /*Media Args here*/) public {
    require(creator_map[cid].exists);
    // TODO : Add stake_holders
    uint m_id = creator_map[cid].num_media;
    creator_map[cid].all_media[m_id] = Media(m_id, cost_individual, cost_company);
    for (uint8 i = 0; i < stake_addr.length; i++) {
      creator_map[cid].all_media[m_id].stake_holders[stake_addr[i]] = stakes[i];
    }
    creator_map[cid].num_media += 1;
  }
}