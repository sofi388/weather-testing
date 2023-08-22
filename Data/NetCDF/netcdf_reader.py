import netCDF4 as nc
import numpy as np
from netCDF4 import Dataset
import scipy.interpolate

fn = 'cmems_obs.nc'
ds = nc.Dataset(fn)
print('\n --------------------- Dataset METADATA --------------------- \n')
print(ds)

print('\n --------------------- Variables --------------------- \n')
for var in ds.variables.values():
    print(var)

print('\n  --------------------- Eastward_wind -------------------- \n')
eastward_wind = ds['eastward_wind'][6, 0, 0]
print('eastward_wind')
print(eastward_wind)

eastward_wind = ds['eastward_wind'][:]
print(eastward_wind)

print('\n  --------------------- lon & lat ------------------- \n')
lon = ds['lon'][0]
print(lon)
lat = ds['lat'][0]
print(lat)

print('\n  --------------------- time -------------------- \n')
time = ds['time'][0]
print('seconds since 1990-01-01 00:00:00  :   ')
print(time)

print('\n  --------------------- ncep_global -------------------- \n')
fn = 'ncep_global.nc'
ds = nc.Dataset(fn)

print('\n --------------------- Dataset METADATA --------------------- \n')
print(ds)

print('\n --------------------- Variables --------------------- \n')
for var in ds.variables.values():
    print(var)

print('\n  --------------------- ugrd10m -------------------- \n')
print('\n  ---------- eastward wind velocity at 10m --------- \n')
ugrd10m = ds['ugrd10m'][0, 0, 0]
print('ugrd10m')
print(ugrd10m)

ugrd10m = ds['ugrd10m'][:]
print(ugrd10m)

print('\n  --------------------- lon & lat-------------------- \n')
lon = ds['longitude'][:]
print(lon)
lat = ds['latitude'][:]
print(lat)

print('\n  --------------------- time -------------------- \n')
time = ds['time'][:]
print('hours since 2022-12-01 00:00:00.000 UTC  :   ')
print(time)
