class StormPredict(object):
    """ 
    Build a machine learning based storm predictor

    Author - Bharat Kunduri
    """

    import datetime

    def __init__( self, startTime=datetime.datetime(2012,1,1,0), endTime=datetime.datetime(2012,12,31,23) ):
        # set the start and end times to run the classification algorithm on
        self.sTime = startTime
        self.eTime = endTime

    def symHAePred( self, makeSctrPlt=False ):
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
        del ae # we are doing this to save memory, these are huge numbers

        #Read in SymH, AsymH Data...
        symasy=gme.ind.symasy.readSymAsy(sTime=self.sTime, eTime=self.eTime, symh=None, symd=None, asyh=None, asyd=None)
        symhDatArr  = [symasy[x].symh for x in range(len(symasy))]
        asyhDatArr  = [symasy[x].asyh for x in range(len(symasy))]
        symTimeArr  = [symasy[x].time for x in range(len(symasy))]
        del symasy # we are doing this to save memory, these are huge numbers
        symhDatArr = numpy.array( symhDatArr )
        asyhDatArr = numpy.array( asyhDatArr )

        if makeSctrPlt :
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
            ax.clear()


