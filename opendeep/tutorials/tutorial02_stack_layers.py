"""
Please refer to the following tutorial in the documentation at www.opendeep.org

Tutorial: Your Second Model (Combining Layers)
"""
# standard libraries
import logging
# third party libraries
import theano.tensor as T
from opendeep.log.logger import config_root_logger
from opendeep.models.container import Prototype
from opendeep.models.single_layer.basic import BasicLayer, SoftmaxLayer
from opendeep.tutorials.tutorial01_modular_dae import DenoisingAutoencoder
from opendeep.optimization.adadelta import AdaDelta
from opendeep.data.standard_datasets.image.mnist import MNIST
from opendeep.data.dataset import TEST

# grab a log to output useful info
log = logging.getLogger(__name__)

def create_stacked_dae():
    # initialize the empty container
    stacked_dae = Prototype()
    # # add a few layers of denoising autoencoders!
    # stacked_dae.add(DenoisingAutoencoder(input_size=28*28, hidden_size=1000))
    # # use our inputs_hook we implemented before! in this case, hook the input to the output of the last model added.
    # stacked_dae.add(DenoisingAutoencoder(inputs_hook=(1000, stacked_dae[-1].get_hiddens()), hidden_size=1500))
    # # do it again for good measure, to make a 3-layer stacked denoising autoencoder
    # stacked_dae.add(DenoisingAutoencoder(inputs_hook=(1500, stacked_dae[-1].get_hiddens()), hidden_size=1500))
    # # now we need to go back down to the input level - use params_hook to tie parameters!
    # stacked_dae.add(DenoisingAutoencoder(hiddens_hook=(1500, stacked_dae[-1].get_outputs()), input_size=1500,
    #                                      params_hook=stacked_dae[-1].get_params()))
    # stacked_dae.add(DenoisingAutoencoder(hiddens_hook=(1500, stacked_dae[-1].get_outputs()), input_size=1000,
    #                                      params_hook=stacked_dae[-1].get_params()))
    # stacked_dae.add(DenoisingAutoencoder(hiddens_hook=(100, stacked_dae[-1].get_outputs()), input_size=28*28,
    #                                      params_hook=stacked_dae[-1].get_params()))
    #
    # # that's it! we just used a container to combine three denoising autoencoders into one!
    # # while this is easy to set up for experiments, I would still recommend making a Model instance
    # # for your awesome new model :)
    #
    # # Let's train this container with AdaDelta on MNIST, as usual with these tutorials
    # optimizer = AdaDelta(model=stacked_dae, dataset=MNIST())
    #
    # optimizer.train()

def create_mlp():
    # define the model layers
    relu_layer1 = BasicLayer(input_size=784, output_size=1000, activation='rectifier')
    relu_layer2 = BasicLayer(inputs_hook=(1000, relu_layer1.get_outputs()), output_size=1000, activation='rectifier')
    class_layer3 = SoftmaxLayer(inputs_hook=(1000, relu_layer2.get_outputs()), output_size=10, out_as_probs=False)
    # add the layers as a Prototype
    mlp = Prototype(layers=[relu_layer1, relu_layer2, class_layer3])

    mnist = MNIST()

    optimizer = AdaDelta(model=mlp, dataset=mnist, n_epoch=20)
    optimizer.train()

    test_data = mnist.getDataByIndices(indices=range(25), subset=TEST)
    # use the predict function!
    preds = mlp.predict(test_data)
    print '-------'
    print preds
    print mnist.getLabelsByIndices(indices=range(25), subset=TEST)




if __name__ == '__main__':
    config_root_logger()
    create_mlp()
    # create_stacked_dae()