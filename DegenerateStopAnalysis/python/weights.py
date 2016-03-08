



isrWeight = lambda norm: '(1.+{norm}*GenPart_mass[stopIndex1]) *(1.*(stops_pt<120.)+0.95*(stops_pt>=120.&&stops_pt<150.)+0.9*(stops_pt>=150.&&stops_pt<250.)+0.8*(stops_pt>=250.))'.format(norm=norm)
isrw = isrWeight(9.5e-5)
