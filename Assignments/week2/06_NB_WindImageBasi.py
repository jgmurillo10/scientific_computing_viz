#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 11:28:51 2017

@author: juanmurillo
"""

import vtk

# Read the file (to test that it was written correctly)
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("./data/wind_image.vti")
reader.Update()

# Convert the image to a polydata
imageDataGeometryFilter = vtk.vtkImageDataGeometryFilter()
imageDataGeometryFilter.SetInputConnection(reader.GetOutputPort())
imageDataGeometryFilter.Update()

scalarRange = reader.GetOutput().GetPointData().GetScalars().GetRange(-1)
print(scalarRange)
contoursFilter = vtk.vtkContourFilter()
contoursFilter.SetInputConnection(reader.GetOutputPort())
contoursFilter.GenerateValues(100, scalarRange)


contoursMapper = vtk.vtkPolyDataMapper()
contoursMapper.SetInputConnection(contoursFilter.GetOutputPort())
contoursMapper.SetColorModeToMapScalars()
contoursMapper.ScalarVisibilityOn()
contoursMapper.SelectColorArray("wind_speed")
contoursMapper.SetScalarRange(scalarRange)

contoursActor = vtk.vtkActor()
contoursActor.SetMapper(contoursMapper)

actor = vtk.vtkActor()
actor.SetMapper(contoursMapper)
 
# Setup rendering
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1,1,1)
renderer.ResetCamera()
 
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
 
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
 
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.Start()
