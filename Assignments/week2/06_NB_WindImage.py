#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:32:24 2017

@author: juanmurillo
"""

#wind_image.vti

import vtk

# Read the file (to test that it was written correctly)
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("./data/wind_image.vti")
reader.Update()

#------------ FILTER: CALCULATE VECTOR MAGNITUDE ----------------------
magnitudeCalcFilter = vtk.vtkArrayCalculator()
magnitudeCalcFilter.SetInputConnection(reader.GetOutputPort())
magnitudeCalcFilter.AddVectorArrayName('vectors')
magnitudeCalcFilter.SetResultArrayName('magnitude')
magnitudeCalcFilter.SetFunction("mag(vectors)") 
magnitudeCalcFilter.Update()
print(magnitudeCalcFilter.GetOutput())
#------------END CALCULATE VECTOR MAGNITUDE ----------------------

#------------FILTER: RECTILINEAR GRID TO IMAGE DATA-----------
bounds = magnitudeCalcFilter.GetOutput().GetBounds()
dimensions = magnitudeCalcFilter.GetOutput().GetDimensions()
origin = (bounds[0], bounds[2], bounds[4])
spacing = ( (bounds[1]-bounds[0])/dimensions[0], 
            (bounds[3]-bounds[2])/dimensions[1],
            (bounds[5]-bounds[4])/dimensions[2])

imageData = vtk.vtkImageData()
imageData.SetOrigin(origin)
imageData.SetDimensions(dimensions)
imageData.SetSpacing(spacing)

probeFilter = vtk.vtkProbeFilter()
probeFilter.SetInputData(imageData)
probeFilter.SetSourceData(magnitudeCalcFilter.GetOutput())
probeFilter.Update()

imageData2 = probeFilter.GetImageDataOutput()
#------------END RECTILINEAR GRID TO IMAGE DATA-----------

##------------FILTER, MAPPER, AND ACTOR: VOLUME RENDERING -------------------
# Create transfer mapping scalar value to opacity
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(0, 0.1) #when the value is 0 assign 0.2 opacity
opacityTransferFunction.AddPoint(30,0.5)
opacityTransferFunction.AddPoint(40,1)
opacityTransferFunction.AddPoint(80, 1) #when value is 14 assign 0 opacity

#rectiliniar grid to image data is not necessary when file is .vti
#wind_image.vti
#the other uploading is the work.

# Create transfer mapping scalar value to color
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(10.5, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(20.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(40.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(80.0, 0.0, 0.2, 0.0)

# The property describes how the data will look
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOff()
volumeProperty.SetInterpolationTypeToLinear()


# The mapper / ray cast function know how to render the data
#volumeMapper = vtk.vtkProjectedTetrahedraMapper()
#volumeMapper = vtk.vtkUnstructuredGridVolumeZSweepMapper()
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
#volumeMapper = vtk.vtkUnstructuredGridVolumeRayCastMapper()
volumeMapper.SetInputData(imageData2)

# The volume holds the mapper and the property and
# can be used to position/orient the volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

##------------END VOLUME RENDERING ----------------------

##LASTTTTTTTTTTTT----

# Convert the image to a polydata

 
# Setup rendering
renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)
renderer.SetBackground(1,1,1)
renderer.ResetCamera()
 
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
 
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
 
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.Start()
