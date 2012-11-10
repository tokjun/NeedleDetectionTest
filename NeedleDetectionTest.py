import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# NeedleDetectionTest
#

class NeedleDetectionTest:
  def __init__(self, parent):
    parent.title = "NeedleDetectionTest" # TODO make this more human readable by adding spaces
    parent.categories = ["Testing"]
    parent.dependencies = []
    parent.contributors = ["Jean-Christophe Fillion-Robin (Kitware), Steve Pieper (Isomics)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc. and Steve Pieper, Isomics, Inc.  and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['NeedleDetectionTest'] = self.runTest

  def runTest(self):
    tester = NeedleDetectionTestTest()
    tester.runTest()

#
# qNeedleDetectionTestWidget
#

class NeedleDetectionTestWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "NeedleDetectionTest Reload"
    self.layout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    self.testButton = qt.QPushButton("Test")
    self.testButton.toolTip = "Test Needle Detection."
    self.testButton.name = "NeedleDetection Test"
    self.layout.addWidget(self.testButton)
    self.testButton.connect('clicked()', self.onTest)

    # Collapsible button
    dummyCollapsibleButton = ctk.ctkCollapsibleButton()
    dummyCollapsibleButton.text = "A collapsible button"
    self.layout.addWidget(dummyCollapsibleButton)

    # Layout within the dummy collapsible button
    dummyFormLayout = qt.QFormLayout(dummyCollapsibleButton)

    # List transforms button
    listTransformsButton = qt.QPushButton("List Transforms") 
    listTransformsButton.toolTip = "List Transforms in the Phython console"
    dummyFormLayout.addWidget(listTransformsButton)
    listTransformsButton.connect('clicked()', self.onListTransforms);

    # List Fiducials button
    listFiducialsButton = qt.QPushButton("List Fiducials") 
    listFiducialsButton.toolTip = "List Fiducials in the Phython console"
    dummyFormLayout.addWidget(listFiducialsButton)
    listFiducialsButton.connect('clicked()', self.onListFiducials);

    # List Rulers button
    listRulersButton = qt.QPushButton("List Rulers") 
    listRulersButton.toolTip = "List Rulers in the Phython console"
    dummyFormLayout.addWidget(listRulersButton)
    listRulersButton.connect('clicked()', self.onListRulers);

    # Convert transform to fiducial
    convertTransformToFiducialButton = qt.QPushButton("Convert Transforms to Fiducials") 
    convertTransformToFiducialButton.toolTip = "Convert Transforms to Fiducials"
    dummyFormLayout.addWidget(convertTransformToFiducialButton)
    convertTransformToFiducialButton.connect('clicked()', self.onConvertTransformToFiducial);

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.listTransformsButton = listTransformsButton
    self.listFiducialsButton  = listFiducialsButton
    self.listRulersButton = listRulersButton
    self.convertTransformToFiducialButton = convertTransformToFiducialButton

  def onReload(self,moduleName="NeedleDetectionTest"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)
    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()

  def onTest(self,moduleName="NeedleDetectionTest"):
    self.onReload()
    evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
    tester = eval(evalString)
    tester.runTest()

  def onListTransforms(self,moduleName="NeedleDetectionTest"):
    self.onReload()
    evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
    tester = eval(evalString)
    tester.listTransforms()
    
  def onListFiducials(self,moduleName="NeedleDetectionTest"):
    self.onReload()
    evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
    tester = eval(evalString)
    tester.listFiducials()

  def onListRulers(self,moduleName="NeedleDetectionTest"):
    self.onReload()
    evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
    tester = eval(evalString)
    tester.listRulers()

  def onConvertTransformToFiducial(self,moduleName="NeedleDetectionTest"):
    self.onReload()
    evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
    tester = eval(evalString)
    tester.convertTransformToFiducial()
    

#
# NeedleDetectionTestLogic
#

class NeedleDetectionTestLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that 
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True


class NeedleDetectionTestTest(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """
  def delayDisplay(self,message,msec=1000):
    """This utility method displays a small dialog and waits.
    This does two things: 1) it lets the event loop catch up
    to the state of the test so that rendering and widget updates
    have all taken place before the test continues and 2) it
    shows the user/developer/tester the state of the test
    so that we'll know when it breaks.
    """
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    self.cliList = []
    #slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    #self.test_NeedleDetectionTest1()
    self.TestNeedleDetection()

  def TestNeedleDetection(self):
    
    parameters = {}
    scene = slicer.mrmlScene
    collection = scene.GetNodesByClass('vtkMRMLScalarVolumeNode');
    nimages = collection.GetNumberOfItems()
    collection.InitTraversal()
    n = 0
    cliList = []
    while n < nimages:
      inImage = collection.GetNextItemAsObject()
      if inImage == None:
        break
      
      id = inImage.GetID()
      print('Processing image node = %s...' % id)
      
      # Create a new image node
      outImage = slicer.vtkMRMLScalarVolumeNode()
      name = inImage.GetName() + '_Needle'
      outImage.SetName(name)
      scene.AddNode(outImage)
      outImage.SetLabelMap(1)

      # Create a new linear transform node (for needle position/orientation)
      needleTransform = slicer.vtkMRMLLinearTransformNode()
      name = inImage.GetName() + '_Transform'
      needleTransform.SetName(name)
      scene.AddNode(needleTransform)

      parameters = {}
      parameters['inputVolume'] = inImage.GetID()
      parameters['outputVolume'] = outImage.GetID()
      parameters['needleTransform'] = needleTransform.GetID()

      parameters['sigma1'] = 0.5
      parameters['minsigma'] = 0.5
      #parameters['maxsigma'] = 1.3
      #parameters['stepsigma'] = 5
      #parameters['minlinemeasure'] = 10
      parameters['maxsigma'] = 1.0
      parameters['stepsigma'] = 6
      parameters['minlinemeasure'] = 10
      parameters['alpha1'] = 0.5
      parameters['alpha2'] = 2
      parameters['anglethreshold'] = 25
      parameters['normal'] = [0.0, 0.0, 1.0]
      parameters['numberOfBins'] = 128
      parameters['minimumObjectSize'] = 50
      parameters['minPrincipalAxisLength'] = 50
      parameters['maxMinorAxisLength'] = 3
      parameters['closestPoint'] = [0.0, 0.0, 0.0]

      nd = slicer.modules.needledetection
      c = slicer.cli.run(nd, None, parameters)
      c.AddObserver('ModifiedEvent', self.printStatus)
      self.cliList.append(c)
      n = n + 1

  def printStatus(self, caller, event):
    if caller.IsA('vtkMRMLCommandLineModuleNode'):
      #print("Status is %s" % caller.GetStatusString())
      if caller.GetStatusString() == 'Complete':
        f = 0
        print("One task is completed")
        for c in self.cliList:
          if c.GetStatusString() != 'Complete':
            f = 1
            break
        if f == 0:
          print ('All needle detection tasks are completed')
          self.cliList = []

  def listTransforms(self):
    self.setUp
    scene = slicer.mrmlScene
    collection = scene.GetNodesByClass('vtkMRMLLinearTransformNode');
    ntransforms = collection.GetNumberOfItems()
    collection.InitTraversal()
    n = 0
    while n < ntransforms:
      tnode = collection.GetNextItemAsObject()
      n = n + 1
      m = vtk.vtkMatrix4x4()
      tnode.GetMatrixTransformToWorld(m)
      elm = (tnode.GetName(),
             m.GetElement(0, 0), m.GetElement(0, 1), m.GetElement(0, 2), m.GetElement(0, 3),
             m.GetElement(1, 0), m.GetElement(1, 1), m.GetElement(1, 2), m.GetElement(1, 3),
             m.GetElement(2, 0), m.GetElement(2, 1), m.GetElement(2, 2), m.GetElement(2, 3),
             m.GetElement(3, 0), m.GetElement(3, 1), m.GetElement(3, 2), m.GetElement(3, 3));
      print('%s, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f' % elm)

  def listFiducials(self):
    self.setUp
    scene = slicer.mrmlScene
    collection = scene.GetNodesByClass('vtkMRMLAnnotationFiducialNode');
    ntransforms = collection.GetNumberOfItems()
    collection.InitTraversal()
    n = 0
    while n < ntransforms:
      fnode = collection.GetNextItemAsObject()
      n = n + 1
      p = [0.0, 0.0, 0.0]
      fnode.GetFiducialCoordinates(p)
      elm = (fnode.GetName(), p[0], p[1], p[2]);
      print('%s, %f, %f, %f' % elm)

  def listRulers(self):
    self.setUp
    scene = slicer.mrmlScene
    collection = scene.GetNodesByClass('vtkMRMLAnnotationRulerNode');
    ntransforms = collection.GetNumberOfItems()
    collection.InitTraversal()
    n = 0
    while n < ntransforms:
      fnode = collection.GetNextItemAsObject()
      n = n + 1
      p1 = [0.0, 0.0, 0.0]
      p2 = [0.0, 0.0, 0.0]
      fnode.GetPosition1(p1)
      fnode.GetPosition2(p2)
      elm = (fnode.GetName(), p1[0], p1[1], p1[2], p2[0], p2[1], p2[2],);
      print('%s, %f, %f, %f, %f, %f, %f' % elm)

  def convertTransformToFiducial(self):
    self.setUp
    scene = slicer.mrmlScene
    collection = scene.GetNodesByClass('vtkMRMLLinearTransformNode');
    ntransforms = collection.GetNumberOfItems()
    collection.InitTraversal()
    n = 0
    scene = slicer.mrmlScene
    while n < ntransforms:
      tnode = collection.GetNextItemAsObject()
      n = n + 1
      m = vtk.vtkMatrix4x4()
      tnode.GetMatrixTransformToWorld(m)

      fnode = slicer.vtkMRMLAnnotationFiducialNode()
      pos = [m.GetElement(0,3), m.GetElement(1,3), m.GetElement(2,3)]
      fnode.SetFiducialCoordinates(pos[0], pos[1], pos[2]);
      scene.AddNode(fnode)
      fnode.CreateAnnotationTextDisplayNode();
      fnode.CreateAnnotationPointDisplayNode();
      name = '%s_Fiducial' % tnode.GetName()
      fnode.SetName(name)
