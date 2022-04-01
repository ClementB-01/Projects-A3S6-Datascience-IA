from numpy import sin
import random as rd

def Selection(indiv_list):
    return indiv_list
    
def XOSubject(individual1, individual2, strat = '1XO'): # FONCTIONNELLE EN TEST UNITAIRE
    individual = list()
    choiceXO = None
    indiv1 = individual1.copy()
    indiv2 = individual2.copy()

    choice1 = rd.choice([indiv1, indiv2]) #Random selection of the which individual will be selected firstly
    choice2 = indiv1 if choice1 == indiv2 else indiv2

    if strat == 'Mix':
        choiceXO = rd.choice(['1XO', '2XO'])

    if strat == '1XO' or choiceXO == '1XO': # One crossover
        cut = (len(indiv1) // 2) - 1
        for i in range(len(indiv1)):
            if i <= cut:
                individual.append(choice1[i])
            else:
                individual.append(choice2[i])

    if strat == '2XO' or choiceXO == '2XO': # Two crossover
        cut = len(indiv1) // 3
        for i in range(len(indiv1)):
            if i < cut:
                individual.append(choice1[i])
            if i < 2 * (cut) and i >= cut: 
                individual.append(choice2[i])
            elif i >= cut * 2:
                individual.append(choice1[i])
    return individual

def MutateSubject(individual, strat = 'Insertion'): # FONCTIONNELLE EN TEST UNITAIRE
    indiv = individual.copy()
    pivot1 = 0
    pivot2 = 0
    choice = None
    while pivot1 == pivot2:
        pivot1 = rd.randint(0,5)
        pivot2 = rd.randint(0,5)
    #print(pivot1, pivot2)

    if strat == 'Mix': # Use all mutation strategies
        choice = rd.choice(['Insertion', 'Reversion', 'Swap', 'Random'])
        #print("Mix")

    if strat == 'Insertion' or choice == 'Insertion':
        indiv.insert((pivot1 + 1) % len(indiv), indiv[pivot2]) # Insert pivot2 just after pivot1 no matter which of them has the highest index
        if pivot1 < pivot2:
            indiv.pop(pivot2 + 1)
        else:
            indiv.pop(pivot2)
        #print("Insertion")

    if strat == 'Reversion' or choice == 'Reversion':
        if max(pivot1, pivot2) == pivot2: # If pivot1 is before pivot2, just slicing the list
            temp = indiv[pivot1:pivot2 +1]
            temp.reverse()
            for i in range(pivot1, pivot2 + 1):
                indiv[i] = temp[i - pivot1]
        else:
            temp = indiv[pivot1::] # Else we take the extremities and then reverse the list
            temp.extend(indiv[:pivot2 + 1])
            temp.reverse()
            for i in range(len(indiv)):
                if i <= pivot2:
                    indiv[i] = temp[len(temp) - pivot2 - 1 + i]
                if i >= pivot1:
                    indiv[i] = temp[i - pivot1]
        #print("Reversion")
        

    if strat == 'Swap' or choice == 'Swap':
        temp = indiv[pivot2]
        indiv[pivot2] = indiv[pivot1]
        indiv[pivot1] = temp
        #print("Swap")

    if choice == 'Random':
        pivot2 = round(rd.uniform(-100, 100), 3)
        indiv[pivot1] = pivot2
    
    return indiv

def ToNextGeneration(indiv_list, known_values, dico_parameter, strat = 'BWheel', parameter_percentage = [12,60,28]):
    if parameter_percentage[0] + parameter_percentage[1] + parameter_percentage[2] != 100:
        raise Exception("False percentage given")
    
    indiv_list.sort(key = lambda indiv : Fitness(indiv, known_values))
    
    if strat == 'Linear Filter':
        for i in range(len(indiv_list)):
            if i <= len(indiv_list) * parameter_percentage[0] // 100:
                new_gen.append(indiv_list[i])
            elif i > len(indiv_list) * parameter_percentage[0] // 100 and i <= len(indiv_list) * parameter_percentage[1] // 100:
                new_gen.append(XOSubject(indiv_list[i], indiv_list[i+1]))
            else:
                new_gen.append(MutateSubject(indiv_list[i]))

    if strat == 'Elitism':
        for i in range(len(indiv_list)// 10):
            new_gen.append(indiv_list[i])
            new_gen.append(XOSubject(indiv_list[i], indiv_list[i+1]))
            new_gen.append(XOSubject(indiv_list[i], indiv_list[i+2]))
            new_gen.append(XOSubject(indiv_list[i], indiv_list[i+3]))
            new_gen.append(XOSubject(MutateSubject(indiv_list[i]), indiv_list[i+1]))
            new_gen.append(XOSubject(MutateSubject(indiv_list[i]), indiv_list[i+2]))
            new_gen.append(XOSubject(indiv_list[i], MutateSubject(indiv_list[i+1])))
            new_gen.append(XOSubject(indiv_list[i], MutateSubject(indiv_list[i+2])))
            new_gen.append(XOSubject(indiv_list[i], MutateSubject(indiv_list[i+3])))
            new_gen.append(MutateSubject(indiv_list[i]))

    if strat == 'BWheel':
        new_gen = [indiv_list[0]] #On ajoute le meileur individu systématiquement
        for i in range(len(indiv_list) - 1):
            fitness_biased_choice = rd.choices([1,2,3,4,5], weights=[30,25,20,15,10], k=1)
            rdown = 0
            rup = 0
            if fitness_biased_choice[0] == 1:
                rdown = dico_parameter[1][0]
                rup = dico_parameter[1][1]
            if fitness_biased_choice[0] == 2:
                rdown = dico_parameter[2][0]
                rup = dico_parameter[2][1]
            if fitness_biased_choice[0] == 3:
                rdown = dico_parameter[3][0]
                rup = dico_parameter[3][1]
            if fitness_biased_choice[0] == 4:
                rdown = dico_parameter[4][0]
                rup = dico_parameter[4][1]
            if fitness_biased_choice[0] == 5:
                rdown = dico_parameter[5][0]
                rup = dico_parameter[5][1]
            indiv_choice = rd.randint(rdown, rup)
            choice_offspring_type = rd.choices([1,2,3], weights=parameter_percentage, k=1)
            if choice_offspring_type == [1]:
                new_gen.append(indiv_list[indiv_choice])
            if choice_offspring_type == [2]:
                indiv_choice2 = rd.randint(rdown, rup)
                new_gen.append(XOSubject(indiv_list[indiv_choice], indiv_list[indiv_choice2], 'Mix'))
            if choice_offspring_type == [3]:
                new_gen.append(MutateSubject(indiv_list[indiv_choice], 'Mix'))
    return new_gen

def Fitness(individual, known_values): # FONCTIONNELLE EN TEST UNITAIRE
    score = 0
    for t, real_values in known_values.items():
        x_estimate = individual[0] * sin(individual[1]*t + individual[2])
        y_estimate = individual[3] * sin(individual[4]*t + individual[5])
        x_real = real_values[0]
        y_real = real_values[1]
        score += abs(x_real - x_estimate) + abs(y_real - y_estimate)
    return round(score, 5)

def GeneratePopulation(size, up, down): # FONCTIONNELLE EN TEST UNITAIRE
    indiv_list = list()
    for i in range(size):
        indiv_list.append([round(rd.uniform(down, up), 3) for x in range(6) ])
    return indiv_list

def LoadDatas(path): # FONCTIONNELLE EN TEST UNITAIRE
    file = open(path, 'r')
    known_values = {}
    count = 0
    for i in file:
        if count != 0:
            i = [x.split(';') for x in i.split()]
            key = float (i[0][0])
            value = (float (i[0][1]), float (i[0][2]))
            known_values.update({key : value})
        count += 1
        #print(i)
    return known_values

def AlgoG():
    stop = False
    #print("Choose the strategy to stop the algorithm : \n 1. Number of iteration \n 2. Number of Fitness call \n 3. CPU Time \n 4. Stability")
    #stop_mod = input("==> ")
    stop_mod = 'Iteration'
    #stop_parameter = int(input("Give correct parameter : "))
    stop_parameter = 200
    known_values = LoadDatas('Projet_algo_genetique/position_sample.csv')

    #size = int(input("Enter the size of population to simulate : "))
    size = 10000
    up = 100
    down = -100

    indiv_list = GeneratePopulation(size, up, down)
    count = 1
    dico_parameter = {1 : (0,size*0.1), 2 : (size*0.1 + 1,size*0.3), 3 : (size*0.3 + 1, size*0.6), 4 : (size*0.6+1, size*0.9), 5 : (size*0.9+1, size-1)}
    fit = [0,100000,0]
    while stop == False:
        indiv_list = ToNextGeneration(indiv_list, known_values, dico_parameter)
        print(f"----- Generation n°{count} -----")
        indiv_list.sort(key = lambda indiv : Fitness(indiv, known_values))
        #print(indiv_list[0])
        fit[0] = Fitness(indiv_list[0], known_values)
        fit[1] = indiv_list[0]
        #print(len(indiv_list))
        print(fit[0])
        count += 1
        if stop_mod == 'Iteration':
            if count == stop_parameter:
                stop = True
        #if fit[0]/60 <= 2:
            #print(indiv_list[0])
       #if stop_mod == 'CPU Time':
    print(fit)
    return fit

#print(GeneratePopulation(10, 100, -100)) #test unitaire de GeneratePopulation()
#print(LoadDatas('Projet_algo_genetique/position_sample.csv')) #test unitaire de LoadDatas()
#print(Fitness([0,0,0,-56,2,3.14],LoadDatas('Projet_algo_genetique/position_sample.csv'))) #test unitaire de Fitness()

#individual = [0,1,2,3,4,5,6]
#individual2 = [100, 10, 20, 30, 40, 50, 60]
#print(XOSubject(individual, individual2, '2XO')) # Test unitaire de XOSubject()
#for i in range(10): # Test unitaire  de MutateSubject()
    #print(MutateSubject(individual, 'Mix'))

#indiv_list = GeneratePopulation(15,100,-100)
#print(indiv_list)
#indiv_list.sort(key = lambda indiv : Fitness(indiv, LoadDatas('Projet_algo_genetique/position_sample.csv')))
#for i in indiv_list:
    #print(Fitness(i,LoadDatas('Projet_algo_genetique/position_sample.csv')))
    #print(i)
#indiv_list = ToNextGeneration(indiv_list, LoadDatas('Projet_algo_genetique/position_sample.csv'), dico_parameter={1 : (0,int(15*0.1)), 2 : (int(15*0.1 + 1),int(15*0.3)), 3 : (int(15*0.3 + 1), int(15*0.6)), 4 : (int(15*0.6+1), int(15*0.9)), 5 : (int(15*0.9+1), 15-1)})
#print(f"Affiche longueur sortie : {len(indiv_list)}")
#print(indiv_list)
AlgoG()