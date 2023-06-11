// SPDX-License-Identifier: MIT
/**
* @author Andrae Aldrete  Github:Onn_drE   Twitter:Onn_drE
* 
* Smart conntract to grant access to the Notion Chat app with the condition that they have to pay a minimum of $5 to mint.
* Currently set to $0.05 for testing purposes. Used thirdweb contractKit and deploy tool. Real time price conversion 
* provided by Chainlink Data Feeds.
*/
pragma solidity ^0.8.0;

import "@thirdweb-dev/contracts/base/ERC721Base.sol";
import "@thirdweb-dev/contracts/openzeppelin-presets/utils/Counters.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
// chainlink price feed
import "./PriceConverter.sol";

contract NotionChatToken is ERC721Base {
    using PriceConverter for uint256;
    using Counters for Counters.Counter;
    using Strings for uint256;

    Counters.Counter private _tokenIdCounter;
    // Minimum price to mint NFT in MATIC
    uint256 public constant MINIMUM_USD = 5 * 10 ** 16;
    mapping(address => bool) public hasMinted;
   // Default token Metadata URI
    string constant defaultTokenURI = "https://gateway.pinata.cloud/ipfs/QmZda6FPLNdDz8UCdpvF986m1MoNHCpjEczPZfKMdJsjno";

    /**
    * @param _name: name of the whole NFT bundle Collection
    * @param _symbol: symbol of the whole NFT bundle Collection
    */
    constructor(
        string memory _name,
        string memory _symbol,
        address _royaltyRecipient,
        uint128 _royaltyBps
    )
        ERC721Base(
            _name,
            _symbol,
            _royaltyRecipient,
            _royaltyBps
        )
    {}

    /**
    * @dev createToken mint the ERC721 Token with the check that the user has paid minimum
    */
    function createToken() public payable {
       // require statement to check the user has paid minimum to mint the NFT
        require(msg.value.getConversionRate() >= MINIMUM_USD, "SEND_MORE_MATIC");
        // Check that the msg.sender has not minted before
        require(!hasMinted[msg.sender], "ALREADY_MINTED");

        // Increment it so next time it's correct when we call .current()
        _tokenIdCounter.increment();

        // Current counter value will be the minted token's token ID.
        uint256 newTokenId = _tokenIdCounter.current();

        // Mint the token
        _mint(msg.sender, newTokenId);

        // Set the value of minted to true for the msg.sender
        hasMinted[msg.sender] = true;
        
        // Transfer funds to contract's owner
        (bool callSuccess, ) = payable(owner()).call{value: msg.value}("");
        require(callSuccess,"TRANSFER_FUND_FAIL");
    }

    /**
    * @dev function to withdraw funds present in contract address to owner address.
    */
    function withdraw() public onlyOwner(){
        (bool callSuccess, ) = payable(msg.sender).call{value: address(this).balance}("");
        require(callSuccess,"TRANSFER_FUND_FAIL");
    }

    /**
    * @dev view / Getter function to get the balance of the smart contract
    */
    function getContractBalance() public view returns(uint){
        return address(this).balance;
    }

    // Override function to return default token URI for every token
   function tokenURI(uint256 tokenId) public view override returns (string memory) {
       return defaultTokenURI;
   }

    // receive() is called if msg.data is empty
    receive() external payable {}

}