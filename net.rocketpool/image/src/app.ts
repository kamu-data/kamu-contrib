import fs from "fs";
import { Console } from "console";

import Web3 from "web3";
import abiDecoder from "abi-decoder";

const console = new Console(process.stderr);

/////////////////////////////////////////////////////////////////////////////////////////

interface Event {
  eventName: "TokensMinted" | "TokensBurned";
  amount: string;
  ethAmount: string;
  blockNumber: number;
  blockHash: string;
  blockTime: number;
  transactionIndex: number;
  transactionHash: string;
  logIndex: number;
}

/////////////////////////////////////////////////////////////////////////////////////////

async function readEventsFromETH(
  startBlock: number,
  endBlock: number,
  clb: (_: Event) => boolean,
  blockBatchSize: number
): Promise<void> {
  console.log(
    "Considering events in block range [%s, %s] (%s blocks)",
    startBlock,
    endBlock,
    endBlock - startBlock
  );

  let fromBlock = startBlock;
  let toBlock = fromBlock;

  do {
    fromBlock = toBlock + 1;
    toBlock = Math.min(endBlock, fromBlock + blockBatchSize);

    console.log("Syncing block range [%s, %s]", fromBlock, toBlock);

    await readEventsFromETHRangeWithFallback(fromBlock, toBlock, clb);
  } while (toBlock != endBlock);
}

/////////////////////////////////////////////////////////////////////////////////////////

async function readEventsFromETHRangeWithFallback(
  fromBlock: number,
  toBlock: number,
  clb: (_: Event) => boolean
): Promise<void> {
  try {
    const logs = await web3.eth.getPastLogs({
      fromBlock,
      toBlock,
      address: rethAddress,
    });
    const logsDecoded = abiDecoder.decodeLogs(logs);

    for (let i = 0; i != logsDecoded.length; i++) {
      const logDecoded = logsDecoded[i];
      const logRaw = logs[i];

      if (!["TokensMinted", "TokensBurned"].includes(logDecoded.name)) {
        continue;
      }

      const event = {
        eventName: logDecoded.name,
        amount: logDecoded.events.find((i) => i.name == "amount").value,
        ethAmount: logDecoded.events.find((i) => i.name == "ethAmount").value,
        blockNumber: logRaw.blockNumber,
        blockHash: logRaw.blockHash,
        blockTime: Number(
          logDecoded.events.find((i) => i.name == "time").value
        ),
        transactionIndex: logRaw.transactionIndex,
        transactionHash: logRaw.transactionHash,
        logIndex: logRaw.logIndex,
      };

      if (!clb(event)) {
        return;
      }
    }
  } catch (err) {
    // TODO: Is this too Infura-specific?
    if (err.message.includes("query returned more than")) {
      const middle = Math.round((fromBlock + toBlock) / 2);

      console.log(
        "Hit API limit, splitting interval to [%s, %s] and [%s, %s]",
        fromBlock,
        middle,
        middle + 1,
        toBlock
      );

      await readEventsFromETHRangeWithFallback(fromBlock, middle, clb);
      await readEventsFromETHRangeWithFallback(middle + 1, toBlock, clb);
    } else {
      throw err;
    }
  }
}

/////////////////////////////////////////////////////////////////////////////////////////

// See: https://etherscan.io/token/0xae78736cd615f374d3085123a210448e74fc6393
const rethAddress = "0xae78736cd615f374d3085123a210448e74fc6393";
const rethStartBlock = 13325304;

// ABI
const rethAbi = JSON.parse(fs.readFileSync("./abi/reth.abi.json", "utf8"));
abiDecoder.addABI(rethAbi);

// Init
const providerUrl = process.env.ETH_NODE_PROVIDER_URL;

console.log("ETH node provider URL: %s", providerUrl);

const web3 = new Web3(
  new Web3.providers.WebsocketProvider(providerUrl, {
    clientConfig: {
      maxReceivedFrameSize: 10000000,
      maxReceivedMessageSize: 10000000,
    },
  })
);

// Block range
const etag = process.env.ODF_ETAG;
const newEtagPath = process.env.ODF_NEW_ETAG_PATH;

const lastSeenBlock = etag.length != 0 ? Number(etag) : 0;
console.log("Last seen block: %s", lastSeenBlock);

const ethHeadBlock = await web3.eth.getBlockNumber();
console.log("Current chain head block: %s", ethHeadBlock);

const blockBatchSize = Number(process.env.ODF_BATCH_SIZE);

await readEventsFromETH(
  Math.max(lastSeenBlock + 1, rethStartBlock),
  ethHeadBlock,
  function (event) {
    process.stdout.write(JSON.stringify(event));
    process.stdout.write("\n");
    return true;
  },
  blockBatchSize
);

// Save last seen block
fs.writeFileSync(newEtagPath, ethHeadBlock.toString());
process.exit(0);
