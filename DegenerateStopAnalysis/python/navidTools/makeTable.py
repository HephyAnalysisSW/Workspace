import pickle
import jinja2
import numpy as np
import glob

texDir="./tex/"
pdfDir="/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions/tables/"
pklDir="./pkl/dmt_regions/*.pkl"
#templateLoader = jinja2.FileSystemLoader( searchpath="./LaTexJinjaTemplates" )
#templateEnv = jinja2.Environment( 
#                  "%<", ">%",
#                  "<<", ">>",
#                  "<#", "",
#
#                  #block_start_string = '\BLOCK{',
#                  #block_end_string = '}',
#                  #variable_start_string = '\VAR{',
#                  #variable_end_string = '}',
#                  #comment_start_string = '\#{',
#                  #comment_end_string = '}',
#                  #line_statement_prefix = '%-',
#                  #line_comment_prefix = '%#',
#                  #trim_blocks = True,
#                  #autoescape = False,
#
#
#                  loader=templateLoader )
#template_file = "latexTemplate.j2.tex"
#texTemplate = templateEnv.get_template( template_file )





#outputName = yields.tableName+".tex"


def fix(x):
    return x.replace("_","-").replace("+-","$\pm$").replace("-+","$\mp$").replace(">","$>$")

def fixForLatex(x):
  if type(x)==type(""):
    return fix(x)
  if type(x) in [ type([]) ] : 
    return [fix(ix) for ix in x]
  if type(x) in [ type(np.array([])) ]:
    return np.array( [fix(ix) for ix in x] )




import os


templateDir = "/afs/hephy.at/user/n/nrad/CMSSW/fork/CMSSW_7_4_12_patch4/src/Workspace/DegenerateStopAnalysis/python/navidTools/LaTexJinjaTemplates/"

class JinjaTexTable():
  def __init__(self,yieldInstance, FOM=True, texDir="./tex/", pdfDir=pdfDir, outputName="",\
                              searchpath=templateDir, template_file= "", removeJunk=False, tableNum=1, caption=""):
    self.searchpath = searchpath

    if template_file:
      self.template_file = template_file 
    elif FOM:
      self.template_file = "LaTexTemplateWithFOM.j2.tex"
    else:
      sel.template_file = "LaTexTemplateWith.j2.tex"
    self.yields = yieldInstance
    if not outputName:
      self.outputName = self.yields.tableName+".tex"
    else: self.outputName = outputName
    self.pdfDir = pdfDir
    self.texDir = texDir
    #yieldDict ={
    #      "y": self.yields,
    #      "table":self.yields.table.T,
    #      "yields":self.yields.yields.T,
    #      "colLegend" : [ x[0] for x in yields.table[1:] ],
    #      "rowLegend" : [x for x in yields.table[0][1:]],
    #      }
    templateLoader = jinja2.FileSystemLoader( searchpath=self.searchpath )
    self.templateEnv = jinja2.Environment( 
                      "%<", ">%",
                      "<<", ">>",
                      "<#", "",
                      #block_start_string = '\BLOCK{',
                      #block_end_string = '}',
                      #variable_start_string = '\VAR{',
                      #variable_end_string = '}',
                      #comment_start_string = '\#{',
                      #comment_end_string = '}',
                      #line_statement_prefix = '%-',
                      #line_comment_prefix = '%#',
                      #trim_blocks = True,
                      #autoescape = False,
                      loader=templateLoader )
    self.templateEnv.filters['fixForLatex']=fixForLatex

    texTemplate = self.templateEnv.get_template( self.template_file )

    
    self.fout=open(texDir+self.outputName,"w")
    self.out = texTemplate.render( yields=self.yields, yieldTable=self.yields.FOMTable.T, TAB=tableNum, CAPTION=caption)
    print(self.out)
    self.fout.write( self.out)
    self.fout.close()
    print "LaTex File:", texDir+self.outputName

    os.system("pdflatex -output-directory=%s %s"%(self.pdfDir,self.texDir+self.outputName))
    if removeJunk:
      out = pdfDir+self.outputName
      print "output:", out
      os.system("rm %s"%out.replace(".tex","aux"))      
      os.system("rm %s"%out.replace(".tex","log"))      




if __name__=='__main__':
  pklfiles = glob.glob(pklDir)
  for pklfile in pklfiles:
    yields = pickle.load(open(pklfile,"rb"))
    j=JinjaTexTable(yields)


