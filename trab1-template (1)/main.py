#autor = BRUNO KOBI VALADARES DE AMORIM
# ULTIMO UPDATE  = 15/06/2022
# TRABALHO DE BUSCA -  MESTRADO EM COMPUTAÇÃO APLICADA
# DICIPLINA DE INTELIGENCIA ARTIFICIAL
# BUSCAS IMPLEMENTADAS:
    # breadth_first_search
    # depth_first_search
    # uniform_cost_search
    # iterative_deepening_depth_first_search

import time

from src.problems import MazeProblem
from src.viewer import MazeViewer
from src.search import breadth_first_search,depth_first_search,uniform_cost_search,Astar_search,iterative_deepening_depth_first_search


def main():
    # habilitar estrutura de teste
    # OBS: desativar pra visualizar
    teste = 0
    #-------------------------------
    # habilita visualização bfs
    v_bfs = 1
    # habilita visualização Dfs
    v_dfs = 1
    # habilita visualização uniform cost
    v_ucs = 1
    # habilita visualização Busca estrela
    v_star = 1
    # habilita visualização IDDFS
    v_iddfs = 1



    #configuração dos mapas
    mapa_x = 30
    mapa_y = 30
    seed = 42

    # configuração do objetivo
    # Foi denifido 4 posiçoes para os objetivo:
    # end= x e y no maximo --> 1
    # endTop= x maximo e y minimo --> 2
    # endBotton= x minimo e y maximo --> 3
    # center = centro do mapa  --> 4
    posicao = 1

    if posicao == 1:
        goal_x = mapa_x
        goal_y = mapa_y

    if posicao == 2:
        goal_x = mapa_x
        goal_y = 1

    if posicao == 3:
        goal_x = 1
        goal_y = mapa_y-2

    if posicao == 4:
        goal_x = round(mapa_x/2)
        goal_y = round(mapa_y/2)

    maze_problem = MazeProblem(mapa_y, mapa_x,goal_y,goal_x, seed)
    viewer = MazeViewer(maze_problem, step_time_miliseconds=20, zoom=20)

    #MENSAGEM DE HEAD DO PROGRAMA
    print('.______    __    __       _______.  ______     ___             __       ___'), print("|   _  \  |  |  |  |     /       | /      |   /   \           |  |     /   \\"),print("|  |_)  | |  |  |  |    |   (----`|  ,----'  /  ^  \          |  |    /  ^  \\"), print("|   _  <  |  |  |  |     \   \    |  |      /  /_\  \         |  |   /  /_\  \\")
    print("|  |_)  | |  `--'  | .----)   |   |  `----./  _____  \        |  |  /  _____  \\"),print("|______/   \______/  |_______/     \______/__/     \__\       |__| /__/     \__\\"),print("----------------------------------------------------------------------------------")

    if v_dfs == 1 and teste == 0 :
        tempo = 0
        inicio = time.time()
        path2, cost2, n_explorados, n_gerados = depth_first_search(maze_problem, viewer, v_dfs)
        fim = time.time()
        tempo += round(fim - inicio, 2)
        print(f"DFS: Tempo de execução: {round(fim - inicio, 2)}s nós expandidos:{n_explorados} nós gerados:{n_gerados} custo do caminho:{cost2} tamanho do caminho:{len(path2) - 1}")
        print("----------------------------------------------------------------------------------------------------------------------------------------------------")
        if len(path2) == 0:
            print("Labirinto sem Saida")
        viewer.update(path=path2, titulo='BUSCA EM PROFUNDIDADE')
        viewer.pause()

    if v_bfs == 1 and teste == 0 :
        tempo=0
        inicio = time.time()
        path2, cost2, n_explorados, n_gerados = breadth_first_search(maze_problem, viewer,v_bfs)
        fim = time.time()
        tempo += round(fim - inicio, 2)
        print(f"BFS: Tempo de execução: {round(fim - inicio, 2)}s nós expandidos:{n_explorados} nós gerados:{n_gerados} custo do caminho:{cost2} tamanho do caminho:{len(path2) - 1}")
        print("----------------------------------------------------------------------------------------------------------------------------------------------------")
        if len(path2) == 0:
            print("Labirinto sem Saida")
        viewer.update(path=path2, titulo='BUSCA EM LARGURA')
        viewer.pause()

    if v_ucs == 1 and teste == 0:
        tempo = 0
        inicio = time.time()
        path2, cost2, n_explorados, n_gerados = uniform_cost_search(maze_problem, viewer,v_ucs)
        fim = time.time()
        tempo += round(fim - inicio, 2)
        print(f"Uniform Cost: Tempo de execução: {round(fim - inicio, 2)}s nós expandidos: {n_explorados} nós gerados:{n_gerados} custo do caminho: {cost2} tamanho do caminho: {len(path2) - 1}")
        print("----------------------------------------------------------------------------------------------------------------------------------------------------")
        if len(path2) == 0:
            print("Labirinto sem Saida")
        viewer.update(path=path2, titulo='BUSCA DE CUSTO UNIFORME')
        viewer.pause()

    if v_star == 1 and teste == 0:
        tempo = 0
        inicio = time.time()
        path2, cost2, n_explorados, n_gerados = Astar_search(maze_problem, viewer,v_star)
        fim = time.time()
        tempo += round(fim - inicio, 2)
        print(f"A* Star: Tempo de execução:{round(fim - inicio, 2)} s nós explandidos: {n_explorados} nós gerados:{n_gerados} custo do caminho: {cost2} tamanho do caminho: {len(path2) - 1}")
        print("----------------------------------------------------------------------------------------------------------------------------------------------------")
        if len(path2) == 0:
            print("Labirinto sem Saida")
        viewer.update(path=path2, titulo='BUSCA A* ESTRELA')
        viewer.pause()

    if v_iddfs == 1 and teste == 0:
        tempo = 0
        inicio = time.time()
        path2, cost2, n_explorados, n_gerados = iterative_deepening_depth_first_search(maze_problem, viewer, v_iddfs)
        fim = time.time()
        tempo += round(fim - inicio, 2)
        print(f"IDDFS: Tempo de execução: {round(fim - inicio, 2)}s nós expandidos:{n_explorados} nós gerados:{n_gerados} custo do caminho:{cost2} tamanho do caminho:{len(path2) - 1}")
        print("----------------------------------------------------------------------------------------------------------------------------------------------------")
        if len(path2) == 0:
            print("Labirinto sem Saida")
        viewer.update(path=path2, titulo='BUSCA EM IDDFS')
        viewer.pause()



