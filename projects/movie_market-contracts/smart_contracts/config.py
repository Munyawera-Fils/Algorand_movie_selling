import importlib
from collections.abc import Callable
from pathlib import Path

from algokit_utils import Account, ApplicationSpecification
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from beaker import Application

# Import SmartContract class
from .movie_market.contract import SmartContract


def import_contract(folder: Path) -> Application:
    """Imports the contract from a folder if it exists."""
    try:
        contract_module = importlib.import_module(
            f"smart_contracts.{folder.name}.contract"
        )
        return contract_module.app
    except ImportError as e:
        raise Exception(f"Contract not found in {folder}") from e

def import_deploy_if_exists(
    folder: Path,
) -> (
    Callable[[AlgodClient, IndexerClient, ApplicationSpecification, Account], None]
    | None
):
    """Imports the deploy function from a folder if it exists."""
    try:
        deploy_module = importlib.import_module(
            f"smart_contracts.{folder.name}.deploy_config"
        )
        return deploy_module.deploy
    except ImportError:
        return None

def has_contract_file(directory: Path) -> bool:
    """Checks whether the directory contains contract.py file."""
    return (directory / "contract.py").exists()

# define contracts to build and/or deploy
base_dir = Path("smart_contracts")
contracts = [
    SmartContract(app=import_contract(folder), deploy=import_deploy_if_exists(folder))
    for folder in base_dir.iterdir()
    if folder.is_dir() and has_contract_file(folder)
]
