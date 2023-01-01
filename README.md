# Cherry Lambdas (Serverless Backend)
These lambda functions define the backend logic for Cherry, a Bitcoin block explorer. The frontend repo (as well as a more comprehensive description of the project) can be found [here](https://github.com/tigeryant/cherry-fe).
## Functions
* `get_block` - returns data regarding a specific block
* `get_address_info` - returns data regarding a specific address
* `get_raw_transaction` - returns data regarding a specific transaction

## Stack
### AWS
* Lambda
* API Gateway
### CI/CD
* Serverless Framework
* GitHub Actions
### Languages
* Python 3.7
