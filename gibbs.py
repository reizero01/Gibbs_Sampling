import pandas as pd
import random
import numpy 

class Gibbs:
    def __init__(self, *args, **kwargs):
        self.data = ''

    def create_data_set(self):
        Cloud = pd.DataFrame([0.5, 0.5], index=['T', 'F'], columns=['Cloud'])
        Cloud.__name__ = 'Cloud'
        Sprinkler = pd.DataFrame([[0.1, 0.9], [0.5, 0.5]], index=['T', 'F'], columns=['sprinkler', '-sprinkler'])
        # Sprinkler.parent1 = Cloud
        Sprinkler.__name__ = 'Sprinkler'
        Rain = pd.DataFrame([[0.8, 0.2], [0.2, 0.8]], index=['T', 'F'], columns=['rain', '-rain'])
        # Rain.parent1 = Cloud
        Rain.__name__ = 'Rain'
        Wet_Grass = pd.DataFrame([[0.99, 0.01], [0.9, 0.1], [0.9, 0.1], [0, 1]], index=['T,T', 'T,F', 'F,T', 
        'F,F'], columns=['wet', '-wet'])
        # Wet_Grass.parent1 = Sprinkler
        # Wet_Grass.parent2 = Rain
        Wet_Grass.__name__ = 'Wet_Grass'
        self.Cloud = Cloud
        self.Sprinkler = Sprinkler
        self.Rain = Rain
        self.Wet_Grass = Wet_Grass

    def Question_A(self):
        q1 = "P(C|-s,r)"
        q1_c_true = self.Cloud.loc['T', 'Cloud'] * self.Sprinkler.loc['T', '-sprinkler'] * self.Rain.loc['T', 'rain']
        q1_c_false = self.Cloud.loc['F', 'Cloud'] * self.Sprinkler.loc['F', '-sprinkler'] * self.Rain.loc['F', 'rain']
        q1_alpha = 1 / (q1_c_true + q1_c_false)
        q1_c_true = q1_c_true * q1_alpha
        q1_c_false = q1_c_false * q1_alpha
        self.q1 = q1
        self.q1_c_ture = q1_c_true
        self.q1_c_false = q1_c_false

        q2 = "P(C|-s,-r)"
        q2_c_ture = self.Cloud.loc['T', 'Cloud'] * self.Sprinkler.loc['T', '-sprinkler'] * self.Rain.loc['T', '-rain']
        q2_c_false = self.Cloud.loc['F', 'Cloud'] * self.Sprinkler.loc['F', '-sprinkler'] * self.Rain.loc['F', '-rain']
        q2_alpha = 1 / (q2_c_ture + q2_c_false)
        q2_c_ture = q2_c_ture * q2_alpha
        q2_c_false = q2_c_false * q2_alpha
        self.q2 = q2
        self.q2_c_true = q2_c_ture
        self.q2_c_false = q2_c_false

        q3 = "P(R|c,-s,w)"
        q3_r_ture = self.Rain.loc['T', 'rain'] * self.Cloud.loc['T', 'Cloud'] * self.Sprinkler.loc['T', '-sprinkler'] * self.Wet_Grass.loc['F,T', 'wet']
        q3_r_false = self.Rain.loc['T', '-rain'] * self.Cloud.loc['T', 'Cloud'] * self.Sprinkler.loc['T', '-sprinkler'] * self.Wet_Grass.loc['F,F', 'wet']
        q3_alpha = 1 / (q3_r_ture + q3_r_false)
        q3_r_ture = q3_r_ture * q3_alpha
        q3_r_false = q3_r_false * q3_alpha
        self.q3 = q3
        self.q3_r_true = q3_r_ture
        self.q3_r_false = q3_r_false

        q4 = "P(R|-c,-s,w)"
        q4_r_true = self.Rain.loc['F', 'rain'] * self.Cloud.loc['F', 'Cloud'] * self.Sprinkler.loc['F', '-sprinkler'] * self.Wet_Grass.loc['F,T', 'wet']
        q4_r_false = self.Rain.loc['F', '-rain'] * self.Cloud.loc['F', 'Cloud'] * self.Sprinkler.loc['F', '-sprinkler'] * self.Wet_Grass.loc['F,F', 'wet']
        q4_alpha = 1/(q4_r_true + q4_r_false)
        q4_r_true = q4_r_true * q4_alpha
        q4_r_false = q4_r_false * q4_alpha
        self.q4 = q4
        self.q4_r_true = q4_r_true
        self.q4_r_false = q4_r_false

        print("Part A. The sampling probabilities")
        print("P(C|-s,r) = <" + str(self.q1_c_ture) + ", " + str(self.q1_c_false) + ">")
        print("P(C|-s,-r) = <" + str(self.q2_c_true) + ", " + str(self.q2_c_false) + ">")
        print("P(R|c,-s,w) = <" + str(self.q3_r_true) + ", " + str(self.q3_r_false) + ">")
        print("P(R|-c,-s,w) = <" + str(self.q4_r_true) + ", " + str(self.q4_r_false) + ">")

    def Question_B(self):
        #half chance to choose c or r
        #q2_c_false = p(-c|-s,-r) q4_r_false = p(-r|-c,-s,w)
        state1_to_state1 = 0.5 * self.q2_c_false + 0.5 * self.q4_r_false
        #no chance when choose c, q4_r_true = p(r|-c,-s,w)
        state1_to_state2 = 0.5 * 0 + 0.5 * self.q4_r_true
        #q2_c_true = p(c|-s,-r), no chance when choose r
        state1_to_state3 = 0.5 * self.q2_c_true + 0.5 * 0
        #no chance for choose either c or r
        state1_to_state4 = 0

        #no chance when choose c, 
        state2_to_state1 = 0.5 * 0 + 0.5 * self.q4_r_false
        state2_to_state2 = 0.5 * self.q1_c_false + 0.5 * self.q4_r_true
        state2_to_state3 = 0
        state2_tostate4 = 0.5 * self.q1_c_ture + 0

        state3_to_state1 = 0.5 * self.q2_c_false + 0
        state3_to_state2 = 0
        state3_to_state3 = 0.5 * self.q2_c_true + 0.5 * self.q3_r_false
        state3_to_state4 = 0 + 0.5 * self.q3_r_true

        state4_to_state1 = 0
        state4_to_state2 = 0.5 * self.q1_c_false + 0
        state4_to_state3 = 0 + 0.5 * self.q3_r_false
        state4_to_state4 = 0.5 * self.q1_c_ture + 0.5 * self.q3_r_true
        P_table = pd.DataFrame([[state1_to_state1, state1_to_state2, state1_to_state3, state1_to_state4], 
        [state2_to_state1, state2_to_state2, state2_to_state3, state2_tostate4], 
        [state3_to_state1, state3_to_state2, state3_to_state3, state3_to_state4],
        [state4_to_state1, state4_to_state2, state4_to_state3, state4_to_state4]], index=['S1', 'S2', 'S3', 'S4'],
        columns=['S1', 'S2', 'S3', 'S4'])
        self.P_table = P_table
        print('\nPart B. The transition probability matrix')
        print(P_table)

    def Question_C(self):
        C_true = 0
        C_flase = 0
        initial = random.randint(1, 4)
        initial_state = 'S' + str(initial)
        if(initial == 1 or initial == 2):
            C_flase += 1
        else:
            C_true += 1
        for i in range(999998):
            temp = self.P_table[self.P_table.index == initial_state]
            temp2 = temp.values
            temp2 = temp2.ravel()
            next_s = numpy.random.choice(4, 1, p=temp2)
            next_state = 1 + next_s[0]
            if(next_state == 1 or  next_state == 2):
                C_flase += 1
            else:
                C_true += 1
            initial_state = 'S' + str(next_state)
            
        print('\nPart C. P(C|-s,w) = <' + str(C_true/1000000) + ', ' + str(C_flase/1000000) + '>')

if __name__ == "__main__":
    test = Gibbs()
    test.create_data_set()
    test.Question_A()
    test.Question_B()
    test.Question_C()