#INICIO DA ESTRUTURA DE TESTE  ----------------------------------------------------------------------------------------------------

    if teste==1:
        # numero repetição teste
        n = 3
        tempo = 0
        # configuração dos mapas
        mapa_x = 100
        mapa_y = 100

        seed = 42

        # habilita  bfs
        bfs = 1
        # habilita  bfs
        dfs = 1
        # habilita  uniform cost
        ucs = 1
        # habilita  Busca estrela
        star = 1
        # habilita  IDDFS
        iddfs=1

        # configuração do objetivo
        # Foi denifido 4 posiçoes para os objetivo:
        # end= x e y no maximo --> 1
        # endTop= x maximo e y minimo --> 2
        # endBotton= x minimo e y maximo --> 3
        # center = centro do mapa  --> 4
        # configuração posição
        posicao = 4

        while posicao < 5 :
            if posicao == 1:
                goal_x = mapa_x
                goal_y = mapa_y

            if posicao == 2:
                goal_x = mapa_x
                goal_y = 1

            if posicao == 3:
                goal_x = 1
                goal_y = mapa_y

            if posicao == 4:
                goal_x = round(mapa_x / 2)
                goal_y = round(mapa_y / 2)

            maze_problem = MazeProblem(mapa_y, mapa_x, goal_y, goal_x, seed)



            # inicio do Loop DFS
            if dfs==1:
                for i in range(n):
                    inicio = time.time()
                    path2, cost2,n_explorados, n_gerados = depth_first_search(maze_problem,viewer,v_dfs)
                    fim = time.time()
                    tempo += round(fim - inicio, 2)
                    print(f"DFS: Tempo de execução: {round(fim-inicio, 2)}s nós expandidos:{n_explorados} nós gerados:{n_gerados} custo do caminho:{cost2} tamanho do caminho:{len(path2) - 1}")
                print(f"tempo médio: {round(tempo / n, 2)}s Mapa:{mapa_y}x{mapa_x}  posição objetivo:{posicao}")
                print("----------------------------------------------------------------------------------------------------------------------------------------------------")
                tempo=0

            # inicio do Loop BFS
            if bfs==1:
                for i in range(n):
                    inicio = time.time()
                    path2, cost2, n_explorados, n_gerados = breadth_first_search(maze_problem, viewer, v_bfs)
                    fim = time.time()
                    tempo += round(fim - inicio, 2)
                    print(
                        f"BFS: Tempo de execução: {round(fim - inicio, 2)}s nós expandidos:{n_explorados} nós gerados:{n_gerados} custo do caminho:{cost2} tamanho do caminho:{len(path2) - 1}")
                print(f"tempo médio: {round(tempo / n, 2)}s Mapa:{mapa_y}x{mapa_x}  posição objetivo:{posicao}")
                print("----------------------------------------------------------------------------------------------------------------------------------------------------")
                tempo = 0

            # inicio do Loop ucs
            if ucs == 1:
                for i in range(n):
                    inicio = time.time()
                    path2, cost2, n_explorados, n_gerados = uniform_cost_search(maze_problem,viewer,v_ucs)
                    fim = time.time()
                    tempo += round(fim - inicio, 2)
                    print(f"Uniform Cost: Tempo de execução: {round(fim-inicio, 2)}s nós expandidos:{n_explorados} nós gerados:{n_gerados} custo do caminho:{cost2} tamanho do caminho:{len(path2) - 1}")
                print(f"tempo médio: {round(tempo / n, 2)}s Mapa:{mapa_y}x{mapa_x}  Mapa:{mapa_y}x{mapa_x}  posição objetivo:{posicao}")
                print("----------------------------------------------------------------------------------------------------------------------------------------------------")
                tempo=0

            # inicio do Loop a star
            if star == 1:
                for i in range(n):
                    inicio = time.time()
                    path2, cost2,n_explorados, n_gerados = Astar_search(maze_problem,viewer,v_star)
                    fim = time.time()
                    tempo += round(fim-inicio, 2)
                    print(f"A* Star: Tempo de execução:{round(fim-inicio, 2)}s nós explandidos:{n_explorados} nós gerados:{n_gerados} custo do caminho:{cost2} tamanho do caminho:{len(path2) - 1}")
                print(f"tempo médio: {round(tempo / n, 2)}s  Mapa:{mapa_y}x{mapa_x}  posição objetivo:{posicao}\n")
                tempo=0
                # inicio do Loop DFS
            if iddfs == 0:
                for i in range(n):
                    inicio = time.time()
                    path2, cost2, n_explorados, n_gerados = iterative_deepening_depth_first_search(maze_problem, viewer, v_iddfs)
                    fim = time.time()
                    tempo += round(fim - inicio, 2)
                    print(
                        f"IDDFS: Tempo de execução: {round(fim - inicio, 2)}s nós expandidos:{n_explorados} nós gerados:{n_gerados} custo do caminho:{cost2} tamanho do caminho:{len(path2) - 1}")
                print(f"tempo médio: {round(tempo / n, 2)}s Mapa:{mapa_y}x{mapa_x}  posição objetivo:{posicao}\n")
                print("----------------------------------------------------------------------------------------------------------------------------------------------------")
                tempo = 0
            posicao += 1



    #MENSAGEM DE FINALIZAÇÃO DO PROGRAMA
    print("   _"), print("  | |"), print("  | |===( )   //////"), print("  |_|   |||  | o o|"),print("         ||| ( c  )                  ____"), print("          ||| \= /                  ||   \_")
    print("            ||||||                  ||     |"),print('            ||||||               ...||__/|-"'), print("            ||||||             __|________|__"), print("              |||             |______________|")
    print("              |||             || ||      || ||"),print("              |||             || ||      || ||"), print("--------------|||-------------||-||------||-||-------"), print("              |||             || ||      || ||")
    print("              |__>            || ||      || ||")
    print("----------------  THE END --------------------------")




















if __name__ == "__main__":
    main()
