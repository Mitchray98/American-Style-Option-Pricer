import math


print("")
print("-----------------------------------")
print("")
n = input("Periods =  ")
print("")
s = input("Spot ($) =  ")
print("")
k = input("Strike ($) =  ")
print("")
r = input("Risk-Free Rate (%) =  ")
print("")
de = input("Dividend Yield (%) =  ")
print("")
sig = input("Volatility (%) =  ")
print("")
T = input("Time to Expiry (Years) =  ")
print("")
mode = input("Call or Put? : ")
print("")

n=int(n)
s=float(s)
k=float(k)
r=float(r)/100
de=float(de)/100
sig=float(sig)/100
T=float(T)
h=T/n



##n = 4
##
##s = float(68.04)
##k= float(67.50)
##r = float(0.018)
##de = float(0.0118)
##sig = float(0.2433)
##T = float(0.4740)
##h = float(T/n)
##
##mode="call"



u = math.exp((r-de)*h + sig*(h**(1/2)))
d = math.exp((r-de)*h - sig*(h**(1/2)))

p = (math.exp((r-de)*h) - d)/(u-d)

#Structure is tree -> periods -> nodes

def calls(n,s,k,r,de,sig,T,h,u,d,p):

    tree = []

    for j in range(n,-1,-1):
        period = []
        for i in range(0,j+1):
            node = []
            ud = [j-i,i]
            node.append(ud)

            st = s*(u**(ud[0]))*(d**(ud[1]))
            node.append(st)

            if j==n:
                
                Ce = max(st-k,0)
                Ca = max(st-k,0)
                node.append(None)
                node.append(None)
                node.append(Ce)
                node.append(Ca)
                
            else:
                
                bigd = math.exp(-1*de*h)*(tree[n-1-j][i][5] - tree[n-1-j][i+1][5])/(u*st - d*st)
                b = math.exp(-1*r*h)*(u*tree[n-1-j][i+1][5] - d*tree[n-1-j][i][5])/(u-d)
                Ce = math.exp(-1*r*h) * (p * tree[n-1-j][i][4] + (1-p)* tree[n-1-j][i+1][4])
                Ca = max(math.exp(-1*r*h) * (p * tree[n-1-j][i][5] + (1-p)* tree[n-1-j][i+1][5]), st-k)

                node.append(bigd)
                node.append(b)
                node.append(Ce)
                node.append(Ca)

            if Ca < st-k:
                node.append("Early")

            period.append(node)
        
        tree.append(period)

    return tree


def puts(n,s,k,r,de,sig,T,h,u,d,p):

    tree = []

    for j in range(n,-1,-1):
        period = []
        for i in range(0,j+1):
            node = []
            ud = [j-i,i]
            node.append(ud)

            st = s*(u**(ud[0]))*(d**(ud[1]))
            node.append(st)

            if j==n:
                
                Ce = max(k-st,0)
                Ca = max(k-st,0)
                node.append(None)
                node.append(None)
                node.append(Ce)
                node.append(Ca)
                
            else:
                
                bigd = math.exp(-1*de*h)*(tree[n-1-j][i][5] - tree[n-1-j][i+1][5])/(u*st - d*st)
                b = math.exp(-1*r*h)*(u*tree[n-1-j][i+1][5] - d*tree[n-1-j][i][5])/(u-d)
                Ce = math.exp(-1*r*h) * (p * tree[n-1-j][i][4] + (1-p)* tree[n-1-j][i+1][4])
                Ca = max(math.exp(-1*r*h) * (p * tree[n-1-j][i][5] + (1-p)* tree[n-1-j][i+1][5]), k-st)

                node.append(bigd)
                node.append(b)
                node.append(Ce)
                node.append(Ca)

                if Ca < k-st:
                    node.append("Early")


            period.append(node)
        
        tree.append(period)

    return tree

if mode.lower() == "call":
    tree = calls(n,s,k,r,de,sig,T,h,u,d,p)
elif mode.lower() == "put":
    tree = puts(n,s,k,r,de,sig,T,h,u,d,p)


Delta = tree[n][0][2]

Gamma = (tree[n-1][0][2]-tree[n-1][1][2])/(u*s - d*s)

Theta = ( tree[n-2][1][5] - tree[n][0][5] - Delta*(u*d*s - s) - 0.5*Gamma*(u*d*s - s)**2 ) /(2*h*365)

tree.reverse()

print("")
print("------------------------------")
print("")
print("Price: "+str(round(float(tree[0][0][5])*100)/100))
print("")
print("Δ: "+str(round(float(Delta)*10000)/10000))
print("Γ: "+str(round(float(Gamma)*10000)/10000))
print("Θ: "+str(round(float(Theta)*10000)/10000))
print("")
print("------------------------------")
print("")
print("")
input("Press ENTER to continue...")

        
