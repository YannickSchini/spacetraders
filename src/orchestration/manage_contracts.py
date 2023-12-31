from typing import List

from src.domain.agent import AgentRepository, Contract, ContractRepository
from src.logging import configure_logger
from src.repositories.agent import HttpAndFileAgentRepository
from src.repositories.contract import HttpContractRepository


def get_contracts(
        agent_repo: AgentRepository,
        contracts_repo: ContractRepository,
    ) -> List[Contract]:
    agent = agent_repo.get_agent()
    return agent.get_contracts(contracts_repo)

def accept_contract(
        agent_repo: AgentRepository,
        contracts_repo: ContractRepository,
        contract_id: str,
    ) -> None:
    agent = agent_repo.get_agent()
    return agent.accept_contract(
        contract_id=contract_id,
        contract_repository=contracts_repo
    )



if __name__ == "__main__":
    configure_logger()
    agent_repo = HttpAndFileAgentRepository()
    contracts_repo = HttpContractRepository()
    contracts = get_contracts(agent_repo, contracts_repo)
    print(contracts)
    accept_contract(agent_repo, contracts_repo, contracts[0].contract_id)
