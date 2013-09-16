
# build the decision node with this function...
class DecisionNode() :

    def __init__( self, col=-1, value=None, results=None, tb=None, fb=None ):

        self.col = col # col index of the criteria
        self.value = value # value the column must match to get a true result
        self.results = results # stores a dictionary of results for this branch (None for all the things except for the branch)
        self.tb = tb # next node is result is true
        self.fb = fb # next node is result is false



def divideset( rows, column, value ):
    # divide a set on a specific column
    # A function that tells us if a row is in the first (true) group or second (false)
    
    # We only have numeric values...
    split_function = lambda row : row[ column ] < value

    # Divide the rows into two sets and return them
    set1 = [ row for row in rows if split_function( row ) ]
    set2 = [ row for row in rows if not split_function( row ) ]


    return ( set1, set2 )

def uniquecounts( rows ):
    # find all the different possible outcomes and return them as dictionary..
    # create counts of possible results

    results = {}
    for row in rows:
        # the result according the code is the last column
        r = row[ len(row)-1 ]
        if r not in results:results[r] = 0
        results[r] += 1
    return results


def entropy( rows ):
    # entropy ---> sum of p(x)log( p(x) ) across all different possible results
    # entropy is indicative of the amount of disorder in the data, higher entropy more uncertainity
    from math import log

    log2 = lambda x : log(x)/log(2) # entropy is to the base 2
    results = uniquecounts(rows)

    ent = 0.
    for r in results.keys():
        p = float(results[r])/len(rows)
        ent = ent - p*log2(p)
    return ent


def variance(rows):

    if len(rows) == 0: return 0
    data = [ float( row[ len(row)-1 ] ) for row in rows ]
    mean = sum(data)/len(data)
    varnce = sum( [ (d-mean)**2 for d in data ] )/len(data)

    return varnce

def buildTree( rows, scoref=variance ):
    import math

    if len(rows) == 0. : return DecisionNode()
    currentScore = scoref(rows)

    # initial setup
    bestGain = 0.
    bestCriteria = None
    bestSets = None

    columnCount = len(rows[0])-1
    for col in range( 0, columnCount ):
        # get list of different values in the current column
        # since we are using numeric data... we round off to the nearest 2.5 value
        columnValues = {}
        for row in rows:
            currVal = round( row[ col ]/2.5 )*2.5
            if math.isnan(currVal) :
                continue
            
            columnValues[ currVal ] = 1
        

        # Try dividing the rows up for each value in the column
        for value in columnValues.keys():
            ( set1, set2 ) = divideset( rows, col, value )

            #Information Gain
            p = float( len(set1) )/len(rows)
            gain = currentScore-p*scoref(set1)-(1-p)*scoref(set2)

            if gain > bestGain and len(set1) > 0 and len(set2) > 0:
                bestGain = gain
                bestCriteria = ( col,value )
                bestSets = ( set1, set2 )

    
    # create subbranches
    if bestGain > 0:
        trueBranch = buildTree( bestSets[0] )
        falseBranch = buildTree( bestSets[1] )
        return DecisionNode( col=bestCriteria[0], value=bestCriteria[1], tb=trueBranch, fb=falseBranch )
    else :
        return DecisionNode( results=uniquecounts(rows) )


def prune(tree, mingain):

    if tree.tb.results == None:
        prune(tree.tb, mingain)
    if tree.fb.results == None:
        prune(tree.fb, mingain)


    if tree.tb.results != None and tree.fb.results != None :
        tb,fb = [],[]
        for v,c in tree.tb.results.items():
            tb+=[[v]]*c
        for v,c in tree.fb.results.items():
            fb+=[[v]]*c

        delta=entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)

        if delta<mingain:
            tree.tb, tree.fb = None, None
            tree.results = uniquecounts( tb+fb )


def example():

    import numpy
    import math
    import gmstrm

    ob1 = gmstrm.StormPredict()
    rows = ob1.symAePredictor()

    # need to remove the 'nan' values
    arrNanVals = []
    for r in range(len(rows)):
        if math.isnan(sum(rows[r])) :
            arrNanVals.append(r)
    rows = numpy.delete(rows, numpy.s_[arrNanVals], axis=0)
    
    uniRes = uniquecounts(rows)
    print 'unique Results--', uniRes

    tree = buildTree(rows)
    prune( tree, 1. )

    # print the tree
    printtree(tree)
    drawtree(tree)




def printtree( tree, indent='' ):

    # check if a leaf node
    if tree.results != None:
        print str( tree.results )
    else:

        # print criteria
        if tree.col == 0 :
            colStr = 'Bz'
        if tree.col == 1 :
            colStr = 'Bt'
        if tree.col == 2 :
            colStr = 'pDyn'

        print str( colStr )+'<'+str( tree.value )+'? '

        # print the branches
        print indent+'T->', 
        printtree( tree.tb, indent+'  ' )
        print indent+'F->', 
        printtree( tree.fb, indent+'  ' )

def getwidth(tree):

    if tree.tb==None and tree.fb == None: return 1
    return getwidth( tree.tb ) + getwidth( tree.fb )

def getdepth(tree):
    
    if tree.tb==None and tree.fb == None: return 0    
    return max( getdepth( tree.tb ), getdepth( tree.fb ) ) + 1


def drawtree( tree, jpeg='plots/jpeg' ):
    from PIL import Image, ImageDraw

    w = getwidth(tree)*100
    h = getdepth(tree)*100 + 120

    img = Image.new( 'RGB', (w,h), (255,255,255) )
    draw=ImageDraw.Draw(img)

    drawnode(draw, tree, w/2, 20)
    img.save(jpeg,'JPEG')



def drawnode( draw, tree, x, y ):

    if tree.results == None:
        w1 = getwidth(tree.fb)*100
        w2 = getwidth(tree.tb)*100

        left = x - (w1+w2)/2
        right = x + (w1+w2)/2

        # print criteria
        if tree.col == 0 :
            colStr = 'Bz'
        if tree.col == 1 :
            colStr = 'Bt'
        if tree.col == 2 :
            colStr = 'pDyn'

        draw.text( (x-20,y-10), str(colStr)+'<'+str(tree.value), (0,0,0) )

        draw.line( ( x, y, left+w1/2, y+100 ), fill = ( 255, 0 , 0 ) )
        draw.line( ( x, y, right-w2/2, y+100 ), fill = ( 255, 0 , 0 ) )

        drawnode( draw, tree.fb, left+w1/2, y+100 )
        drawnode( draw, tree.tb, right-w2/2, y+100 )
    else:
        txt = '\n'.join( [ '%s:%d'%v for v in tree.results.items() ] )
        draw.text( (x-20, y), txt, (0,0,0) )