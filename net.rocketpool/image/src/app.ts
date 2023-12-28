import fs from "fs";
import { Console } from "console";

import { ethers } from "ethers"
import { cleanEnv, url, str, num } from "envalid";

import { RethAbi__factory } from "./contracts/factories/RethAbi__factory";
import type { RethAbi } from "./contracts";

const console = new Console(process.stderr);

/////////////////////////////////////////////////////////////////////////////////////////

interface EventRow {
  eventName: "TokensMinted" | "TokensBurned";
  amount: string;
  ethAmount: string;
  blockNumber: number;
  blockHash: string;
  eventTime: number;
  transactionIndex: number;
  transactionHash: string;
  logIndex: number;
}

interface OdfReadRowsResult {
  etag: number;
  hasMore: boolean;
}

type Provider = ethers.providers.JsonRpcProvider | ethers.providers.WebSocketProvider;
type OnEventCallback = (_: EventRow) => Promise<boolean>;
type AllBlockRangeHasProcessed = boolean;

/////////////////////////////////////////////////////////////////////////////////////////

async function main() {
  const env = cleanEnv(process.env, {
    // Application:
    ETH_NODE_PROVIDER_URL: url(),
    BLOCK_BATCH_SIZE: num(),
    // ODF interface:
    ODF_BATCH_SIZE: num(),
    ODF_ETAG: num({ default: 0 }),
    ODF_NEW_ETAG_PATH: str(),
    ODF_NEW_HAS_MORE_DATA_PATH: str(),
  })

  // See: https://etherscan.io/token/0xae78736cd615f374d3085123a210448e74fc6393
  //      https://etherscan.io/address/0xae78736cd615f374d3085123a210448e74fc6393
  const rethAddress = "0xae78736cd615f374d3085123a210448e74fc6393";
  const rethStartBlock = 13325304;

  // Init
  const providerUrl = env.ETH_NODE_PROVIDER_URL;

  console.log(`ETH node provider URL: ${providerUrl}`);

  const provider = getProvider(providerUrl)
  const rethContract = RethAbi__factory.connect(rethAddress, provider)

  // Block range
  const lastSeenBlock = env.ODF_ETAG;

  console.log(`Last seen block: ${lastSeenBlock}`);

  const ethHeadBlock = await provider.getBlockNumber();

  console.log(`Current chain head block: ${ethHeadBlock}`);

  const startBlock = Math.max(lastSeenBlock + 1, rethStartBlock);
  const endBlock = ethHeadBlock;
  const {
    etag,
    hasMore,
  } = await odfReadRows(rethContract, startBlock, endBlock, env.BLOCK_BATCH_SIZE, env.ODF_BATCH_SIZE);

  // Notify `kamu-cli` regarding new state
  fs.writeFileSync(env.ODF_NEW_ETAG_PATH, etag.toString());

  if (hasMore) {
    fs.writeFileSync(env.ODF_NEW_HAS_MORE_DATA_PATH, "");
  }
}

/////////////////////////////////////////////////////////////////////////////////////////

async function odfReadRows(
  rethContract: RethAbi,
  startBlock: number,
  endBlock: number,
  blockBatchSize: number,
  odfBatchSize: number,
): Promise<OdfReadRowsResult> {
  let outputRowsCount = 0;
  let lastOutputBlockNumber = 0;

  const allBlockRangeHasProcessed = await readRethContractEvents(
    rethContract,
    startBlock,
    endBlock,
    async function (eventRow) {
      if (outputRowsCount >= odfBatchSize) {
        return false;
      }

      outputRowsCount++;
      lastOutputBlockNumber = eventRow.blockNumber;

      await stdOutWrite(`${JSON.stringify(eventRow)}\n`);

      return true;
    },
    blockBatchSize,
  );

  const etag = allBlockRangeHasProcessed ? endBlock : lastOutputBlockNumber;
  const hasMore = !allBlockRangeHasProcessed;

  return {
    etag,
    hasMore
  };
}

/////////////////////////////////////////////////////////////////////////////////////////

async function readRethContractEvents(
  rethContract: RethAbi,
  startBlock: number,
  endBlock: number,
  onEventCallback: OnEventCallback,
  blockBatchSize: number
): Promise<AllBlockRangeHasProcessed> {
  const blocksDelta = endBlock - startBlock;

  console.log(`Considering events in block range [${startBlock}, ${endBlock}] (${blocksDelta} blocks)`);

  let fromBlock = startBlock;
  let toBlock = fromBlock;

  do {
    fromBlock = toBlock + 1;
    toBlock = Math.min(endBlock, fromBlock + blockBatchSize);

    console.log(`Syncing block range [${fromBlock}, ${toBlock}]`);

    const stopProcessing = !await readRethContractEventsBatch(
      rethContract, fromBlock, toBlock, onEventCallback
    );

    if (stopProcessing) {
      return false;
    }
  } while (toBlock !== endBlock);

  return true;
}

/////////////////////////////////////////////////////////////////////////////////////////

async function readRethContractEventsBatch(
  rethContract: RethAbi,
  fromBlock: number,
  toBlock: number,
  onEventCallback: OnEventCallback
): Promise<AllBlockRangeHasProcessed> {
  const eventFilters = [
    rethContract.filters.TokensMinted(),
    rethContract.filters.TokensBurned()
  ] as const;
  const eventsRowsPromises = eventFilters.map(async (eventFilter) => {
    const events = await rethContract.queryFilter(eventFilter, fromBlock, toBlock);

    return events.map((event) => {
      return {
        eventName: event.event,
        amount: event.args.amount.toString(),
        ethAmount: event.args.ethAmount.toString(),
        blockNumber: event.blockNumber,
        blockHash: event.blockHash,
        eventTime: event.args.time.toNumber(),
        transactionIndex: event.transactionIndex,
        transactionHash: event.transactionHash,
        logIndex: event.logIndex,
      } as EventRow;
    });
  });
  const eventRows = (await Promise.all(eventsRowsPromises)).flat();

  eventRows.sort((right, left) => right.eventTime - left.eventTime);

  for (const eventRow of eventRows) {
    if (!await onEventCallback(eventRow)) {
      return false;
    }
  }

  return true;
}

/////////////////////////////////////////////////////////////////////////////////////////

function getProvider(url: string): Provider {
  const { protocol } = new URL(url);
  const isWebSocketSchema = /wss?:/.test(protocol);

  if (isWebSocketSchema) {
    return new ethers.providers.WebSocketProvider(url);
  } else {
    return new ethers.providers.JsonRpcProvider(url);
  }
}

/////////////////////////////////////////////////////////////////////////////////////////

async function stdOutWrite(data: Uint8Array | string): Promise<void> {
  // https://nodejs.org/docs/latest-v20.x/api/stream.html#writablewritechunk-encoding-callback
  return new Promise((resolve) => {
    const hasDrained = process.stdout.write(data);

    if (hasDrained) {
      resolve();
    } else {
      process.stdout.once('drain', function(){
        resolve();
      });
    }
  })
}

/////////////////////////////////////////////////////////////////////////////////////////

main().then(() => {
  process.exit(0)
}).catch((e) => {
  console.error(e);

  process.exit(1)
});
