import math

CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"

def getDirecao(n):
    '''Retorna a direção para o qual o número n aponta ou retorna "igual" caso n seja válido
    '''
    global direcoes
    if n in direcoes.keys():
        return direcoes[n]

def player(number_guesses, rule_guesses):
    global direcoes, validos, n2, binEsq, BindDir, validamosMod, x

    """Função principal do jogador.
    Retorna para game.py o chute de número ou de regra atual.
    
    Estratégia:
        1. Valida se a regra atual é pot
        2. Se não for, valida se a regra atual é mod
            2.1 Procura o primeiro número válido, chuta números cada vez maiores até que um chute retorne "igual" ou "menor",
                no segundo caso garante que há um válido entre os dois últimos números chutados e incia uma busca binária para
                descobri-lo
            2.2 Procura o segundo válido da mesma forma, mas buscando encontrar um número "igual" ou "maior" para fazer a
                busca binária
        3. Se não for, valida se a regra atual é int 
            3.1 Procura o primeiro número válido se ele ainda não foi descoberto
            3.2 Aumenta o tamanho do intervalo até verificar que ele está no tamanho máximo
    """

    # atualizamos o dicionário direcoes com base no último chute
    if number_guesses:
        last_valor = number_guesses[-1][0]  # número chutado
        direcao    = number_guesses[-1][1]  # "maior" ou "menor"
        hit        = number_guesses[-1][2]  # true or false 

        direcoes[last_valor] = "igual" if hit else direcao # adiciona o último chute ao dicionário

    else: # não tínhamos chutes ainda, fazemos o primeiro chute e iniciamos as variáveis
        direcoes = {} # associa números com suas direções
        validos = []  # lista todos os válidos encontrados até agora
        x = 2         # armazena o chute atual na busca por mod e int 
        binEsq, BindDir = None, None # variáveis auxiliares para busca binária
        validamosMod = False         # verifica se já consideramos a possibilidade de ser mod
        return [CHUTE_DE_NUMERO, 2]  # efetua o primeiro chute 
    
    ############ inciamos a lógica de chutes ############
    #####################################################

    if getDirecao(2) == "menor" and len(rule_guesses) == 0:
        # caso 2 aponte para menor, concluímos que 1 é válido
        # caso seja potência, obrigatoriamente 1 será válido
        # logo, testamos para ver se realmente são potências

        # tratamento de exeções e redundância:
        # os números válidos encontrados nesse caso são ignorados,
        # pois caso mod ou int ative a busca por potências, eles serão descobertos segundo a lógica principal

        # esse é o único válido registrado.
        # caso seja mod ou int, a lógica principal começará levando em conta 1 como válido
        if 1 not in validos:
            validos.append(1)
        
        
        # testamos 3**6, 9**3, 27**2 (p = 6, 3 ou 2)
        if 729 not in direcoes.keys():
            return ["NUMBER", 729]
        elif getDirecao(729) == "igual":
            # p é 2, 3 ou 6, logo testamos 6**2 

            if 36 not in direcoes.keys(): 
                return ["NUMBER", 36]
            elif getDirecao(36) == "igual":   # confirmamos p == 2
                return [CHUTE_DE_REGRA, ["pot", 2, 0]]
            elif getDirecao(36) == "maior": # a potência maior mais próxima é 2**6, logo inferimos que ela é válida
                return [CHUTE_DE_REGRA, ["pot", 6, 0]]
            else:                           # a potência menor mais próxima é 3**3, logo inferimos que ela é válida
                return [CHUTE_DE_REGRA, ["pot", 3, 0]]
        # eliminamos os valores 2, 3, 6
        # p é 4, 5, 7, 8, 9 ou 10 

        elif getDirecao(729) == "maior":
            # a potência maior mais próxima é 2**10 (4**5), logo inferimos que ela é válida
            # p é 5 ou 10

            # testamos 2**5 
            if 32 not in direcoes.keys():
                return ["NUMBER", 32]
            elif getDirecao(32) == "igual": # confirmamaos p == 5
                return [CHUTE_DE_REGRA, ["pot", 5, 0]]
            else:                           # confirmamos p == 10
                return [CHUTE_DE_REGRA, ["pot", 10, 0]]
        # eliminamos os valores 5 e 10
        # p é 4, 7, 8 ou 9

        else:
            # a potência menor mais próxima é 5**4 (25**2), logo inferimos que ela é válida
            # nesse caso, p é 2 ou 4 (sendo que 2 já foi eliminado)
            # a segunda potência menor mais próxima é 2**9 (8**3) (isso se não for 4)
            # logo a direção apontou para uma dessas potências

            # testamos 3**9
            if 19683 not in direcoes.keys():
                return ["NUMBER", 19683]
            elif getDirecao(19683) == "igual": # confirmamos p == 9
                return [CHUTE_DE_REGRA, ["pot", 9, 0]]
            elif getDirecao(19683) == "maior": # a potência menor mais próxima é 141**2 (12**4), logo inferimos que ela é válida
                return [CHUTE_DE_REGRA, ["pot", 4, 0]] # como p == 2 já foi eliminado, confirmamos p == 4
            else: 
                # p é 7 ou 8
                if 256 not in direcoes.keys():
                    return ["NUMBER", 256]
                elif getDirecao(256) == "igual": # confirmamos p == 8
                    return [CHUTE_DE_REGRA, ["pot", 8, 0]]
                else:                            # por eliminação, confirmamos p == 7
                    return [CHUTE_DE_REGRA, ["pot", 7, 0]]

    else:
        # caso seja mod, obrigatoriamente teremos um válido entre os 100 primeiros números
        # logo, se não acharmos um válido entre os 100 primeiros, consideramos que já validamos a possibilidade de ser mod
        # ou se decobrirmos apenas 1 válido entre os (100 + esse válido) primeiros, consideramos também que já validamos a possibilidade de ser mod
        # no caso de já termos validado a possibilidade de ser mod, tentamos descobrir o intervalo
        if not validamosMod:

            # Os chutes apontarão para maior até passarmos por um válido
            # quando apontar para o menor, teremos um período no qual reside um número válido.
            # faremos busca binária para encontrar esse válido.
            # note que esse método sempre encontra o menor número válido
            if len(validos) == 0:
                if getDirecao(x) == "menor":
                    # inciamos a busca binária
                    if BindDir == binEsq == None:
                        binEsq, BindDir = [i[0] for i in number_guesses[-2:]]
                    while True:
                        c = (binEsq + BindDir) // 2
                        if c not in direcoes:
                            return ["NUMBER", c]
                        
                        if direcoes[c] == "maior":
                            binEsq = c + 1
                        elif direcoes[c] == "menor":
                            BindDir = c - 1
                        else: # achamos um valor
                            binEsq = BindDir = None # reiniciamos os parâmetros da busca binária
                            validos.append(c)
                            x = c*2
                            return ["NUMBER", x]
                            # preparamos para a busca do segundo valor.

                elif getDirecao(x) == "igual": # achamos um valor
                    validos.append(x)
                    x = x * 2
                    return ["NUMBER", x]
                    # preparamos para a busca do segundo valor.

                else: # aponta para maior 
                    if x == 100: # acabamos de analisar o 100 e não era ele
                        validamosMod = True # logo não era mod
                    else: # escolhemos o próximo número a ser verificado
                        if x == 2:
                            x = 4

                        # o próximo será a média aritmética entre x+1 e 2(x+1)
                        # isso garante que nunca pularemos um válido
                        else:
                            x = (3*x+3)//2 if (3*x+3)//2 < 100 else 100

                        return ["NUMBER", x]

            # se já achamos o primeiro válido, 
            # a lógica inverte, esperamos um número apontar para longe do primeiro válido
            # procuramos até 100 + primeiro válido pois os válidos estão no máximo a 100 de distância
            elif len(validos) == 1:
                if getDirecao(x) == "menor":
                    if x == 100 + validos[0]: # só descobrimos 1 válido entre 0 e 100+validos[0], logo é int
                        validamosMod = True   # validamos que não é mod
                    else:
                        x = x + (x - validos[0]) if x + (x - validos[0]) < 100 + validos[0] else 100 + validos[0] # isso garante que não pularemos nenhum número válido
                        return ["NUMBER", x]
                elif getDirecao(x) == "igual": # achamos o segundo válido
                    validos.append(x)
                    validamosMod = True # temos informação suficiente para avaliar a possibilidade de ser mod
                    return [CHUTE_DE_REGRA, ["mod", validos[1] - validos[0], validos[0]%(validos[1] - validos[0]) ]] 
                    # achamos dois válidos consecutivos, 
                    # logo, o segundo - o primeiro retornará k. Calculamos o r com base em k.

                elif getDirecao(x) == "maior": # não estamos mais apontando para o primeiro válido
                    if BindDir == binEsq == None:
                        binEsq, BindDir = x, x + (x - validos[0]) if x + (x - validos[0]) < 100 + validos[0] else 100 + validos[0] 
                    while True: # fazemos a busca binária                                                                         
                        c = (binEsq + BindDir) // 2
                        if c not in direcoes:
                            return ["NUMBER", c]
                        if direcoes[c] == "maior":
                            binEsq = c + 1
                        elif direcoes[c] == "menor":
                            BindDir = c - 1
                        else: 
                            validos.append(c)
                            validamosMod = True # temos informação suficiente para avaliar a possibilidade de ser mod
                            return [CHUTE_DE_REGRA, ["mod", validos[1] - validos[0], validos[0]%(validos[1] - validos[0]) ]] 
                            # achamos dois válidos consecutivos, 
                            # logo, o segundo - o primeiro retornará k. Calculamos o r com base em k.

    if validamosMod:
        # validamos que não é mod
        # sabemos que é int 

        # temos que procurar o primeiro válido para usá-lo de base
        # para isso, fazemos uma busca binária
        if len(validos) == 0:
            while True:
                if binEsq == BindDir == None:
                    binEsq = 101
                    BindDir = 100_000
                c = (binEsq + BindDir) // 2
                if c not in direcoes:
                    return ["NUMBER", c]
                if direcoes[c] == "maior":
                    binEsq = c + 1
                elif direcoes[c] == "menor":
                    BindDir = c - 1
                else: 
                    validos.append(c)
                    break

        # se já encontramos um número, daí usamos ele como base
        # (se acabamos de achar um válido na busca binária, entra aqui também)
        if len(validos) > 0:

            # verifica se o último número chutado na determinação do tamanho do período era válido
            if number_guesses[-1][2]:
                n = number_guesses[-1][0]
                if n not in validos:
                    validos.append(n)

            menor = min(validos)
            maior = max(validos)
            tamanho = maior - menor
            maxDis = 100 - tamanho # maior distância de chute a partir de alguma das extremidades
            achouMaximo = (maior+1) in direcoes.keys() or maior == 100_000 # verificou que não tem nenhum válido após o máximo atual 
            achouMinimo = (menor-1) in direcoes.keys() or menor == 1       # verificou que não tem nenhum válido antes do mínimo atual

            # se já fechou o tamanho máximo do intervalo
            # ou se verificou que não existe válidos após o intervalo atual,
            # então achou
            if tamanho == 100 or (achouMaximo and achouMinimo):
                return [CHUTE_DE_REGRA, ["int", menor, maior]]
            else:
                if not achouMinimo:

                    # consideramos a possibilidade de ter um chute não válido que reduz o escopo da procura de extremos
                    maxDisMenor = maxDis
                    if len(direcoes.keys()) != 0:
                        lOrdChutes = sorted(list(direcoes.keys()))
                        if lOrdChutes.index(menor) != 0:
                            maxDisMenor = menor - lOrdChutes[lOrdChutes.index(menor) - 1] - 1 # consideramos o chute mais próximo do menor pois o período se estenderá até no máximo ele
                            if maxDisMenor > 101: maxDisMenor = maxDis

                    proposta = menor - math.ceil(maxDisMenor/2) if menor - math.ceil(maxDisMenor/2) > 1 else 1 # verifica a uma distância do menor atual 

                    while True:
                        if proposta in direcoes.keys(): # se está tentando chutar um valor que já foi estimado, ele não é válido, logo chuta um mais próximo 
                            proposta = (proposta + menor)//2 
                        else: # verifica o número ainda desconhecido
                            return ["NUMBER", proposta]
                        
                elif not achouMaximo:
                    
                    # consideramos a possibilidade de ter um chute não válido que reduz o escopo da procura de extremos
                    maxDisMaior = maxDis
                    if len(direcoes.keys()) != 0:
                        lOrdChutes = sorted(list(direcoes.keys()))
                        if lOrdChutes.index(maior) != len(lOrdChutes) - 1:
                            maxDisMaior = lOrdChutes[lOrdChutes.index(maior) + 1] - maior - 1 # consideramos o chute mais próximo do maior pois o período se estenderá até no máximo ele
                            if maxDisMaior > 101: maxDisMaior = maxDis

                    proposta = maior + math.ceil(maxDisMaior/2) if maior + math.ceil(maxDisMaior/2) < 100_000 else 100_000

                    while True:
                        if proposta in direcoes.keys(): # se está tentando chutar um valor que já foi estimado, ele não é válido, logo chuta um mais próximo
                            proposta = (proposta + maior)//2
                        else: # verifica o número ainda desconhecido
                            return ["NUMBER", proposta]