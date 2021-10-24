## Smart Contracts

Is a self -xecuting set of instructions that is executed without a third party intermidiarie

Smart contracts are written in code.

O Smart Contract ****nada mais é do que uma ferramenta tecnológica que permite a **criação de contratos autoexecutáveis**, que não podem ser perdidos, nem adulterados.

O **Blockchain** é um banco de dados bastante seguro e praticamente a prova de fraudes, que armazena dados em blocos, com registro de data e tempo, e que funciona como uma base de dados distribuída e descentralizada.

Toda vez que um registro é inserido nessa rede, você precisa do consenso de todos os participantes da cadeia, e os dados não podem ser mais apagados (e se forem por um membro, todos os outros ficam sabendo da ação).

Assim, você tem um registro seguro e inviolável dos dados.

uma transferência de moedas só poderia ser executada, caso as condições registradas no **Smart Contract** fossem atendidas, e a própria rede era responsável pela validação das ações.

os Smart Contracts não são exclusivos para transações de criptomoedas, e podem estar presentes no dia a dia do seu escritório.

Na prática, **a codificação de um Smart Contract em Blockchain** permite que apenas as partes envolvidas trabalhem nele. E o código autoexecutável é que aplica as cláusulas contidas no documento.

Isso significa que, depois da assinatura eletrônica de um contrato inteligente, ele passa a ser monitorado por computadores ligados à rede de Blockchain, onde o contrato digital foi registrado.

Em primeiro lugar, a **automação** proporcionada pelo contrato autoexecutável inteligente exige **menos intervenção humana**.

Isso acontece porque a criptografia do Blockchain garante total segurança à relação contratual, mesmo sem a presença dos intermediários.

Além de inviolável, a tecnologia aplicada aos **contratos digitais** autoexecutáveis também é 100% auditável.

Ou seja, qualquer alteração depois da assinatura digital precisa ser necessariamente validada pelas partes, o que impede que alguém tente fraudar o contrato, e qualquer modificação pode ser rastreada facilmente.

1. Decentralized
2. Transparent
3. Speed
4. Immutable
5. Remove Counterparty Risk
6. Allow for trust minimized agreements

---

### Sites:

- MetaMask →A crypto wallet & gateway to blockchain apps
- EtherScan→ track a wallet id
- Remix IDE - run solidity code
- ETH Gas Station →

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b1dc6199-5d86-4eb0-9406-3011a6890d93/Untitled.png)

If you want to get your transaction in right away it will cost 2 gas, in the standard 2 gas and on, on..

because the blockchain needs to priorize the transactions

### Taxes:

**Gas:** Measure of computation use

**Gas Price:** How much it costs per unit of gas

**Gas Limit:** Max amount of gas in a transaction

**Transaction Fee:** Gas Used * Gas Price

**Nonce:** Number Used Once, to find the solution to the blockchain problem

## Signature

Public keys is derived from our private key. Anyone can 'see' it, and use it to verify that a transaction came from you.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/a424c2e1-88d4-4ff1-bb1d-7edb92ee8ac6/Untitled.png)

in this situation I made a transaction for someone else and signed with my private key, after the transaction be completed it will generate a signature

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/2313d676-4ac8-4962-a7fb-7f5b6f18ad6b/Untitled.png)

and we can check if the date send is true with it

Signing a transaction is a one way process. someone with a private key signs a transaction by their private key being hashed with their transaction data.

anyone can then verify this new transaction hash with your public key

## Security

Chain Selection, how do we know wich block is actually the real blockchain and the true one, this is when nakamoto consensus comes in, this is the combination of proof of work and longest chain rule, whichever blockchain has the longest chain or the most number of blocks on it is going to be the chain they will use.

## Proof of work

It a computation to find the solution to the block, the nounce, and it requires a lot of computation work so whoever find the solution first will receive the transaction fee.

## Solidity

**1- Types**

```jsx
// SPDX-License-Identifier: GPL-3.0

// 1 - definin solidity version, use somethin between 0.6.0 and 0.9
pragma solidity >=0.6.0 <0.9.0;

// 2 - contract is a kind on Class in OOP language
contract SimpleStorage {
 
    // types
    uint256 favoriteNumber = 5; //unsigned integer
    bool favoriteBool = true; //boolean
    string favoriteString = "some random word"; // string
    int256 favoriteInt = -5;
    address favoriteAddress = 0x3003466FDE8fEA0691dDA63215C9483b8fb6e944; // etherium account addresss
    bytes32 favoriteBytes = "cat"; //32 is the maxium size of the bytes types
    
}
```

