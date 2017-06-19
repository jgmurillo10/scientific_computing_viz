#Compiled filters
import vtk
#------------------------------------SOURCES------------------------------------#

#----------------------------CHALLENGE1---------------------------#
rectGridReader = vtk.vtkRectilinearGridReader()
rectGridReader.SetFileName("data/jet4_0.500.vtk")
# do not forget to call "Update()" at the end of the reader
rectGridReader.Update()
#----------------------------ALTERNATIVE---------------------------#
subset = vtk.vtkMaskPoints()
subset.SetOnRatio(10)
subset.RandomModeOn()
subset.SetInputConnection(rectGridReader.GetOutputPort())
#vtk.vtkColorTransferFunction()
#vtk.vtkLookupTable()
lut = vtk.vtkLookupTable()
lut.SetNumberOfColors(256)
lut.SetHueRange(0.667, 0.0)
lut.SetVectorModeToMagnitude()
lut.Build()

hh = vtk.vtkHedgeHog()
hh.SetInputConnection(subset.GetOutputPort())
hh.SetScaleFactor(0.001)

#------------------------------------FILTERS------------------------------------#
#----------------------------CHALLENGE1---------------------------#
rectGridOutline = vtk.vtkRectilinearGridOutlineFilter()
rectGridOutline.SetInputData(rectGridReader.GetOutput())
rectGridGeom = vtk.vtkRectilinearGridGeometryFilter()
rectGridGeom.SetInputData(rectGridReader.GetOutput())
rectGridGeom.SetExtent(0, 128, 0, 0, 0, 127)
#----------------------------CHALLENGE2---------------------------#
magnitudeCalcFilter = vtk.vtkArrayCalculator()
magnitudeCalcFilter.SetInputConnection(rectGridReader.GetOutputPort())
magnitudeCalcFilter.AddVectorArrayName('vectors')
# Set up here the array that is going to be used for the computation ('vectors')
magnitudeCalcFilter.SetResultArrayName('magnitude')
magnitudeCalcFilter.SetFunction("mag(vectors)")
# Set up here the function that calculates the magnitude of a vector
magnitudeCalcFilter.Update()
#----------------------------CHALLENGE3---------------------------#
#Extract the data from the result of the vtkCalculator
points = vtk.vtkPoints()
grid = magnitudeCalcFilter.GetOutput()
grid.GetPoints(points)
scalars = grid.GetPointData().GetArray('magnitude')

#Create an unstructured grid that will contain the points and scalars data
ugrid = vtk.vtkUnstructuredGrid()
ugrid.SetPoints(points)
ugrid.GetPointData().SetScalars(scalars)

#Populate the cells in the unstructured grid using the output of the vtkCalculator
for i in range (0, grid.GetNumberOfCells()):
    cell = grid.GetCell(i)
    ugrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

#There are too many points, let's filter the points
subset = vtk.vtkMaskPoints()
subset.SetOnRatio(50)
subset.RandomModeOn()
subset.SetInputData(ugrid)
#Make a vtkPolyData with a vertex on each point.
pointsGlyph = vtk.vtkVertexGlyphFilter()
pointsGlyph.SetInputConnection(subset.GetOutputPort())
#pointsGlyph.SetInputData(ugrid)
pointsGlyph.Update()
#----------------------------CHALLENGE4---------------------------#
scalarRange = ugrid.GetPointData().GetScalars().GetRange()
isoFilter = vtk.vtkContourFilter()
isoFilter.SetInputData(ugrid)
isoFilter.GenerateValues(10, scalarRange)




#------------------------------------MAPPERS------------------------------------#
#----------------------------CHALLENGE1---------------------------#
rectGridOutlineMapper = vtk.vtkPolyDataMapper()
rectGridOutlineMapper.SetInputConnection(rectGridOutline.GetOutputPort())
rectGridGeomMapper = vtk.vtkPolyDataMapper()
rectGridGeomMapper.SetInputConnection(rectGridGeom.GetOutputPort())
#----------------------------CHALLENGE3---------------------------#

pointsMapper = vtk.vtkPolyDataMapper()
pointsMapper.SetInputConnection(pointsGlyph.GetOutputPort())
pointsMapper.SetScalarModeToUsePointData()
#----------------------------CHALLENGE4---------------------------#
isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(isoFilter.GetOutputPort())
#----------------------------ALTERNATIVE---------------------------#

hhm = vtk.vtkPolyDataMapper()
hhm.SetInputConnection(hh.GetOutputPort())
hhm.SetLookupTable(lut)
hhm.SetScalarVisibility(True)
hhm.SetScalarModeToUsePointFieldData()
hhm.SelectColorArray('vectors')
hhm.SetScalarRange((rectGridReader.GetOutput().GetPointData().GetVectors().GetRange(-1)))

#------------------------------------ACTORS------------------------------------#
#----------------------------CHALLENGE1---------------------------#
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(rectGridOutlineMapper)
outlineActor.GetProperty().SetColor(0, 0, 0)
gridGeomActor = vtk.vtkActor()
gridGeomActor.SetMapper(rectGridGeomMapper)
gridGeomActor.GetProperty().SetRepresentationToWireframe()
gridGeomActor.GetProperty().SetColor(0, 0, 0)
#----------------------------CHALLENGE3---------------------------#
pointsActor = vtk.vtkActor()
pointsActor.SetMapper(pointsMapper)
#----------------------------CHALLENGE4---------------------------#

isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetOpacity(0.5)
#----------------------------ALTERNATIVE---------------------------#
hha = vtk.vtkActor()
hha.SetMapper(hhm)



#------------------------------------RENDERS AND WINDOWS------------------------------------#


renderer = vtk.vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)

#Comment the actors you do not want to visualize
renderer.AddActor(isoActor)
renderer.AddActor(pointsActor)
renderer.AddActor(outlineActor)
renderer.AddActor(gridGeomActor)
renderer.AddActor(hha)
renderer.ResetCamera()

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(500, 500)
renderWindow.Render()

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)
iren.Start()
