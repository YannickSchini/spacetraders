from src.repositories.agent import InMemoryAgentRepository
from src.repositories.contract import create_in_memory_contract_repo


def test_get_contracts_returns_contracts() -> None:
    agent_repo = InMemoryAgentRepository.create_agent_repo()
    contracts_repo = create_in_memory_contract_repo()
    contracts_repo.append_contract_to_repo(
        contract_id="DUMMY_CONTRACT_2",
        merchandise="GOLD",
        destination="HERE",
        units_required=105,
        units_fulfilled=5,
    )
    agent = agent_repo.get_agent()
    first_contract_from_repo = agent.get_contracts(contracts_repo)[0]
    second_contract_from_repo = agent.get_contracts(contracts_repo)[1]

    assert len(agent.get_contracts(contracts_repo)) == 2

    assert first_contract_from_repo.contract_id == "DUMMY_CONTRACT_1"
    assert first_contract_from_repo.delivery_details[0].merchandise == "ROCK"
    assert first_contract_from_repo.delivery_details[0].destination.waypoint == "THERE"
    assert first_contract_from_repo.delivery_details[0].units_required == 100
    assert first_contract_from_repo.delivery_details[0].units_fulfilled == 0

    assert second_contract_from_repo.contract_id == "DUMMY_CONTRACT_2"
    assert second_contract_from_repo.delivery_details[0].merchandise == "GOLD"
    assert second_contract_from_repo.delivery_details[0].destination.waypoint == "HERE"
    assert second_contract_from_repo.delivery_details[0].units_required == 105
    assert second_contract_from_repo.delivery_details[0].units_fulfilled == 5


def test_accept_contract() -> None:
    agent_repo = InMemoryAgentRepository.create_agent_repo()
    contracts_repo = create_in_memory_contract_repo()
    agent = agent_repo.get_agent()
    contracts = agent.get_contracts(contracts_repo)

    agent.accept_contract(contracts[0].contract_id, contracts_repo)

