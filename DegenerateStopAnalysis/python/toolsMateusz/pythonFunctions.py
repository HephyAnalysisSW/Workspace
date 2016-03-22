#pythonFunctions.py

def combineSel(*a):
   if len(a) == 1:
      print "At least 2 arguments required for combineSel() function."
      return
   else:
      sel = ""
      for i in range(len(a)):
         if i == 0: sel = "(" + a[0] + ")"
         else: sel += " && (" + a[i] + ")"
   return sel

def combineSelList(a):
   if len(a) == 1:
      print "List of strings required as input."
      return
   else:
      sel = ""
      for i in range(len(a)):
         if i == 0: sel = "(" + a[0] + ")"
         else: sel += " && (" + a[i] + ")"
   return sel
