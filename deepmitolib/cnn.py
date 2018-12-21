from keras.models import load_model
import numpy

class CNN(object):
  
  def __init__(self, filepath):
    self.model = load_model(filepath)

  def summary(self):
    self.model.summary()

  def predict(self, X):
    return self.model.predict(X)
    

class MultiCNNWrapper():
  def __init__(self, filenames):
    self.models = []
    for filename in filenames:
      self.models.append(CNN(filename))

  def predict(self, X):
    pred = []
    for model in self.models:
      ypred = model.predict(X)
      pred.append([ypred[0][0,0], ypred[1][0,0], ypred[2][0,0], ypred[3][0,0]])
    pred = numpy.mean(numpy.array(pred), axis=0)
    return pred

if __name__ == "__main__":
  cnn = CNN()
