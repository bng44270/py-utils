import re

def b64decode(s):
  b64map = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,"T":19,"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25,"a":26,"b":27,"c":28,"d":29,"e":30,"f":31,"g":32,"h":33,"i":34,"j":35,"k":36,"l":37,"m":38,"n":39,"o":40,"p":41,"q":42,"r":43,"s":44,"t":45,"u":46,"v":47,"w":48,"x":49,"y":50,"z":51,"0":52,"1":53,"2":54,"3":55,"4":56,"5":57,"6":58,"7":59,"8":60,"9":61,"+":62,"/":63}
  binstr = ""
  for c in s:
    binstr += re.sub(r'^0b','',bin(b64map[c])).rjust(6,"0")
  bytear = [binstr[i:i+8] for i in range(0,len(binstr),8)]
  return "".join([chr(int(a,2)) for a in bytear])

def b64encode(s):
  b64map = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']
  binar = "".join([re.sub(r'^0b','',bin(ord(a))).rjust(8,"0") for a in s])
  pad = (len(binar) % 6) ^ 6 if not len(binar) % 6 == 0 else 0
  binar += "".join(["0" for i in range(0,pad)])
  encstr = "".join([b64map[a] for a in [int(binar[i:i+6],2) for i in range(0,len(binar),6)]])
  return (encstr + "".join(["=" for i in range(0,int((pad ^ 6 if not pad == 0 else 0)/2))]))
