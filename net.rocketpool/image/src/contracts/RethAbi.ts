/* Autogenerated file. Do not edit manually. */
/* tslint:disable */
/* eslint-disable */
import type {
  BaseContract,
  BigNumber,
  BigNumberish,
  BytesLike,
  CallOverrides,
  ContractTransaction,
  Overrides,
  PayableOverrides,
  PopulatedTransaction,
  Signer,
  utils,
} from "ethers";
import type {
  FunctionFragment,
  Result,
  EventFragment,
} from "@ethersproject/abi";
import type { Listener, Provider } from "@ethersproject/providers";
import type {
  TypedEventFilter,
  TypedEvent,
  TypedListener,
  OnEvent,
} from "./common";

export interface RethAbiInterface extends utils.Interface {
  functions: {
    "allowance(address,address)": FunctionFragment;
    "approve(address,uint256)": FunctionFragment;
    "balanceOf(address)": FunctionFragment;
    "burn(uint256)": FunctionFragment;
    "decimals()": FunctionFragment;
    "decreaseAllowance(address,uint256)": FunctionFragment;
    "depositExcess()": FunctionFragment;
    "depositExcessCollateral()": FunctionFragment;
    "getCollateralRate()": FunctionFragment;
    "getEthValue(uint256)": FunctionFragment;
    "getExchangeRate()": FunctionFragment;
    "getRethValue(uint256)": FunctionFragment;
    "getTotalCollateral()": FunctionFragment;
    "increaseAllowance(address,uint256)": FunctionFragment;
    "mint(uint256,address)": FunctionFragment;
    "name()": FunctionFragment;
    "symbol()": FunctionFragment;
    "totalSupply()": FunctionFragment;
    "transfer(address,uint256)": FunctionFragment;
    "transferFrom(address,address,uint256)": FunctionFragment;
    "version()": FunctionFragment;
  };

  getFunction(
    nameOrSignatureOrTopic:
      | "allowance"
      | "approve"
      | "balanceOf"
      | "burn"
      | "decimals"
      | "decreaseAllowance"
      | "depositExcess"
      | "depositExcessCollateral"
      | "getCollateralRate"
      | "getEthValue"
      | "getExchangeRate"
      | "getRethValue"
      | "getTotalCollateral"
      | "increaseAllowance"
      | "mint"
      | "name"
      | "symbol"
      | "totalSupply"
      | "transfer"
      | "transferFrom"
      | "version"
  ): FunctionFragment;

  encodeFunctionData(
    functionFragment: "allowance",
    values: [string, string]
  ): string;
  encodeFunctionData(
    functionFragment: "approve",
    values: [string, BigNumberish]
  ): string;
  encodeFunctionData(functionFragment: "balanceOf", values: [string]): string;
  encodeFunctionData(functionFragment: "burn", values: [BigNumberish]): string;
  encodeFunctionData(functionFragment: "decimals", values?: undefined): string;
  encodeFunctionData(
    functionFragment: "decreaseAllowance",
    values: [string, BigNumberish]
  ): string;
  encodeFunctionData(
    functionFragment: "depositExcess",
    values?: undefined
  ): string;
  encodeFunctionData(
    functionFragment: "depositExcessCollateral",
    values?: undefined
  ): string;
  encodeFunctionData(
    functionFragment: "getCollateralRate",
    values?: undefined
  ): string;
  encodeFunctionData(
    functionFragment: "getEthValue",
    values: [BigNumberish]
  ): string;
  encodeFunctionData(
    functionFragment: "getExchangeRate",
    values?: undefined
  ): string;
  encodeFunctionData(
    functionFragment: "getRethValue",
    values: [BigNumberish]
  ): string;
  encodeFunctionData(
    functionFragment: "getTotalCollateral",
    values?: undefined
  ): string;
  encodeFunctionData(
    functionFragment: "increaseAllowance",
    values: [string, BigNumberish]
  ): string;
  encodeFunctionData(
    functionFragment: "mint",
    values: [BigNumberish, string]
  ): string;
  encodeFunctionData(functionFragment: "name", values?: undefined): string;
  encodeFunctionData(functionFragment: "symbol", values?: undefined): string;
  encodeFunctionData(
    functionFragment: "totalSupply",
    values?: undefined
  ): string;
  encodeFunctionData(
    functionFragment: "transfer",
    values: [string, BigNumberish]
  ): string;
  encodeFunctionData(
    functionFragment: "transferFrom",
    values: [string, string, BigNumberish]
  ): string;
  encodeFunctionData(functionFragment: "version", values?: undefined): string;

