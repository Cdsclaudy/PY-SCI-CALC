""" WELCOME TO THE SOURCE CODE OF THE PROGRAM """

""" EACH MODULE USED BELOW SERVES A UNIQUE PURPOSE IN THE PROGRAM.
    HOWEVER THE MATH MODULE SERVES THE MOST IMPORTANT PURPOSE. """
from tkinter import *
from math import *
from tkinter import messagebox

#________________________BASIC_GUI_BLOCK______________________________________________________________________________

""" THE GUI BLOCK BELOW FORMS THE FOUNDATION OF THE INTERFACE WINDOW """

root=Tk()
root.title("PY-SCI-CALC")
root.geometry("818x602")
root.configure(background="#666664")
root.resizable(width=False,height=False)
calcu=Frame(root)
calcu.grid()

#________________________MAIN_OPERATIONAL_BLOCK________________________________________________________________________

""" THE class Calculation ENCAPSULATES ALL THE MAJOR FUNCTIONS OF THE CALCULATOR. """

class Calculation():
    
    #CONSTRUCTOR
    def __init__(self):
        
        #CLASS VARIABLES
        self.total=0            #Variable used to store total(result)
        self.mainlist=[0]       #List used to store the expression entered by the user
        self.position=0         #Variable used to store the current position of the end of list
        self.s=""               #Variable used to store the final simplified expression for evaluation

    #____________________NUMBER_BUTTON_BLOCK___________________________________________________________________________
    """ THIS BLOCK ENCOUNTERS ALL FUNCTION CALLS FROM THE NUMERICAL BUTTONS. """
    
    def numbers(self,num):

        #DISPLAY CALL BLOCK
        if(self.position!=0 and self.mainlist[self.position]==")"):
            self.mainlist.append("*")
            self.position+=1
        #MISCELLANEOUS CASE
        if(DisplayBox.get() in ["SYNTAX ERROR","MATH ERROR"]):
            self.clearall()
            self.display(str(num))
        else:
            #CASE 1: WHEN THE LIST ELEMENT AT HAND ENDS WITH A DECIMAL POINT
            if("." in str(self.mainlist[self.position])):
                self.display(DisplayBox.get()+str(num))
                self.mainlist[self.position]=str(self.mainlist[self.position])+str(num)
                return

            #CASE 2: WHEN THE CURRENT LIST ELEMENT IS NOT ZERO  
            if(self.mainlist[self.position]!=0 and DisplayBox.get() not in "0.0"):
                self.display(DisplayBox.get()+str(num))
    
            #CASE 3: WHEN THE CURRENT DISPLAY BOX DISPLAYS ZERO, ANY NUMBER ENTERED SHOULD OVERWRITE IT
            else:
                self.display(str(num))   

        #LIST UPDATE BLOCK
        # SPECIAL CASE 1: WHEN THE CURRENT VARIABLE AT HAND IS e OR pi, A '*' OPERATOR MUST BE APPENDED TO AVOID AN EVAL ERROR
        if(self.mainlist[self.position]==e or self.mainlist[self.position]==pi):
            self.mainlist.append("*")
            self.mainlist.append(str(num))
            self.position+=2
            return
        
        # SPECIAL CASE 2: WHEN THE CURRENT LIST ELEMENT IS JUST A ZERO IT NEEDS TO BE OVERWRITTEN BY THE NUMBER THAT HAS BEEN INPUT
        if(self.mainlist==[0]):
            self.mainlist[self.position]=str(num)
            return

        # REAL CASE 1: WHEN THE CURRENT LIST ELEMENT IS AN INT OR FLOAT TYPE THEN WE MUST APPEND TO THE CURRENT ELEMENT
        if(str(self.mainlist[self.position]).isdigit() or str(self.mainlist[self.position]).endswith(".")):
            self.mainlist[self.position]=str(self.mainlist[self.position])+str(num)

        # REAL CASE 2: WHEN THE CURRENT LIST ELEMENT IS NOT A NUMBER THE CURRENT NUMBER MUST BE APPENDED TO THE LIST WITH UPDATE IN THE POSITION    
        else:
            self.position+=1
            self.mainlist.append(str(num))

    #_____________________DECIMAL_POINT_BLOCK__________________________________________________________________________
    """ THIS BLOCKS HANDLES ALL ISSUES RELATED TO THE "." BUTTON. """
    
    def point(self):
        #ERROR DISPLAY HANDLER
        if(DisplayBox.get() in ["SYNTAX ERROR","MATH ERROR"]):
            self.clearall()
        # APPENDING THE DECIMAL POINT TO THE DISPLAY
        self.display(DisplayBox.get()+".")

        # CASE 1: IF THE DECIMAL POINT IS CALLED PRECEEDED BY NO NUMBER "." CONVERTS TO "0." AND NEEDS TO BE APPENDED
        if(self.mainlist and (str(self.mainlist[self.position])[0].isdigit()==False)):
            self.mainlist.append("0.")
            self.position+=1
            return

        # CASE 2: IF THE DECIMAL POINT IS CALLED BUT PRECEEDED BY A NUMBER THE POINT IS ONLY TO BE APPENDED TO THE NUMBER
        else:
            self.mainlist[self.position]=str(self.mainlist[self.position])+"."

    #____________________ARITHMETIC_OPERATION_BLOCK_____________________________________________________________________
        
    def operation(self,fn):
        if(DisplayBox.get() in ["SYNTAX ERROR","MATH ERROR","Inf"]):
            self.clearall()
        # SPECIAL CASE: WHEN THE BUTTON PRESSED IS 'e' or'pi'(π)
        if(fn=="e" or fn=="π"):

            #CASE 1: WHEN THE CURRENT LIST ELEMENT IS NOT A ZERO, THE VALUE HAS TO BE APPENDED, UPDATING POSITION
            if(self.mainlist[self.position]!=0):
                self.display(DisplayBox.get()+fn)
                self.minorcalcs()
                if(fn=="e"):
                    self.mainlist.append(e)
                elif(fn=="π"):
                    self.mainlist.append(pi)
                self.position+=1

            #CASE 2: WHEN THE CURRENT LIST ELEMENT IS A ZERO, THE VALUE HAS TO BE OVERRIDDEN TO AVOID ERRORS   
            else:
                self.display(fn)
                if(fn=="e"):
                    self.mainlist=[e]
                elif(fn=="π"):
                    self.mainlist=[pi]
            return
        # CASE 1: WHEN THE CURRENT LIST ELEMENT IS NOT 'e' OR 'pi' AND IS NOT ZERO THE VARIABLE WILL HAVE TO BE APPENDED
        if(self.mainlist[self.position]!=0 and DisplayBox.get()!="0.0"):
            self.display(DisplayBox.get()+fn)
            if(fn not in ["+","-","/","*",")","^"]):
                self.minorcalcs()
            self.mainlist.append(fn)
            self.position+=1

        # CASE 2: WHEN THE CURRENT LSIT ELEMENT IS A ZERO, THE ZERO HAS TO BE OVERRIDEN TO AVOID AN ERROR
        else:
            self.display(fn)
            self.mainlist=[fn]

    #_____________________RESULT_BLOCK__________________________________________________________________________________
    """ THIS BLOCK IS ACCESSED WHEN THE EQUAL TO BLOCK IS TRIGGERED. """
    
    def final(self,exp):
        # LOOPING THROUGH THE ENTIRE LIST AND APPENDING TO THE CLASS VARIABLE STRING s FOR EVALUATION
        k="" #k CHECKS IF EXTRA BRACKETS ARE REQUIRED
        for i in exp:
            # CASE 1: SINCE sin AND A FEW OTHER FUNCTIONS CALCULATE IN RADIANS, THE VALUE ENTERED IN DEGREES MUST BE CONVERTED TO RADIANS AND THEN PASSED
            if(i in ["tan(","sin(","cos(","sinh(","cosh(","tanh("]):
                self.s+=str(i)+"radians("
                k+="a"
                continue
            
            # CASE 2: SINCE asin AND A FEW OTHER FUNCTIONS OUTPUT IN RADIANS, THE VALUE IN THE OUTPUT MUST BE CONVERTED TO DEGREES
            elif(i in ["atan(","asin(","acos("]):
                k+="a"
                self.s+="degrees("+str(i)

            # CASE 3: CURRENT CASE IS A COMBINATION OF CASE 1 AND 2
            elif(i in ["atanh(","asinh(","acosh("]):
                k+="A"
                self.s+="degrees("+str(i)+"radians("

            # CASE 4: CURRENT CASE IS "ln(" THE EQUIVALENT IS "log("
            elif(i=="ln("):
                self.s+="log("

            # CASE 5: CURRENT CASE IS "log(" THE EQUIVALENT IS "log10("    
            elif(i=="log("):
                self.s+="log10("

            # CASE 6: CURRENT CASE IS "√(" THE EQUIVALENT IS "sqrt("     
            elif(i=="√("):
                self.s+="sqrt("

            # CASE 7: CURRENT CASE IS "ANS" THE EQUIVALENT IS THE PREVIOUS OUTPUT    
            elif(i=="ANS"):
                self.s+=str(self.total)

            # CASE 8: CURRENT CASE IS "^" THE EQUIVALENT IS "**" FOR POWER
            elif(i=="^"):
                self.s+="**"
            elif(i=="Inv("):
                self.s+="1/("

            # CASE 9: LAST CASE INCLUDES ALL KINDS OF NUMBERS
            else:
                self.s+=str(i)
            if(i==")" and k and k[-1]=='A'):
                self.s+="))"
                k=k[:-1]
                continue
            if(i==")" and k):
                self.s+=")"
                k=k[:-1]
                
        # HANDLING BRACKET ERROR
        self.s+=(")"*(self.s.count("(")-self.s.count(")")))
        if(self.s.count("(")!=self.s.count(")")):
            self.display("SYNTAX ERROR")
            return

        # HANDLING COMMON SYNTAX ERRORS
        s={"+","-","*","/","^"}
        st={str(x)+str(y) for x in s for y in s}
        for i in st:
            if i!="**" and i in self.s:
                self.display("SYNTAX ERROR")
                return
            
        # HANDLING MATH ERRORS ON EVALUATION
        try:
            self.total=eval(self.s)
        except:
            self.display("MATH ERROR")
            return
        
        # HANDLING INFINITY CASE FOR TRIGONOMETRIC FUNCTIONS AND DISPLAY IT   
        if str(self.total)!='0' or str(self.total)!='0.0':
            if (("sin" in self.s) or ("cos" in self.s) or ("tan" in self.s)):
                if(self.total>=10e+14):
                    self.display("MATH ERROR")
                    self.total=0
                else:
                    self.display(round(self.total,15))
            else:
                self.display(round(self.total,15))
        else:
            self.display(0)
        self.mainlist=[self.total]
        if(DisplayBox.get()=="0.0"):
            self.mainlist=[0]
        # UPDATING THE MAINLIST WHEN FINAL ANSWER IS ZERO 
        if(DisplayBox.get()=="0"):
            self.mainlist=[0]
        self.s=""
        self.position=0

    #_____________________MINOR_ERROR_HANDLER_BLOCK____________________________________________________________________

    def minorcalcs(self):
        # CASE TO CORRECT ERRORS CAUSED BY e AND pi
        if self.mainlist and str(self.mainlist[-1])[0].isdigit():
            self.mainlist.append("*")
            self.position+=1

    #_____________________SIMPLE_CLEAR_BLOCK___________________________________________________________________________
        
    def clear(self):
        if(DisplayBox.get()=="0"):
            return
        if((DisplayBox.get().isdigit() and len(DisplayBox.get())==1) or (len(self.mainlist)==1 and DisplayBox.get()[0].isdigit()==False)):
            self.clearall()
            return
        if(len(str(self.mainlist[self.position]))==1):
            self.mainlist=self.mainlist[:-1]
            self.position-=1
            self.display(DisplayBox.get()[:-1])
            return
            
        # CASE 1: WHEN A DOUBLE NUMBER IS ALREADY PRESENT AT CURRENT POSITION 
        if(str(self.mainlist[self.position])[0].isdigit()):
            self.mainlist[self.position]=str(self.mainlist[self.position])[:-1]
            self.display(DisplayBox.get()[:-1])

        # CASE 2: WHEN A NON NUMBER OR SINGLE NUMBER IS PRESENT
        else:
            self.display(DisplayBox.get()[:len(DisplayBox.get())-len(self.mainlist[-1])])
            self.mainlist=self.mainlist[:self.position]
            self.position-=1

    #_____________________COMPLETE_CLEAR_BLOCK__________________________________________________________________________
    # THIS BLOCK CLEARS THE ENTIRE DISPLAY BOX AND RESETS VARIABLES
    
    def clearall(self):
        self.display(0)
        self.position=0
        self.mainlist=[0]
        self.s=""

    #_____________________DISPLAY_BLOCK__________________________________________________________________________________
    # THIS BLOCK HANDLES THE ENTIRE DISPLAY
    
    def display(self,var):
        DisplayBox.delete(0,END)
        DisplayBox.insert(0,var)
        #print(self.mainlist)
        #print(self.s)

