# -*- coding: utf-8 -*-

import os
import re
import logging
import numpy as np

from collections import OrderedDict


#%%---------------------------------------------------------------------------#
class GTParam(OrderedDict):
    
    pat_single = re.compile(r'(.+)=(.+)')
    pat_multi = re.compile(r'(.+)>(.+)<')
    
    
    def __init__(self, path):
        
        if os.path.lexists(path):
            
            with open(path, 'r') as fobj:
                
                lines = [l.strip() for l in fobj.readlines() if l.strip()]
                
                grp1 = [GTParam.pat_single.match(l) for l in lines]
                grp2 = [GTParam.pat_multi.match(l) for l in lines]
                

                
                if all(item is not None for item in grp1):
                    
                    self.flag = 1
                
                    items = OrderedDict([s.strip() for s in item.groups()] for item in grp1)
                    
                elif all(item is not None for item in grp2):
                    
                    self.flag = 2
                    
                    items = OrderedDict((item.groups[0].strip(), 
                                         np.fromiter((s.strip() for s in item.groups[1]),
                                                     dtype=np.object)) for item in grp2)
                    
                else:
                    
                    raise ValueError
                
        else:
            
            items = OrderedDict()
            
        self.path = path

        
        super().__init__(items)
        
        
    #%%-----------------------------------------------------------------------#   
    def save(self):
        
        with open(self.path, 'w') as fobj:
            
            fobj.writelines(['{} = {}\n'.format(k, v) for k, v in self.items()])
#%%---------------------------------------------------------------------------#
            
class GTResult(OrderedDict):
    
    def __init__(self, path):
        
        
        pass
        
#%%---------------------------------------------------------------------------#
class GTObject(object):
    
    
    def __init__(self, path, **kwargs):
        
        path = os.path.abspath(os.path.normpath(path))
        
        if os.path.lexists(path):

            self.path, _ = os.path.splitext(path)
            
        else:
            self.path = path
            
           
        self.parameters = GTParam(kwargs.pop('paramfile', self.path+'.param'))
        
        
    #%%-----------------------------------------------------------------------#            
    def set_parameter(self, name, value):
        
        self.parameters[name] = value
        
        return self

    setp = set_parameter
    #%%-----------------------------------------------------------------------#
    def update(self):
        
        self.parameters.save()
        
    #%%-----------------------------------------------------------------------#
    def export(self, expfile=None, gdxfile=None, rltfile=None, delimiter=','):
        
        return GTResult(rltfile)
        
        

#%%---------------------------------------------------------------------------#
if __name__ == '__main__':

    gto = GTObject(r'..\unittest\simple1d.gtm' )

    print(gto.path)
    
    print(gto.parameters)
    
    gto.setp('FlowRate', 100)
    gto.setp('Test', 30)
    
    print(gto.parameters)
    
#    gto.update()
    
    expfile = r'..\unittest\simple1d.exp'
    
    print(gto.export())

        