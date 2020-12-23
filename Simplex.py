import numpy as np

def simplex(objective_var, decision_vars, tableau):
    answer = {}
    slack_vars = ["s{}".format(i+1) for i in range(len(tableau)-1)]
    dec_plus_slack = decision_vars + slack_vars 

    basis = slack_vars

    answer[objective_var] = tableau[0][-1]
    for var in dec_plus_slack:
            if var in basis:
                answer[var] = tableau[basis.index(var) + 1][-1]
            else:
                answer[var] = 0

    print_tableau(obj_var, dec_plus_slack, basis, tableau, answer)

    while any([i < 0 for i in tableau[0][:-1]]):
        bring_in_col = np.argmin(tableau[0][:-1])
        bring_in_var = dec_plus_slack[bring_in_col]
        
        #min ratio test
        kick_out_row = None

        min_ratio = np.inf
        for i in range(1, len(tableau)):
            if tableau[i][bring_in_col] > 0:
                ratio = tableau[i][-1] / tableau[i][bring_in_col]
                if ratio < min_ratio:
                    kick_out_row = i
                    min_ratio = ratio

        #update tableau through matrix operations
        tableau[kick_out_row] = tableau[kick_out_row] / tableau[kick_out_row][bring_in_col]
        for i in range(len(tableau)):
            if i != kick_out_row:
                tableau[i] = tableau[i] - tableau[i][bring_in_col] * tableau[kick_out_row]

        #updating basis
        basis[kick_out_row-1] = bring_in_var 

        #updating answer
        answer[objective_var] = tableau[0][-1]
        for var in dec_plus_slack:
            if var in basis:
                answer[var] = tableau[basis.index(var) + 1][-1]
            else:
                answer[var] = 0
        
        print_tableau(obj_var, dec_plus_slack, basis, tableau, answer)
    return answer

def print_tableau(objective_var, dec_plus_slack, basis, tableau, answer):
    print("Basis: {}".format(basis))

    z_col = np.append(np.array([[1]]), np.zeros((len(tableau) - 1, 1)), axis=0)
    whole_tableau = np.block([
        [z_col, tableau]
    ])
    print(whole_tableau)
    print(answer)
    print()


if __name__ == "__main__":
    #examples
    wyndor_tableau = np.array([[-3, -5, 0, 0, 0, 0], [1, 0, 0, 0, 0, 4], [0, 2, 0, 0, 0, 12], [3, 2, 0, 0, 0, 18]])
    dakota_tableau = np.array([[-60, -30, -20, 0, 0, 0, 0], [8, 6, 1, 1, 0, 0, 48], [4, 2, 1.5, 0, 1, 0, 20], [2, 1.5, 0.5, 0, 0, 1, 8]])

    #change these
    obj_var = "z"
    decision_vars = ["a", "b", "c"]
    tableau = dakota_tableau #change this to your own initial tableau

    #Don't change this
    print(simplex(obj_var, decision_vars, tableau))
        