  decodeFunctionResult(functionFragment: "allowance", data: BytesLike): Result;
  decodeFunctionResult(functionFragment: "approve", data: BytesLike): Result;
  decodeFunctionResult(functionFragment: "balanceOf", data: BytesLike): Result;
  decodeFunctionResult(functionFragment: "burn", data: BytesLike): Result;
  decodeFunctionResult(functionFragment: "decimals", data: BytesLike): Result;
  decodeFunctionResult(
    functionFragment: "decreaseAllowance",
    data: BytesLike
  ): Result;
  decodeFunctionResult(
    functionFragment: "depositExcess",
    data: BytesLike
  ): Result;
  decodeFunctionResult(
    functionFragment: "depositExcessCollateral",
    data: BytesLike
  ): Result;
  decodeFunctionResult(
    functionFragment: "getCollateralRate",
    data: BytesLike
  ): Result;
  decodeFunctionResult(
    functionFragment: "getEthValue",
    data: BytesLike
  ): Result;
  decodeFunctionResult(
    functionFragment: "getExchangeRate",
    data: BytesLike
  ): Result;
  decodeFunctionResult(
    functionFragment: "getRethValue",
    data: BytesLike
  ): Result;
  decodeFunctionResult(
    functionFragment: "getTotalCollateral",
    data: BytesLike
  ): Result;
  decodeFunctionResult(
    functionFragment: "increaseAllowance",
    data: BytesLike
  ): Result;
  decodeFunctionResult(functionFragment: "mint", data: BytesLike): Result;
  decodeFunctionResult(functionFragment: "name", data: BytesLike): Result;
  decodeFunctionResult(functionFragment: "symbol", data: BytesLike): Result;
  decodeFunctionResult(
    functionFragment: "totalSupply",
    data: BytesLike
  ): Result;
  decodeFunctionResult(functionFragment: "transfer", data: BytesLike): Result;
  decodeFunctionResult(
    functionFragment: "transferFrom",
    data: BytesLike
  ): Result;
  decodeFunctionResult(functionFragment: "version", data: BytesLike): Result;

  events: {
    "Approval(address,address,uint256)": EventFragment;
    "EtherDeposited(address,uint256,uint256)": EventFragment;
    "TokensBurned(address,uint256,uint256,uint256)": EventFragment;
    "TokensMinted(address,uint256,uint256,uint256)": EventFragment;
    "Transfer(address,address,uint256)": EventFragment;
  };

  getEvent(nameOrSignatureOrTopic: "Approval"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "EtherDeposited"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "TokensBurned"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "TokensMinted"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "Transfer"): EventFragment;
}

export interface ApprovalEventObject {
  owner: string;
  spender: string;
  value: BigNumber;
}
export type ApprovalEvent = TypedEvent<
  [string, string, BigNumber],
  ApprovalEventObject
>;

export type ApprovalEventFilter = TypedEventFilter<ApprovalEvent>;

export interface EtherDepositedEventObject {
  from: string;
  amount: BigNumber;
  time: BigNumber;
}
export type EtherDepositedEvent = TypedEvent<
  [string, BigNumber, BigNumber],
  EtherDepositedEventObject
>;

export type EtherDepositedEventFilter = TypedEventFilter<EtherDepositedEvent>;

export interface TokensBurnedEventObject {
  from: string;
  amount: BigNumber;
  ethAmount: BigNumber;
  time: BigNumber;
}
export type TokensBurnedEvent = TypedEvent<
  [string, BigNumber, BigNumber, BigNumber],
  TokensBurnedEventObject
>;

export type TokensBurnedEventFilter = TypedEventFilter<TokensBurnedEvent>;

export interface TokensMintedEventObject {
  to: string;
  amount: BigNumber;
  ethAmount: BigNumber;
  time: BigNumber;
}
export type TokensMintedEvent = TypedEvent<
  [string, BigNumber, BigNumber, BigNumber],
  TokensMintedEventObject
>;

export type TokensMintedEventFilter = TypedEventFilter<TokensMintedEvent>;

