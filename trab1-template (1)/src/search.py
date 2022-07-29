
from math import inf
import time

from collections import deque

from typing import Any, List, Union, Tuple

from src.problems import ProblemInterface,MazeProblem
from src.viewer import ViewerInterface



class Node:
    # The output path is generated backwards starting from
    # the goal node, hence the need to store the parent in
    # the node.
    def __init__(self, state: Any, action=None, previous_node=None):
        self.state = state
        self.action = action
        self.previous_node = previous_node

    def __repr__(self):
        return f"Node(state={self.state}, action={self.action}, previous_node={self.previous_node})"

    def __eq__(self, n) -> bool:
        return (self.state == n.state)

    # method necessary for easily checking if nodes
    # have already been added to sets or used as keys
    # in dictionaries.
    def __hash__(self):
        return hash(self.state)


def breadth_first_search(problem: ProblemInterface, viewer: ViewerInterface, v_bfs) -> Tuple[List[Any], float]:
    # nós gerados que ainda não foram expandidos
    to_explore = deque()



    # nós cujos vizinhos já foram gerados
    expanded = set()
    gerados = set()

    # adiciona o nó inicial à lista de nós
    # ainda a ser expandido.
    state_node = Node(problem.initial_state())
    to_explore.append(state_node)

    # variável para armazenar o nó objetivo quando ele for encontrado.
    goal_found = None

    # Repita enquanto não encontramos o objetivo e ainda temos
    # nós para expandir. Se não houver mais nós
    # para expandir em busca ampla, o objetivo é inacessível.

    while (len(to_explore) > 0) and (goal_found is None):
        # seleciona o próximo nó ou expansão
        state_node = to_explore.popleft()


        neighbors = _generate_neighbors(state_node, problem)

        for n in neighbors:
            if (n not in expanded) and (n not in to_explore):
                if problem.is_goal(n.state):
                    goal_found = n
                    break
                to_explore.append(n)
                gerados.add(n)

        expanded.add(state_node)

        if v_bfs == 1:
            viewer.update(state_node.state,generated=to_explore,expanded=expanded,titulo="BUSCA EM LARGURA")

    path = _extract_path(goal_found)
    cost = _path_cost(problem, path)
    n_gerados = len(gerados)
    n_explorados = len(expanded)

    return path, cost, n_explorados, n_gerados

def depth_first_search(problem: ProblemInterface, viewer: ViewerInterface, v_dfs) -> Tuple[List[Any], float]:
    # Pilhas nós gerados que ainda não foram expandidos
    to_explore = []

    # nós expandidos
    expanded = set()
    # nós gerados
    gerados = set()

    # adiciona o nó inicial à lista de nós
    # ainda a ser expandido.
    state_node = Node(problem.initial_state())
    to_explore.append(state_node)

    # variável para armazenar o nó objetivo quando ele for encontrado.
    goal_found = None

    # Repita enquanto não encontramos o objetivo e ainda temos
    # nós para expandir. Se não houver mais nós
    # para expandir em busca ampla, o objetivo é inacessível.
    while (len(to_explore) > 0) and (goal_found is None):
        # seleciona o próximo nó da pilha
        state_node = to_explore.pop()

        #função encontra os vizinhos de um nó
        neighbors = _generate_neighbors(state_node, problem)
        for n in neighbors:
            if (n not in expanded) and (n not in to_explore):
                if problem.is_goal(n.state):
                    goal_found = n
                    break
                to_explore.append(n)
                gerados.add(n)

        expanded.add(state_node)

        #variavel criada para controle dinamico de teste - exibição grafica
        if v_dfs :
            viewer.update(state_node.state,generated=to_explore,expanded=expanded,titulo='BUSCA EM PROFUNDIDADE')

    path = _extract_path(goal_found)
    cost = _path_cost(problem, path)
    n_gerados = len(gerados)
    n_explorados = len(expanded)

    return path, cost, n_explorados, n_gerados

