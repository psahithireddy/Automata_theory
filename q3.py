import sys
import json 

class dfa_to_gnfa:

    def __init__(self,states,letters,transition,start_states,final_states):
        self.allstates=[]
        self.transition=transition  
        self.startstates=self.get_startstates(start_states)
        self.final_states=self.get_finalstates(final_states)
        self.letters=letters
        self.all_states(states)
        #self.main_transition(self.allstates,transition,start_states,final_states)
        #self.prints()

    #converting startstates
    def get_startstates(self,start_states):
        start_arr=[]
        statenew="Qs"
        self.allstates.append(statenew)
        start_arr.append(statenew)
        for st in start_states:
            self.transition.append([statenew,"$",st])
        return start_arr

    #converting final states
    def get_finalstates(self,final_states):
        final_arr=[]
        state_acc="Qa"
        self.allstates.append(state_acc)
        final_arr.append(state_acc)
        for st in final_states:
            self.transition.append([st,"$",state_acc])
        return final_arr

    def all_states(self,states):
        for i in states:
            if len(i)==0:
                #self.allstates.append(["Qp"])
                pass
            else:    
                self.allstates.append(i)



    # def main_transition(self,states,transition,start_states,final_states):
    #     for st1 in states:
    #         for st2 in states:
    #             f=0
    #             for t in transition:
    #                 if t[0]==st1 and t[2]==st2:
    #                     #print("found")
    #                     self.transition.append(t)
    #                     f=1
    #             if f==0:
    #                 if (st1=="Qs" and st2 in start_states) or (st2=="Qa" and st1 in final_states):
    #                     continue
    #                 else:
    #                     if (st1=="Qs" and st2=="Qs") or (st1=="Qa" and st2=="Qa"):
    #                         continue
    #                     else:
    #                         self.transition.append([st1,"@",st2]) #@ is phi       

    # def prints(self): #need to return all 5 elements
    #     print(self.allstates)
    #     for i in self.transition:
    #         print(i)

def trans(a,b,arr):
    temp=[]
    for tu in arr:
        if a==tu[0] and b==tu[2]:
            temp.append(tu[1])
    if len(temp)==1:
        return temp[0]
    elif len(temp)==0:    
        return '@'
    else:
        exp="("+temp[0]
        for i in range(1,len(temp)):
            exp+="+"+ temp[i]
        exp+=")"    
        return exp

def delete(states,qrip):
    return states[:-1]


def makexp(R1,R2,R3,R4):
    if R1!="@":
        if len(R1)!=1:
            R1="("+ R1 +")"
    if R2!="@":
        if len(R2)!=1:
            R2="("+ R2 +")"
    if R3!="@":
        if len(R3)!=1:
            R3="("+ R3 +")" 
    R=""
    if R1=="@" or R3=="@":
        R="@" 
    else:
        if R2=="@":
            R2="$"
            R=R1+R2+R3
        else:
            R=R1+R2+"*"+R3
    
    if R=="@" and R4!="@":
        return R4
    elif  (R4=="@" or R4=="$") and R!="@":
        return R
    elif R4=="@" and R=="@":
        return R
    else: 
        if len(R4)==1:
            return R+"+"+R4
        else:
            return R+"+"+"("+R4+")"
   
    #return expr




def gnfa_to_regex(states,letters,transition,start_states,final_states):
    #print("hi")
    k=len(states)
    #print(states)
    
    if k==2:
        #print("hey")
        exp=str(trans('Qs','Qa',transition))
        nedstring=exp
        temp= nedstring.strip("(,)")
        final=nedstring
        if len(temp)==1:
            final=temp
        out={
            "regex":final
        }
        with open (sys.argv[2],'w') as outfile:
            json.dump(out,outfile,indent=2)
        return 0
    else:
        transition_new=[]
        qrip=states[-1]
        #print(qrip)
        states=delete(states,qrip)
        #print(states)
        #print("i am dying ;-;", qrip)
        for st1 in states:   #not working we have $ problems and none typees ka bhi
            #print(st1)
            for st2 in states:
                if st2!=start_states and st1!=final_states:
                    R1=str(trans(st1,qrip,transition))
                    R2=str(trans(qrip,qrip,transition))
                    R3=str(trans(qrip,st2,transition))
                    R4=str(trans(st1,st2,transition))
                    #print(R1,R2,R3,R4)
                    # if st1=="Q4" and st2=="Q4" and qrip=="Q2":
                    #     print("i am" ,R1)
                    exp=makexp(R1,R2,R3,R4)
                    #exp= R1+R2+"*"+R3+"+"+R4
                    #print(exp)
                    transition_new.append([st1,exp,st2])
        #print(str(trans('Qs','Qa',transition_new)))
    #print(transition_new) 
    gnfa_to_regex(states,letters,transition_new,start_states,final_states)
    #print("transn            " ,str(trans(['Qs'],['Qa'],transition_new)))


if(len(sys.argv) == 3):      
    input_file = open(sys.argv[1],"r")    
    output_file = open(sys.argv[2],"w")
    file_obj = json.load(input_file)
    states = file_obj['states']
    #print(states)
    letters=file_obj['letters']
    transition=file_obj['transition_function']
    start_states=file_obj['start_states']
    final_states=file_obj['final_states']
    #print(transition)
    gnfa=dfa_to_gnfa(states,letters,transition,start_states,final_states)
    #gnfa.allstates.remove([])
    # print(gnfa.allstates)
    # print(gnfa.startstates)
    # print(gnfa.final_states)
    # for u in gnfa.transition:
    #     print(u)
    #GNFA APPROVED
    regex=gnfa_to_regex(gnfa.allstates,gnfa.letters,gnfa.transition,gnfa.startstates,gnfa.final_states)
    #print(regex)
#print(nfa)
else:
    print("Usage: python3 q3.py <inputfile> <outputfile>")
