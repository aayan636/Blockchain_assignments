pragma solidity ^0.4.18;
// We have to specify what version of compiler this code will compile with

contract MainContract {
  
  struct Media {
    uint uid;
  }
  
  struct Creator {
    bool exists;
    Media[] media_array;
  }

  mapping (address => Creator) creator_map;

  function make_creator() public {
    require(!creator_map[msg.sender].exists);
    creator_map[msg.sender] = Creator({exists : true});
  }

  function add_media(address cid /*Media Args here*/) public {
    require(creator_map[cid].exists);
    creator_map[cid].media_array.length += 1;
    // TODO : Implement media stuff
  }
}