lin=Calculation()

#_________________________BUTTON_EMBED_BLOCK_____________________________________________________________________________
# DISPLAY BOX(ENTRY BOX)CREATION
DisplayBox=Entry(calcu,relief=SUNKEN,font=('Verdana',18),bd=30,width=30,bg="black",fg="white",justify=RIGHT)
DisplayBox.grid(row=0,column=0,columnspan=5,sticky="NSEW")
DisplayBox.insert(0,"0")
    #BREAKING THE KEYBOARD INPUT TO AVOID ERRORS
DisplayBox.bind("<Key>",lambda e:"break")

# EMBEDDING NUMBER BUTTONS
numberpad = "789456123"
i=0
btn=[]
C=Button(calcu, width=2,command=lambda: lin.clear(),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="C").grid(row=1,column=0,pady=1,padx=1,sticky="NSEW")
CE=Button(calcu, width=2,command=lambda: lin.clearall(), height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="CE").grid(row=1,column=1,pady=1,padx=1,sticky="NSEW")
for j in range(2,5):
    for k in range(3):
        btn.append(Button(calcu,command=lambda x=str(numberpad[i]): lin.numbers(x)
        , width=2, height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text=numberpad[i]))
        btn[i].grid(row=j, column=k,sticky="NSEW",pady=1,padx=1)
        i+=1

