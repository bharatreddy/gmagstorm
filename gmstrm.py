class StormPredict(object):
    """ 
    Build a machine learning based storm predictor

    Author - Bharat Kunduri
    """

    import datetime
    import numpy

    def __init__( self, startTime=datetime.datetime(2012,1,1,0), endTime=datetime.datetime(2012,6,30,23) ):
        # set the start and end times to run the classification algorithm on
        self.sTime = startTime
        self.eTime = endTime


    def symHAeData( self, makeSctrPlt=False ):
        # Get the symH and Ae indices data for the given times
        import datetime
        import numpy
        import matplotlib.pyplot as plt

        import pydarn
        import gme



        #Read in AE Data...
        ae = gme.ind.readAe(self.sTime,self.eTime, res=1)
        aeDatArr = [ae[x].ae   for x in range(len(ae))]
        aeTimeArr = [ae[x].time   for x in range(len(ae))]
        aeDatArr = numpy.array( aeDatArr )
        aeTimeArr = numpy.array( aeTimeArr )
        del ae # we are doing this to save memory, these are huge numbers

        #Read in SymH, AsymH Data...
        symasy=gme.ind.symasy.readSymAsy(sTime=self.sTime, eTime=self.eTime, symh=None, symd=None, asyh=None, asyd=None)
        symhDatArr  = [symasy[x].symh for x in range(len(symasy))]
        asyhDatArr  = [symasy[x].asyh for x in range(len(symasy))]
        symTimeArr  = [symasy[x].time for x in range(len(symasy))]
        del symasy # we are doing this to save memory, these are huge numbers
        symhDatArr = numpy.array( symhDatArr )
        asyhDatArr = numpy.array( asyhDatArr )
        symTimeArr = numpy.array( symTimeArr )

        if makeSctrPlt :
            # Make a scatter plot of SymH Vs Ae
            fig = plt.figure(figsize = ( 11, 8.5 ) )
            ax = fig.add_subplot(111)
            ax.plot( aeDatArr, symhDatArr, '.' , markersize = 2)
            ax.plot( [0,3000], [-50,-50], color = 'r', linewidth=2)
            #ax.plot( [0,3000], [-30,-30], color = 'y', linestyle='--', linewidth=2)

            ax.plot( [1000,1000], [200,-200], color = 'r', linewidth=2)
            ax.plot( [500,500], [200,-200], color = 'y', linestyle='--', linewidth=2)
            plt.title('Scatter plot of SymH Vs Ae ', fontsize = 15 )
            plt.xlabel('Ae-index', fontsize = 15)
            plt.ylabel('SymH-index', fontsize = 15)

            fig.savefig('plots/symHae.pdf',orientation='portrait',format='pdf')
            fig.savefig('plots/symHae.jpeg',orientation='portrait',format='jpeg')
            ax.clear()

        return aeTimeArr, aeDatArr, symTimeArr, symhDatArr, asyhDatArr




    def omniData( self ):
        # Get the symH and Ae indices data for the given times
        import datetime
        import numpy
        import matplotlib.pyplot as plt

        import pydarn
        import gme
        import math



        #Read in OMNI Data...get bz, by and pdyn
        omn = gme.ind.readOmni(self.sTime,self.eTime, res=1)
        bzmDatArr = [omn[x].bzm   for x in range(len(omn))]
        bymDatArr = [omn[x].bym   for x in range(len(omn))]
        pDynDatArr = [omn[x].pDyn   for x in range(len(omn))]
        omnTimeArr = [omn[x].time   for x in range(len(omn))]

        btDatArr = []
        # since there are None values in bz and by we cant use direct numpy apps
        for bz, by in zip( bzmDatArr, bymDatArr ):
            if bz != None and by != None :
                btDatArr.append( math.sqrt( math.pow( bz,2 ) + math.pow( by,2 ) ) ) 
            else :
                btDatArr.append( None )

        bzmDatArr = numpy.array( bzmDatArr )
        bymDatArr = numpy.array( bymDatArr )
        pDynDatArr = numpy.array( pDynDatArr )
        btDatArr = numpy.array( btDatArr )
        omnTimeArr = numpy.array( omnTimeArr )

        bzmDatArr = numpy.float64( bzmDatArr )
        btDatArr = numpy.float64( btDatArr )
        pDynDatArr = numpy.float64( pDynDatArr )

        del omn, bymDatArr # we are doing this to save memory, these are huge numbers
        

        return bzmDatArr, btDatArr, pDynDatArr, omnTimeArr



    def symAePredictor( self, makeIndexPlt=False, makeOMNIndexPlt=False ):

        import datetime
        import numpy
        import matplotlib.pyplot as plt

        # get the data
        ( aeTimeArr, aeDatArr, symTimeArr, symhDatArr, asyhDatArr ) = self.symHAeData()

        # set the indexes according to the following criteria
        # SymH >-50 and AE <500, index: 1, quiet time no storm or substorm
        # SymH >-50 and 500<=AE<1000, index: 2, no storm but minor substorm
        # SymH >-50 and AE >=1000, index: 3, no storm but substorm
        # SymH <=-50 and AE <500, index: 4, storm but not substorm
        # SymH <=-50 and 500<=AE<1000, index: 5, storm and minor substorm
        # SymH <=-50 and AE >1000, index: 6, storm and substorm

        indexDatArr = []
        for a, s in zip( aeDatArr, symhDatArr ):
            if ( (s > -50.) and (a < 750.) ):
                indexDatArr.append(1.)
            elif ( (s > -50.) and (a >= 750.) ):
                indexDatArr.append(2.)
            elif ( (s <= -50.) ):
                indexDatArr.append(3.)
            else :
                print 'some issue', s, a


            # if ( (s > -50.) and (a < 500.) ):
            #     indexDatArr.append(1.)
            # elif ( (s > -50.) and (a >= 500. and a < 1000.) ):
            #     indexDatArr.append(2.)
            # elif ( (s > -50.) and (a >= 1000.) ):
            #     indexDatArr.append(3.)
            # elif ( (s <= -50.) and (a < 500.) ):
            #     indexDatArr.append(4.)
            # elif ( (s <= -50.) and (a >= 500. and a < 1000.) ):
            #     indexDatArr.append(5.)
            # elif ( (s <= -50.) and (a >= 1000.) ):
            #     indexDatArr.append(6.)
            # else :
            #     print 'some issue', s, a

        indexDatArr = numpy.array( indexDatArr )

        # make a scatter plot of symH, AE and index
        if makeIndexPlt :
            fig = plt.figure(figsize = ( 11, 8.5 ) )
            ax = fig.add_subplot(111)
            sc = plt.scatter( aeDatArr, symhDatArr, c=indexDatArr, s= indexDatArr*5. )
            plt.xlabel( 'AE-index', fontsize = 15 )
            plt.ylabel( 'SymH-index', fontsize = 15 )
            cbar = plt.colorbar( sc, ticks=[ 1., 2., 3., 4., 5., 6. ] )
            cbar.set_label( "Storm Index", size=15 )
            fig.savefig( 'plots/indexplot.pdf',orientation='portrait',format='pdf' )
            fig.savefig( 'plots/indexplot.jpeg',orientation='portrait',format='jpeg' )
            ax.clear()

                
        # make a scatter plot of symH, AE and index
        if makeOMNIndexPlt :
            fig = plt.figure(figsize = ( 11, 8.5 ) )
            ax = fig.add_subplot(111)
            sc = plt.scatter( bzmDatArr, pDynDatArr, c=indexDatArr, s= indexDatArr*5. )
            plt.xlabel( 'Bz-GSM [nT]', fontsize = 15 )
            plt.ylabel( 'pDyn [nPa]', fontsize = 15 )
            cbar = plt.colorbar( sc, ticks=[ 1., 2., 3., 4., 5., 6. ] )
            cbar.set_label( "Storm Index", size=15 )
            fig.savefig( 'plots/BzPdyn.pdf',orientation='portrait',format='pdf' )
            fig.savefig( 'plots/BzPdyn.jpeg',orientation='portrait',format='jpeg' )
            ax.clear()

            fig = plt.figure(figsize = ( 11, 8.5 ) )
            ax = fig.add_subplot(111)
            sc = plt.scatter( btDatArr, pDynDatArr, c=indexDatArr, s= indexDatArr*5. )
            plt.xlabel( 'Bt-GSM [nT]', fontsize = 15 )
            plt.ylabel( 'pDyn [nPa]', fontsize = 15 )
            cbar = plt.colorbar( sc, ticks=[ 1., 2., 3., 4., 5., 6. ] )
            cbar.set_label( "Storm Index", size=15 )
            fig.savefig( 'plots/BtPdyn.pdf',orientation='portrait',format='pdf' )
            fig.savefig( 'plots/BtPdyn.jpeg',orientation='portrait',format='jpeg' )
            ax.clear()


        # since we are just doing we only need indexDatArr from now on
        del aeDatArr, symhDatArr, asyhDatArr, aeTimeArr, symTimeArr # we are doing this to save memory, these are huge numbers

        ( bzmDatArr, btDatArr, pDynDatArr, omnTimeArr ) = self.omniData()

        # return a single array with Index in the last column and data in the first few
        rows = numpy.array( [ bzmDatArr, btDatArr, pDynDatArr, indexDatArr ] )
        rows = rows.transpose()

        # since we are just doing we only need indexDatArr from now on
        del bzmDatArr, btDatArr, pDynDatArr, omnTimeArr # we are doing this to save memory, these are huge numbers

        return rows