def uniform_cost_search(problem: ProblemInterface, viewer: ViewerInterface,v_ucs) -> Tuple[List[Any], float]:

    # nós gerados que ainda não foram expandidos
    to_explore = []

    # lista de custo de cada caminho
    to_cost = []

    # nós cujos vizinhos já foram gerados
    expanded = set()
    #dicionario auxiliar para mostrar o total de nós gerados
    gerados = set()

    # adiciona o nó inicial à lista de nós
    # ainda a ser expandido.
    state_node = Node(problem.initial_state())
    to_explore.append(state_node)
    to_cost.append(0)


    # variável para armazenar o nó objetivo quando ele for encontrado.
    goal_found = None

    # Repita enquanto não encontramos o objetivo e ainda temos
    # nós para expandir. Se não houver mais nós
    # para expandir em busca ampla, o objetivo é inacessível.
    while (len(to_explore) > 0) and (goal_found is None):

        #condicional de verifica o caminho de menor custo
        if to_cost :
            #pega o menor custo na lista
            menor = min(to_cost)
            #pega o index (posição do menor custo na lista)
            menor_index = to_cost.index(menor)
        else :
            menor_index = 0
        #pega o no de menor custo da lista de explorados
        state_node = to_explore.pop(menor_index)
        # pega o menor custo da lista de custo
        cost_pai = to_cost.pop(menor_index)

        #função gera vizinhos do nó
        neighbors = _generate_neighbors(state_node, problem)

        #loop que percorre os vizinhos encontrados
        for n in neighbors:
            #função retorna o custo entro o nó atual e nó vizinho n
            cost_atual = problem.step_cost(state_node.state, n.action,n.state)


            if (n not in expanded) and (n not in to_explore):
                if problem.is_goal(n.state):
                    goal_found = n
                    break
                #amazena os custo do nó n somado com o custo do nó pai na lista cost
                to_cost.append(cost_pai+cost_atual)
                to_explore.append(n)
                gerados.add(n)
        expanded.add(state_node)

        # variavel criada para controle dinamico de teste - exibição grafica
        if v_ucs==1:
            viewer.update(state_node.state,generated=to_explore,expanded=expanded,titulo='BUSCA DE CUSTO UNIFORME')

    path = _extract_path(goal_found)
    cost = _path_cost(problem, path)
    n_gerados = len(gerados)
    n_explorados = len(expanded)

    return path, cost, n_explorados, n_gerados

def Astar_search(problem: ProblemInterface, viewer: ViewerInterface,v_star) -> Tuple[List[Any], float]:

    # nós gerados que ainda não foram expandidos
    to_explore = []

    # lista de custo + heristica de cada nó
    to_cost = []

    # nós cujos vizinhos já foram gerados
    expanded = set()
    # dicionario auxiliar para mostrar o total de nós gerados
    gerados = set()

    # adiciona o nó inicial à lista de nós
    # ainda a ser expandido.
    state_node = Node(problem.initial_state())
    to_explore.append(state_node)
    to_cost.append(0)



    # variável para armazenar o nó objetivo quando ele for encontrado.
    goal_found = None

    # Repita enquanto não encontramos o objetivo e ainda temos
    # nós para expandir. Se não houver mais nós
    # para expandir em busca ampla, o objetivo é inacessível.
    while (len(to_explore) > 0) and (goal_found is None):
        # condicional de verifica o caminho de menor custo
        if to_cost:
            # pega o menor custo na lista
            menor = min(to_cost)
            # pega o index (posição do menor custo na lista)
            menor_index = to_cost.index(menor)
        else:
            menor_index = 0
        # pega o no de menor custo da lista de explorados
        state_node = to_explore.pop(menor_index)
        # pega o menor custo da lista de custo
        cost_pai = to_cost.pop(menor_index)

        #função gera vizinhos do nó
        neighbors = _generate_neighbors(state_node, problem)

        for n in neighbors:
            cost_atual = problem.step_cost(state_node.state, n.action,n.state)
            #função retorna o valor da heuristica no nó n
            #fator de otimização - obteve uma melhora no tempo de execução e nos gerados e expandidos de quase 90%
            fator_Otimização = 20
            heuristica = round(problem.heuristic_cost(n.state)) ** fator_Otimização



            #print(f"custos:{n.state}.heuristica: {heuristica}.")
            if (n not in expanded) and (n not in to_explore):
                if problem.is_goal(n.state):
                    goal_found = n
                    break
                #função f(n) = custo caminho + heuristica
                to_cost.append(cost_pai+cost_atual+heuristica)
                to_explore.append(n)
                gerados.add(n)

        expanded.add(state_node)

        # variavel criada para controle dinamico de teste - exibição grafica
        if v_star==1:
            viewer.update(state_node.state, generated=to_explore,expanded=expanded,titulo='BUSCA A* ESTRELA')

    path = _extract_path(goal_found)
    cost = _path_cost(problem, path)
    n_gerados = len(gerados)
    n_explorados = len(expanded)

    return path, cost, n_explorados, n_gerados

