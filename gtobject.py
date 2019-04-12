# -*- coding: utf-8 -*-

import os
import re
import logging

from collections import OrderedDict

#%%---------------------------------------------------------------------------#
class GTParam(OrderedDict):
    
    pat_single = re.compile(r'(.+)=(.+)')
    pat_multi = re.compile(r'(.+)>(.+)<')
    
    
    def __init__(self, path):
        
        if os.path.lexists(path):
            
            with open(path, 'r') as fobj:
                
                lines = [l.strip() for l in fobj.readlines() if l.strip()]
                
                items = OrderedDict((s.strip() for s in 
                        line.split('=')) for line in lines)
                
        else:
            
            items = OrderedDict()
            
        self.path = path
        self.pkeys = items.keys()
        
        super().__init__(items)
        
        
    #%%-----------------------------------------------------------------------#   
    def save(self):
        
        with open(self.path, 'w') as fobj:
            
            fobj.writelines(['{} = {}\n'.format(k, v) for k, v in self.items()])

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

#%%---------------------------------------------------------------------------#
if __name__ == '__main__':

    gto = GTObject(r'..\unittest\simple1d.gtm' )

    print(gto.path)
    
    print(gto.parameters)
    
    gto.setp('FlowRate', 100)
    gto.setp('Test', 30)
    
    print(gto.parameters)
    
    gto.update()
    
#    print(gto.paramfile)            