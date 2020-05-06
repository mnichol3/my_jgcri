# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 08:53:36 2019

@author: nich980
"""
import logging
import numpy as np

class EFSubset:
    """
    A simple class to hold CEDS emission factor data for a given emission
    species, sector, fuel, and year
    
    Class attributes
    -----------------
    sector : str
         CEDS sector relevant to the subsetted EF data
    fuel : str
        CEDS fuel relevant to the subsetted EF data
    species : str
        Emission species of the EF data
    year : int
        Year relevant to the subsetted EF data
    year_str : str
        The year formatted to match the EF column headers. Format: 'XYYYY'
    isos : list of str
        List of CEDS ISOs, in the same order as they appear in the original EF file
    ef_data : numpy 1D array of type numpy float64
        EF data for the given species, sector, fuel, and year 
        
    Functions
    ---------
    __init__ : Initialize new EFSubset object
    subset_df: Subset the original EF DataFrame based on the given sector, fuel,
               and year
    __repr__: Pretty print an EFSubset object
    """
    
    def __init__(self, ef_df, sector, fuel, species, year):
        """
        Initialize a new EFSubset object
        
        Parameters
        ----------
        ef_df : Pandas DataFrame
            DataFrame containing EF data for a single species
        sector : string
            CEDS sector to subset the EF data by
        fuel : str
            CEDS fuel to subset the EF data by
        species : str
            Emissions species for the given EF data
        year : int
            Year to subset the EF data by
            
        Return
        -------
        EFSubset obj
        """
        logger = logging.getLogger('main')
        logger.info("Initializing EFSubset object: {} {} {}".format(sector, fuel, year))
        
        self.sector     = sector
        self.fuel       = fuel
        self.species    = species
        self.year       = year
        self.year_str   = 'X{}'.format(year)
        self.isos, self.ef_data = self.subset_df(ef_df)
        
        
        
    def subset_df(self, ef_df):
        """
        Remove a subset of EFs given a sector, fuel, and year
        
        Parameters
        ----------
        self : EFSubset obj
        ef_df : Pandas DataFrame
            DataFrame containing data from an emission factors file
            
        Return
        -------
        isos : list of str
            CEDS ISOs in the order that they appear in the original EF file
        ef_list : numpy 1d array of type numpy float64
            Array of EF values for the given CEDS sector & fuel and year
        """
        
        # Extract the fuel and sector
        ef_df = ef_df[ef_df['sector'] == self.sector]
        ef_df = ef_df[ef_df['fuel'] == self.fuel]
        
        isos = ef_df['iso'].tolist()
        ef_list = ef_df['X{}'.format(self.year)].tolist()
        ef_list = np.asarray(ef_list, dtype=np.float64)
        
        return (isos, ef_list)
    
    
    
    def __repr__(self):
        return '<EFSubset object - {} {} {} {}>'.format(self.species, self.sector, self.fuel, self.year)