def iterative_deepening_depth_first_search(problem: ProblemInterface, viewer: ViewerInterface, v_iddfs) -> Tuple[List[Any], float]:
    #variavel de nivel maximo
    nivelMax = 1

    #variavel resultado  0.0 considerado retorno falso
    resultado = 0.0

    #loop da função de verifica de altura do grafo
    while resultado == 0.0:
        #chamada da função verificar se o altura maxima tem reposta
        resultado = idfs(nivelMax, problem, viewer, v_iddfs)
        nivelMax +=1
    path = resultado[0]
    cost = resultado[1]
    n_gerados = resultado[2]
    n_explorados = resultado[3]

    return path, cost, n_explorados, n_gerados






def idfs(nivelMax:int, problem,viewer, v_iddfs) -> float:
    # Pilhas nós gerados que ainda não foram expandidos
    to_explore = deque()
    to_cost = deque()

    # nós expandidos
    expanded = set()
    # nós gerados
    gerados = set()

    # adiciona o nó inicial à lista de nós
    # ainda a ser expandido.
    state_node = Node(problem.initial_state())
    to_explore.append(state_node)
    to_cost.append(0)

    # variável para armazenar o nó objetivo quando ele for encontrado.
    goal_found = None
    while (len(to_explore) > 0) and (goal_found is None):
        # pega o no de menor custo da lista de explorados
        state_node = to_explore.popleft()
        # pega o menor custo da lista de custo
        if len(to_cost) > 0:
            nivelAtual = to_cost.popleft()



        if nivelAtual == (nivelMax):
            resultado = 0.0
            return resultado

        for i in range(nivelMax):
            # função encontra os vizinhos de um nó
            neighbors = _generate_neighbors(state_node, problem)
            for n in neighbors:
                if (n not in expanded) and (n not in to_explore):
                    if problem.is_goal(n.state):
                        goal_found = n
                        break
                    to_explore.append(n)
                    to_cost.append(nivelAtual + 1)


            expanded.add(state_node)

            # variavel criada para controle dinamico de teste - exibição grafica
            if v_iddfs:
                viewer.update(state_node.state, generated=to_explore, expanded=expanded, titulo='BUSCA EM IDDFS')



    path = _extract_path(goal_found)
    cost = _path_cost(problem, path)
    n_gerados = len(gerados)
    n_explorados = len(expanded)

    return path, cost, n_explorados, n_gerados



def _path_cost(problem: ProblemInterface, path: List[Node]) -> float:
    if len(path) == 0:
        return inf
    cost = 0
    for i in range(1, len(path)):
        cost += problem.step_cost(path[i].previous_node.state,
                                  path[i].action,
                                  path[i].state)
    return cost


def _extract_path(goal: Union[Node, None]) -> List[Node]:
    path = []
    state_node = goal
    while state_node is not None:
        path.append(state_node)
        state_node = state_node.previous_node
    path.reverse()
    return path


def _generate_neighbors(state_node: Node, problem: ProblemInterface) -> List[Node]:
    # generate neighbors of the current state
    neighbors = []
    state = state_node.state
    available_actions = problem.actions(state)
    for action in available_actions:
        next_state = problem.transition(state, action)
        neighbors.append(Node(next_state, action, state_node))
    return neighbors
