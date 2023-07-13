from typing import List

from src.domain.model import AgentRepository, Contract, ContractRepository
from src.repositories.agent import HttpAndFileAgentRepository
from src.repositories.contract import HttpContractRepository


def get_contracts(
        agent_repo: AgentRepository,
        contracts_repo: ContractRepository
    ) -> List[Contract]:
    agent = agent_repo.get_agent()
    return agent.get_contracts(contracts_repo)


if __name__ == "__main__":
    agent_repo = HttpAndFileAgentRepository()
    contracts_repo = HttpContractRepository()
    print(get_contracts(agent_repo, contracts_repo))
