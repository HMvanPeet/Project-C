import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(x, self.w)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        return 1 if nn.as_scalar(self.run(x)) >= 0 else -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        mistakes = True
        while mistakes:
            mistakes = False
            for x, y in dataset.iterate_once(1):
                if self.get_prediction(x) != nn.as_scalar(y):
                    mistakes = True
                    #the multiplier is the label (1 or -1) of a incorrectly predicted point
                    self.w.update(x, nn.as_scalar(y))

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        #1 input because there is a single x, 1 hidden layer of 100 hidden neurons, 1 output
        input = 1
        neurons = 100
        output = 1
        self.w1 = nn.Parameter(input, neurons)
        self.w2 = nn.Parameter(neurons, output)
        self.b1 = nn.Parameter(1, neurons)
        self.b2 = nn.Parameter(1, output)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        #Created from equation f(x) = ReLU(x * w1 + b1) * w2 + b2
        return nn.AddBias(nn.Linear(nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1)), self.w2), self.b2)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        halfset = int(len(dataset.x) / 2)
        multiplier = -0.05
        #Calculate initial loss in case that it accidentally is correct before training
        for x, y in dataset.iterate_once(len(dataset.x)):
            loss = self.get_loss(x, y)
        #As long as the loss is too great, keep learning
        while nn.as_scalar(loss) > 0.02:
            for x, y in dataset.iterate_once(halfset):
                grad_b1, grad_b2, grad_w1, grad_w2 = nn.gradients(self.get_loss(x, y), [self.b1, self.b2, self.w1, self.w2])
                self.w1.update(grad_w1, multiplier)
                self.w2.update(grad_w2, multiplier)
                self.b1.update(grad_b1, multiplier)
                self.b2.update(grad_b2, multiplier)
            #At the end of the while-loop, calculate new loss
            for x, y in dataset.iterate_once(len(dataset.x)):
                loss = self.get_loss(x, y)

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        #784 input (1 for each pixel), 2 hidden layers of 200 hidden neurons each, 10 outputs
        input = 784
        neurons = 400
        output = 10
        hidden_layer_size = int(neurons / 2)
        self.w1 = nn.Parameter(input, hidden_layer_size)
        self.w2 = nn.Parameter(hidden_layer_size, hidden_layer_size)
        self.w3 = nn.Parameter(hidden_layer_size, output)
        self.b1 = nn.Parameter(1, hidden_layer_size)
        self.b2 = nn.Parameter(1, hidden_layer_size)
        self.b3 = nn.Parameter(1, output)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        #Created from equation f(x) = ReLU(ReLU(x * w1 + b1) * w2 + b2) * w3 + b3
        return nn.AddBias(nn.Linear(nn.ReLU(nn.AddBias(nn.Linear(nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1)), self.w2), self.b2)), self.w3), self.b3)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        #Train in batches of 100. While accuracy is lower than 97%, keep training
        partset = int(len(dataset.x) / 600)
        multiplier = -0.3
        while dataset.get_validation_accuracy() < 0.97:
            for x, y in dataset.iterate_once(partset):
                grad_b1, grad_b2, grad_b3, grad_w1, grad_w2, grad_w3 = nn.gradients(self.get_loss(x, y), [self.b1, self.b2, self.b3, self.w1, self.w2, self.w3])
                self.w1.update(grad_w1, multiplier)
                self.w2.update(grad_w2, multiplier)
                self.w3.update(grad_w3, multiplier)
                self.b1.update(grad_b1, multiplier)
                self.b2.update(grad_b2, multiplier)
                self.b3.update(grad_b3, multiplier)

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    #Extra explanation: https://iamtrask.github.io/2015/11/15/anyone-can-code-lstm/
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]
        hidden_layer_size = 100

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.w1 = nn.Parameter(self.num_chars, hidden_layer_size)
        self.w2 = nn.Parameter(hidden_layer_size, len(self.languages))
        self.wh = nn.Parameter(hidden_layer_size, hidden_layer_size)

        #I didn't need biases
        #self.b1 = nn.Parameter(1, hidden_layer_size)
        #self.b2 = nn.Parameter(1, len(self.languages))
        #self.bh = nn.Parameter(1, hidden_layer_size)

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        #Initializes a hidden state (h) for the first "NN"
        h = nn.ReLU(nn.Linear(xs[0], self.w1))
        wordlength = len(xs)

        #Iterates through all letters to update h
        for i in range(1, wordlength):
            h = nn.Add(nn.ReLU(nn.Linear(xs[i], self.w1)), nn.ReLU(nn.Linear(h, self.wh)))
        #Use h of the last NN to calculate the prediction
        output = nn.Linear(h, self.w2)
        return output

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        #Use a simple SoftMax calculation to find the loss
        return nn.SoftmaxLoss(self.run(xs), y)


    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        #Create batches of 500 elements to train with
        partset = int(len(dataset.train_x) / 35)
        multiplier = -0.5

        #While the accuracy is too low on the validation set, keep looping the training
        #A higher accuracy is needed for the validation set, because it is possible that the accuracy of the testset is lower
        while dataset.get_validation_accuracy() < 0.87:
            for x, y in dataset.iterate_once(partset):
                grad_w1, grad_w2, grad_wh = nn.gradients(self.get_loss(x, y), [self.w1, self.w2, self.wh])
                self.w1.update(grad_w1, multiplier)
                self.w2.update(grad_w2, multiplier)
                self.wh.update(grad_wh, multiplier)