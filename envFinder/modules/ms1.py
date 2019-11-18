
from typing import Dict, Tuple, List

from pyteomics import ms1, mzml, mzxml

_MZ_KEY = 'mz'
_INT_KEY = 'int'

class Ms1File(object):

    @staticmethod
    def getMzRange(mono_mz: float, charge: int, range : int = 10) -> Tuple:
       return ((mono_mz - range) / charge, (mono_mz + range) / charge)

    @staticmethod
    def getReadFxn(type:str):
        if type == 'ms1':
            return ms1.read
        elif type == 'mzXML':
            return mzxml.read
        elif type == 'mzML':
            return mzml.read
        else:
            raise RuntimeError('{} is an invalid file type!'.format(type))

    def _getIDStr(self, id):
        if type == 'ms1':
            return str(id).zfill(6)
        else:
            return str(id)

    def __init__(self, fname: str = None, file_type:str = 'mzXML'):
        if fname is None:
            self.fname = str()
        else: self.read(fname, file_type)

    def read(self, fname: str, file_type: str = 'mzXML'):
        self.fname = fname
        _read = Ms1File.getReadFxn(file_type)
        self.dat = _read(self.fname, use_index = True)

    def getSpectra(self, scan: int, mz_range : Tuple) -> Dict:
        '''
        Return spectra at scan in the mz_range

        :param scan: Scan number to fetch
        :type scan: int
        :param mz_range: mz range to return. If None, the entire scan is returned.
        :type mz_range: Tuple(float, float)
        :return: Dict with arrays for mz and int
        '''

        vals = {'m/z array': _MZ_KEY, 'intensity array': _INT_KEY}
        spec = self.dat.get_by_id(self._getIDStr(scan))
        if mz_range is None:
            selection = [True for _ in spec['m/z array']]
        else:
            selection = list(map(lambda x, y: x and y,
                                 spec['m/z array'] >= mz_range[0],
                                 spec['m/z array'] <= mz_range[1]))

        return {v: spec[k][selection] for k, v in vals.items()}









