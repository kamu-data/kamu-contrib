# net.rocketpool

## Local hacking

Prepare:
```shell
nvm use # if you use nvm to manage Node versions
npm install
```

Test start:
```shell
ETH_NODE_PROVIDER_URL=<INSERT_YOUR_VALUE> make test 
```

Regenerate contracts' code from ABIs (if changed):
```shell
npm run codegen-contracts 
```

## Image-related stuff

Build an image:
```shell
make image
```

Push the image:
```shell
make image-push
```