# MATHEMATICAL FUNCTION BUTTON EMBED
Z=Button(calcu, width=2, command=lambda x="0":lin.numbers(x), height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="0").grid(row=5,column=1,pady=1,padx=1,sticky="NSEW")
dote=Button(calcu, width=2, command=lambda: lin.point(),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text=".").grid(row=5,column=0,pady=1,padx=1,sticky="NSEW")
inv=Button(calcu, width=2, command=lambda: lin.operation("Inv("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="Inv(").grid(row=4,column=7,pady=1,padx=1,sticky="NSEW")

equal=Button(calcu, width=2, command=lambda: lin.final(lin.mainlist),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="=").grid(row=5,column=7,pady=1,padx=1,sticky="NSEW")
plus=Button(calcu, width=2, command=lambda: lin.operation("+"),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="+").grid(row=1,column=3,pady=1,padx=1,sticky="NSEW")
minus=Button(calcu, width=2, command=lambda: lin.operation("-"),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="-").grid(row=2,column=3,pady=1,padx=1,sticky="NSEW")
multi=Button(calcu, width=2, command=lambda: lin.operation("*"),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="*").grid(row=3,column=3,pady=1,padx=1,sticky="NSEW")
divide=Button(calcu, width=2, command=lambda: lin.operation("/"),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="÷").grid(row=4,column=3,pady=1,padx=1,sticky="NSEW")
ans=Button(calcu, width=2, command=lambda: lin.operation("ANS"),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="ANS").grid(row=5,column=3,pady=1,padx=1,sticky="NSEW")
sqroot=Button(calcu, width=2, command=lambda: lin.operation("√("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="√").grid(row=1,column=2,pady=1,padx=1,sticky="NSEW")
sine=Button(calcu, width=2, command=lambda: lin.operation("sin("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="sin").grid(row=1,column=4,pady=1,padx=1,sticky="NSEW")
cosi=Button(calcu, width=2, command=lambda: lin.operation("cos("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="cos").grid(row=2,column=4,pady=1,padx=1,sticky="NSEW")
tane=Button(calcu, width=2, command=lambda: lin.operation("tan("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="tan").grid(row=3,column=4,pady=1,padx=1,sticky="NSEW")
loga=Button(calcu, width=2, command=lambda: lin.operation("log("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="log").grid(row=4,column=4,pady=1,padx=1,sticky="NSEW")
asine=Button(calcu, width=2, command=lambda: lin.operation("asin("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="asin").grid(row=1,column=5,pady=1,padx=1,sticky="NSEW")
acosi=Button(calcu, width=2, command=lambda: lin.operation("acos("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="acos").grid(row=2,column=5,pady=1,padx=1,sticky="NSEW")
atane=Button(calcu, width=2, command=lambda: lin.operation("atan("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="atan").grid(row=3,column=5,pady=1,padx=1,sticky="NSEW")
asine=Button(calcu, width=2, command=lambda: lin.operation("sinh("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="sinh").grid(row=1,column=6,pady=1,padx=1,sticky="NSEW")
acose=Button(calcu, width=2, command=lambda: lin.operation("cosh("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="cosh").grid(row=2,column=6,pady=1,padx=1,sticky="NSEW")
atane=Button(calcu, width=2, command=lambda: lin.operation("tanh("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="tanh").grid(row=3,column=6,pady=1,padx=1,sticky="NSEW")
asineh=Button(calcu, width=2, command=lambda: lin.operation("asinh("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="asinh").grid(row=1,column=7,pady=1,padx=1,sticky="NSEW")
acoseh=Button(calcu, width=2, command=lambda: lin.operation("acosh("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="acosh").grid(row=2,column=7,pady=1,padx=1,sticky="NSEW")
ataneh=Button(calcu, width=2, command=lambda: lin.operation("atanh("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="atanh").grid(row=3,column=7,pady=1,padx=1,sticky="NSEW")
lone=Button(calcu, width=2, command=lambda: lin.operation("ln("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="ln").grid(row=4,column=5,pady=1,padx=1,sticky="NSEW")
powe=Button(calcu, width=2, command=lambda: lin.operation("^"),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="^").grid(row=5,column=2,pady=1,padx=1,sticky="NSEW")
ee=Button(calcu, width=2, command=lambda: lin.operation("e"),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="e").grid(row=5,column=4,pady=1,padx=1,sticky="NSEW")
ee=Button(calcu, width=2, command=lambda: lin.operation("π"),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="π").grid(row=5,column=5,pady=1,padx=1,sticky="NSEW")
br1=Button(calcu, width=2, command=lambda: lin.operation("("),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text="(").grid(row=4,column=6,pady=1,padx=1,sticky="NSEW")
br1=Button(calcu, width=2, command=lambda: lin.operation(")"),height=2,bd=12,font=('Verdana',18),fg="white",bg="black", text=")").grid(row=5,column=6,pady=1,padx=1,sticky="NSEW")

# LABEL EMBED
lblDisplay=Label(calcu, text="Scientific Calculator", font=('Verdana',20,'bold'), justify =CENTER)
lblDisplay.grid(row=0, column=5,columnspan=3)

#______________________________MISCELLANEOUS_BLOCK_____________________________________________________________________

def Exiting():
    Exiting = messagebox.askyesno("Scientific Calculator", "Confirm if you want to exit")
    if Exiting>0:
        root.destroy() #USED TO QUIT THE PROGRAM
        return
    
# EXTERNAL ABOUT WINDOW
def About():
    ab=Tk()
    ab.title("About")
    a=Label(ab,font=('Verdana',18),text="This project was created by Claudius D'souza")
    a.pack()

# MENUBAR CREATION AND EMBED
menubar = Menu(calcu)
filemenu = Menu(menubar, tearoff=0)
# CASCADE: MENU LABEL
menubar.add_cascade(label = "File", menu=filemenu)

# COMMAND: SUB MENU LABEL
filemenu.add_command(label = "About", command = About)
filemenu.add_command(label = "Exit", command = Exiting)
root.config(menu=menubar)
#_______________________________________________________________________________________________________________________

root.mainloop()