export interface TransferEventObject {
  from: string;
  to: string;
  value: BigNumber;
}
export type TransferEvent = TypedEvent<
  [string, string, BigNumber],
  TransferEventObject
>;

export type TransferEventFilter = TypedEventFilter<TransferEvent>;

export interface RethAbi extends BaseContract {
  connect(signerOrProvider: Signer | Provider | string): this;
  attach(addressOrName: string): this;
  deployed(): Promise<this>;

  interface: RethAbiInterface;

  queryFilter<TEvent extends TypedEvent>(
    event: TypedEventFilter<TEvent>,
    fromBlockOrBlockhash?: string | number | undefined,
    toBlock?: string | number | undefined
  ): Promise<Array<TEvent>>;

  listeners<TEvent extends TypedEvent>(
    eventFilter?: TypedEventFilter<TEvent>
  ): Array<TypedListener<TEvent>>;
  listeners(eventName?: string): Array<Listener>;
  removeAllListeners<TEvent extends TypedEvent>(
    eventFilter: TypedEventFilter<TEvent>
  ): this;
  removeAllListeners(eventName?: string): this;
  off: OnEvent<this>;
  on: OnEvent<this>;
  once: OnEvent<this>;
  removeListener: OnEvent<this>;

  functions: {
    allowance(
      owner: string,
      spender: string,
      overrides?: CallOverrides
    ): Promise<[BigNumber]>;

    approve(
      spender: string,
      amount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<ContractTransaction>;

    balanceOf(account: string, overrides?: CallOverrides): Promise<[BigNumber]>;

    burn(
      _rethAmount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<ContractTransaction>;

    decimals(overrides?: CallOverrides): Promise<[number]>;

    decreaseAllowance(
      spender: string,
      subtractedValue: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<ContractTransaction>;

    depositExcess(
      overrides?: PayableOverrides & { from?: string }
    ): Promise<ContractTransaction>;

    depositExcessCollateral(
      overrides?: Overrides & { from?: string }
    ): Promise<ContractTransaction>;

    getCollateralRate(overrides?: CallOverrides): Promise<[BigNumber]>;

    getEthValue(
      _rethAmount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<[BigNumber]>;

    getExchangeRate(overrides?: CallOverrides): Promise<[BigNumber]>;

    getRethValue(
      _ethAmount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<[BigNumber]>;

    getTotalCollateral(overrides?: CallOverrides): Promise<[BigNumber]>;

    increaseAllowance(
      spender: string,
      addedValue: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<ContractTransaction>;

    mint(
      _ethAmount: BigNumberish,
      _to: string,
      overrides?: Overrides & { from?: string }
    ): Promise<ContractTransaction>;

    name(overrides?: CallOverrides): Promise<[string]>;

    symbol(overrides?: CallOverrides): Promise<[string]>;

    totalSupply(overrides?: CallOverrides): Promise<[BigNumber]>;

    transfer(
      recipient: string,
      amount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<ContractTransaction>;

    transferFrom(
      sender: string,
      recipient: string,
      amount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<ContractTransaction>;

    version(overrides?: CallOverrides): Promise<[number]>;
  };

  allowance(
    owner: string,
    spender: string,
    overrides?: CallOverrides
  ): Promise<BigNumber>;

  approve(
    spender: string,
    amount: BigNumberish,
    overrides?: Overrides & { from?: string }
  ): Promise<ContractTransaction>;

  balanceOf(account: string, overrides?: CallOverrides): Promise<BigNumber>;

  burn(
    _rethAmount: BigNumberish,
    overrides?: Overrides & { from?: string }
  ): Promise<ContractTransaction>;

  decimals(overrides?: CallOverrides): Promise<number>;

  decreaseAllowance(
    spender: string,
    subtractedValue: BigNumberish,
    overrides?: Overrides & { from?: string }
  ): Promise<ContractTransaction>;

  depositExcess(
    overrides?: PayableOverrides & { from?: string }
  ): Promise<ContractTransaction>;

  depositExcessCollateral(
    overrides?: Overrides & { from?: string }
  ): Promise<ContractTransaction>;

  getCollateralRate(overrides?: CallOverrides): Promise<BigNumber>;

  getEthValue(
    _rethAmount: BigNumberish,
    overrides?: CallOverrides
  ): Promise<BigNumber>;

  getExchangeRate(overrides?: CallOverrides): Promise<BigNumber>;

  getRethValue(
    _ethAmount: BigNumberish,
    overrides?: CallOverrides
  ): Promise<BigNumber>;

  getTotalCollateral(overrides?: CallOverrides): Promise<BigNumber>;

  increaseAllowance(
    spender: string,
    addedValue: BigNumberish,
    overrides?: Overrides & { from?: string }
  ): Promise<ContractTransaction>;

  mint(
    _ethAmount: BigNumberish,
    _to: string,
    overrides?: Overrides & { from?: string }
  ): Promise<ContractTransaction>;

  name(overrides?: CallOverrides): Promise<string>;

  symbol(overrides?: CallOverrides): Promise<string>;

  totalSupply(overrides?: CallOverrides): Promise<BigNumber>;

  transfer(
    recipient: string,
    amount: BigNumberish,
    overrides?: Overrides & { from?: string }
  ): Promise<ContractTransaction>;

  transferFrom(
    sender: string,
    recipient: string,
    amount: BigNumberish,
    overrides?: Overrides & { from?: string }
  ): Promise<ContractTransaction>;

  version(overrides?: CallOverrides): Promise<number>;

  callStatic: {
    allowance(
      owner: string,
      spender: string,
      overrides?: CallOverrides
    ): Promise<BigNumber>;

    approve(
      spender: string,
      amount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<boolean>;

    balanceOf(account: string, overrides?: CallOverrides): Promise<BigNumber>;

    burn(_rethAmount: BigNumberish, overrides?: CallOverrides): Promise<void>;

    decimals(overrides?: CallOverrides): Promise<number>;

    decreaseAllowance(
      spender: string,
      subtractedValue: BigNumberish,
      overrides?: CallOverrides
    ): Promise<boolean>;

    depositExcess(overrides?: CallOverrides): Promise<void>;

    depositExcessCollateral(overrides?: CallOverrides): Promise<void>;

    getCollateralRate(overrides?: CallOverrides): Promise<BigNumber>;

    getEthValue(
      _rethAmount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<BigNumber>;

    getExchangeRate(overrides?: CallOverrides): Promise<BigNumber>;

    getRethValue(
      _ethAmount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<BigNumber>;

    getTotalCollateral(overrides?: CallOverrides): Promise<BigNumber>;

    increaseAllowance(
      spender: string,
      addedValue: BigNumberish,
      overrides?: CallOverrides
    ): Promise<boolean>;

    mint(
      _ethAmount: BigNumberish,
      _to: string,
      overrides?: CallOverrides
    ): Promise<void>;

    name(overrides?: CallOverrides): Promise<string>;

    symbol(overrides?: CallOverrides): Promise<string>;

    totalSupply(overrides?: CallOverrides): Promise<BigNumber>;

    transfer(
      recipient: string,
      amount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<boolean>;

    transferFrom(
      sender: string,
      recipient: string,
      amount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<boolean>;

    version(overrides?: CallOverrides): Promise<number>;
  };

  filters: {
    "Approval(address,address,uint256)"(
      owner?: string | null,
      spender?: string | null,
      value?: null
    ): ApprovalEventFilter;
    Approval(
      owner?: string | null,
      spender?: string | null,
      value?: null
    ): ApprovalEventFilter;

    "EtherDeposited(address,uint256,uint256)"(
      from?: string | null,
      amount?: null,
      time?: null
    ): EtherDepositedEventFilter;
    EtherDeposited(
      from?: string | null,
      amount?: null,
      time?: null
    ): EtherDepositedEventFilter;

    "TokensBurned(address,uint256,uint256,uint256)"(
      from?: string | null,
      amount?: null,
      ethAmount?: null,
      time?: null
    ): TokensBurnedEventFilter;
    TokensBurned(
      from?: string | null,
      amount?: null,
      ethAmount?: null,
      time?: null
    ): TokensBurnedEventFilter;

    "TokensMinted(address,uint256,uint256,uint256)"(
      to?: string | null,
      amount?: null,
      ethAmount?: null,
      time?: null
    ): TokensMintedEventFilter;
    TokensMinted(
      to?: string | null,
      amount?: null,
      ethAmount?: null,
      time?: null
    ): TokensMintedEventFilter;

    "Transfer(address,address,uint256)"(
      from?: string | null,
      to?: string | null,
      value?: null
    ): TransferEventFilter;
    Transfer(
      from?: string | null,
      to?: string | null,
      value?: null
    ): TransferEventFilter;
  };

  estimateGas: {
    allowance(
      owner: string,
      spender: string,
      overrides?: CallOverrides
    ): Promise<BigNumber>;

    approve(
      spender: string,
      amount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<BigNumber>;

    balanceOf(account: string, overrides?: CallOverrides): Promise<BigNumber>;

    burn(
      _rethAmount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<BigNumber>;

    decimals(overrides?: CallOverrides): Promise<BigNumber>;

    decreaseAllowance(
      spender: string,
      subtractedValue: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<BigNumber>;

    depositExcess(
      overrides?: PayableOverrides & { from?: string }
    ): Promise<BigNumber>;

    depositExcessCollateral(
      overrides?: Overrides & { from?: string }
    ): Promise<BigNumber>;

    getCollateralRate(overrides?: CallOverrides): Promise<BigNumber>;

    getEthValue(
      _rethAmount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<BigNumber>;

    getExchangeRate(overrides?: CallOverrides): Promise<BigNumber>;

    getRethValue(
      _ethAmount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<BigNumber>;

    getTotalCollateral(overrides?: CallOverrides): Promise<BigNumber>;

    increaseAllowance(
      spender: string,
      addedValue: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<BigNumber>;

    mint(
      _ethAmount: BigNumberish,
      _to: string,
      overrides?: Overrides & { from?: string }
    ): Promise<BigNumber>;

    name(overrides?: CallOverrides): Promise<BigNumber>;

    symbol(overrides?: CallOverrides): Promise<BigNumber>;

    totalSupply(overrides?: CallOverrides): Promise<BigNumber>;

    transfer(
      recipient: string,
      amount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<BigNumber>;

    transferFrom(
      sender: string,
      recipient: string,
      amount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<BigNumber>;

    version(overrides?: CallOverrides): Promise<BigNumber>;
  };

  populateTransaction: {
    allowance(
      owner: string,
      spender: string,
      overrides?: CallOverrides
    ): Promise<PopulatedTransaction>;

    approve(
      spender: string,
      amount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<PopulatedTransaction>;

    balanceOf(
      account: string,
      overrides?: CallOverrides
    ): Promise<PopulatedTransaction>;

    burn(
      _rethAmount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<PopulatedTransaction>;

    decimals(overrides?: CallOverrides): Promise<PopulatedTransaction>;

    decreaseAllowance(
      spender: string,
      subtractedValue: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<PopulatedTransaction>;

    depositExcess(
      overrides?: PayableOverrides & { from?: string }
    ): Promise<PopulatedTransaction>;

    depositExcessCollateral(
      overrides?: Overrides & { from?: string }
    ): Promise<PopulatedTransaction>;

    getCollateralRate(overrides?: CallOverrides): Promise<PopulatedTransaction>;

    getEthValue(
      _rethAmount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<PopulatedTransaction>;

    getExchangeRate(overrides?: CallOverrides): Promise<PopulatedTransaction>;

    getRethValue(
      _ethAmount: BigNumberish,
      overrides?: CallOverrides
    ): Promise<PopulatedTransaction>;

    getTotalCollateral(
      overrides?: CallOverrides
    ): Promise<PopulatedTransaction>;

    increaseAllowance(
      spender: string,
      addedValue: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<PopulatedTransaction>;

    mint(
      _ethAmount: BigNumberish,
      _to: string,
      overrides?: Overrides & { from?: string }
    ): Promise<PopulatedTransaction>;

    name(overrides?: CallOverrides): Promise<PopulatedTransaction>;

    symbol(overrides?: CallOverrides): Promise<PopulatedTransaction>;

    totalSupply(overrides?: CallOverrides): Promise<PopulatedTransaction>;

    transfer(
      recipient: string,
      amount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<PopulatedTransaction>;

    transferFrom(
      sender: string,
      recipient: string,
      amount: BigNumberish,
      overrides?: Overrides & { from?: string }
    ): Promise<PopulatedTransaction>;

    version(overrides?: CallOverrides): Promise<PopulatedTransaction>;
  };
}
