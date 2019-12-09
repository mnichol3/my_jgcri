# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 08:53:36 2019

@author: nich980
"""
import pandas as pd

class EFSubset:
    
    def __init__(self, ef_df, sector, fuel, species, year):
        self.sector     = sector
        self.fuel       = fuel
        self.species    = species
        self.year       = year
        self.isos, self.ef_data = self.subset_df(ef_df)
        
        
        
    def subset_df(self, ef_df):
        """
        Remove a subset of EFs given a sector, fuel, and year
        
        Parameters
        ----------
        self : EFSubset obj
        ef_df : Pandas DataFrame
            DataFrame containing data from an emission factors file
        """
        
        # Extract the fuel and sector
        ef_df = ef_df[ef_df['sector'] == self.sector]
        ef_df = ef_df[ef_df['fuel'] == self.fuel]
        
        isos = ef_df['iso'].tolist()
        ef_list = ef_df['X{}'.format(self.year)].tolist()
        
        return (isos, ef_list)
    
    
    
    def __repr__(self):
        return '<EFSubset object - {} {} {} {}>'.format(self.species, self.sector, self.fuel, self.year)