from factor_graph import *

RV('burglary',('Yburg','Nburg'))
RV('earthquake',('Yquake','Nquake'))
RV('alarm',('Ysound','Nsound'))
RV('JohnCalls',('Yjohn','Njohn'))
RV('MaryCalls',('Ymery','Nmery'))


burg_prior = {	('Yburg',):0.001,
				('Nburg',):0.999,
				}

quake_prior = {	('Yquake',):0.002,
				('Nquake',):0.998,
				}



g = FactorGraph()
