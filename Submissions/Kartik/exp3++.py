
import random
import math
T=0 # time horizon
# i have decided that standard deviation for stochastic arms is 0.1
class Arm :

    def __init__(self,starting_mean,gamma,armtype): #for adversial arm armtype=1 and for stochastic armtype =0
        self.startmean = starting_mean

        self.nt = 0 #number of times we have played that arm
        self.weight = 1 #weight of the arm
        self.gamma = gamma

        self.probab = 1/5
        self.loss = 0
        self.armtype = armtype


    def pull_arm(self):
        self.nt +=1
        if self.armtype ==1 :
            pull = random.uniform(self.startmean-0.2,self.startmean+0.2)
        elif self.armtype == 0 :
            pull = random.gauss(self.startmean,0.1)
        return pull

    # def arm1_epsilont(self,beta):
    #     self.epsilont = min(1/10,beta,arm1.gamma)

arm1 = Arm(0.4,0.5,1)
arm2 = Arm(0.3,0.5,1)
arm3 = Arm(0.5,0.3,1)
arm4 = Arm(0.3,0.2,0)
arm5 = Arm(0.4,0.4,0)

for i in range(100) :
    T +=1
    betat = 0.5*(math.sqrt(math.log(5,math.e)/(5*T)))
    arm1.epsilont = min(1/10,betat,arm1.gamma)
    arm2.epsilont = min(1 / 10, betat, arm2.gamma)
    arm3.epsilont = min(1 / 10, betat, arm3.gamma)
    arm4.epsilont = min(1 / 10, betat, arm4.gamma)
    arm5.epsilont = min(1 / 10, betat, arm5.gamma)
    sum_of_epsilon = arm1.epsilont+arm2.epsilont+arm3.epsilont+arm4.epsilont+arm5.epsilont
    total_weight = math.exp(-1*arm1.nt*arm1.loss)+math.exp(-1*arm2.nt*arm2.loss)+math.exp(-1*arm3.nt*arm3.loss)
    +math.exp(-1*arm4.nt*arm4.loss)+math.exp(-1*arm5.nt*arm5.loss)
    arm1.rhot= math.exp(-1*arm1.nt*arm1.loss)/total_weight
    arm2.rhot = math.exp(-1*arm2.nt*arm2.loss)/total_weight
    arm3.rhot = math.exp(-1*arm3.nt*arm3.loss)/total_weight
    arm4.rhot = math.exp(-1*arm4.nt*arm4.loss)/total_weight
    arm5.rhot = math.exp(-1*arm5.nt*arm5.loss)/total_weight
    arm1.rhotildat = (1-sum_of_epsilon)*arm1.rhot + arm1.epsilont
    arm2.rhotildat = (1 - sum_of_epsilon) * arm2.rhot + arm2.epsilont
    arm3.rhotildat = (1 - sum_of_epsilon) * arm3.rhot + arm3.epsilont
    arm4.rhotildat = (1 - sum_of_epsilon) * arm4.rhot + arm4.epsilont
    arm5.rhotildat = (1 - sum_of_epsilon) * arm5.rhot + arm5.epsilont
    choice = random.choices([1,2,3,4,5],[arm1.rhotildat,arm2.rhotildat,arm3.rhotildat,arm4.rhotildat,arm5.rhotildat])
    if choice[0]==1:
        arm1.loss+=(float(arm1.pull_arm())/arm1.rhotildat)

    if choice[0]==2:
        arm2.loss+=(float(arm2.pull_arm())/arm2.rhotildat)

    if choice[0]==3:
        arm3.loss+=(float(arm3.pull_arm())/arm3.rhotildat)


    if choice[0]==4:
        arm4.loss+=(float(arm4.pull_arm())/arm4.rhotildat)


    if choice[0]==5:
        arm5.loss+=(float(arm5.pull_arm())/arm5.rhotildat)

    print(f"we have chosen arm {choice[0]} ")




