**2 - Functions**

```jsx
// SPDX-License-Identifier: GPL-3.0

// 1 - definin solidity version, use somethin between 0.6.0 and 0.9
pragma solidity >=0.6.0 <0.9.0;

// 2 - contract is a kind on Class in OOP language
contract SimpleStorage {
 
    // types
    uint256 favoriteNumber; // start to 0
    
    // functions
    function storeFavoriteNumber(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber
    }
}
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d543cf46-fc58-4baa-897e-1a97d4b42b7a/Untitled.png)

in this case after complie and deploy our contract we can interact with it in this section

**3 - Methods Type**

1 - external ⇒ the variable or function can't be called inside the contract just from a external contract, one function in this contract can't access

2 - public ⇒ anyone can access

3 - internal ⇒ just function inside the contract can interact

4 - private ⇒ only visible for the contract they are defined in and not derived contracts

```jsx
// SPDX-License-Identifier: GPL-3.0

// 1 - definin solidity version, use somethin between 0.6.0 and 0.9
pragma solidity >=0.6.0 <0.9.0;

// 2 - contract is a kind on Class in OOP language
contract SimpleStorage {
 
    // types
    uint256 favoriteNumber; // start to 0
    
    // functions
    function storeFavoriteNumber(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
    // view => readOnly, read some state in the blockchain and not making a changing
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }
    
    // pure => do some kind of math but not change the state
    function calculate(uint256 number) public pure returns(uint256) {
        return number + number;
    }
    
}
```

```jsx
// SPDX-License-Identifier: GPL-3.0

// 1 - definin solidity version, use somethin between 0.6.0 and 0.9
pragma solidity >=0.6.0 <0.9.0;

// 2 - contract is a kind on Class in OOP language
contract SimpleStorage {
 
    // create our own type
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // object
    People public person = People({favoriteNumber: 2, name: "Person 1"});
 
    // string to find someone favorite number  
    mapping( string => uint256) public nameToFavoriteNumber;
    
    // dynamic array, can have any size
    // if we want to limit the size of this array we can do People[2] for ex
    People[] public people;
    
    // there is 2 ways to store a variable
    // 1 - memory => data will only be stored during the execution of the function and delete after
    // 2 - storage => data will persist even after the function executes
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        // way 1:
        // people.push(People({name: _name, favoriteNumber: _favoriteNumber}));
        // way 2:
        people.push(People( _favoriteNumber, _name));
        
        // the key is the name and the value the favorite number
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
```

result:

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0643b11d-6d35-4173-9819-abc347e9b49b/Untitled.png)

## Testing in a account

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/8ad6ea28-c962-4e11-a80e-8d50e836ebcb/Untitled.png)

1 - Choose the Injected Web3, 

it will appear a popup asking for connect to our MetaMask account

2 - select the account connected to the ganache

3 - deploy a contract

it will cost a fee

  

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/dcc483e1-4c07-4f7b-9cd9-e4a3a1e8a7e1/Untitled.png)

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5781879d-9307-4800-9fba-8e72a15dcc9e/Untitled.png)

if we run this in a dev blockchain like kovan network or rinkeby it will show a link ro redirect to this contract in etherscan

Functions that read a state does not cost anythin but one that changes the state we need to pay a fee

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/36537bf5-1f0e-4824-af61-d62036a26563/Untitled.png)

## Storage Factory

```jsx
// SPDX-License_Identifier: MIT

pragma solidity ^0.6.0;

import "./SimpleStorage.sol"; // import the SimpleStorage code

contract StorageFactory {
    
    SimpleStorage[] public simpleStorageArray;
    
    function createSimpleStorageContract() public {
        // create a obj of type SimpleStorage class
        SimpleStorage simpleStorage = new SimpleStorage();
        
        simpleStorageArray.push(simpleStorage);
    }
    
}
```

we import a solidy contract and now we can create multiple instances with this factory,

ex:

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f3eefec0-011b-4ef8-9dd3-ce2138e59544/Untitled.png)

the address generated is the generated address contract

Accessing generated contracts data:

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/58f92f04-fac7-4a64-8d75-d64f1265a20a/Untitled.png)