from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf

sns.set()


class ModelFactory():
    def create_model(self, model_name, datasampler, hyper_parameters={'epoch':5}):
        if model_name == 'lstm':
            datasampler = DataSampler() # the reader object for the input data
            model =  LSTM(datasampler)
            model.set_params(hyper_parameters)
            return model

# example usage
# data = DataSampler(file_name='x.csv', timestamp=5)
# this datasampler is sent to the model
class DataSampler():
    def __init__(self, file_name = '../dataset/GOOG-year.csv', timestamp =5):
        self.df = pd.read_csv()
        self.date_ori = pd.to_datetime(df.iloc[:, 0]).tolist()
        self.minmax = MinMaxScaler()
        self.timestamp = timestamp
        self.df_log = self.preprocess_df()
    
    def preprocess_df(self):
        self.minmax.fit(self.df.iloc[:, 1:].astype('float32'))
        df_log = minmax.transform(df.iloc[:, 1:].astype('float32'))
        df_log = pd.DataFrame(df_log)
        return df_log

    def batch_sampler(self, start, end):
        # sampler for training set
        for k in range(0, start, end):
            index   = min(k + timestamp, df_log.shape[0] -1)
            batch_x = np.expand_dims( df_log.iloc[k : index, :].values, axis = 0)
            batch_y = df_log.iloc[k + 1 : index + 1, :].values
            yield (batch_x, batch_y)
    
    def train_batch_sampler(self):
        return batch_sampler(self.df_log.shape[0] - 1, self.timestamp)
    
    def test_batch_sampler(self):
        return batch_sampler((self.df_log.shape[0] // self.timestamp) * self.timestamp, self.timestamp)
    
    def get_n_samples_per_batch(self):
        return self.df_log.shape[0] // self.timestamp
        


class BaseModelDl(object):
    """
    Base Model class used for models under Dl class 
    acting as parent class
    """
    def __init__(self):
        self.datasampler = None
        self.name = ''
        self.epoch = 5
        self.learning_rate = 0.01
        self.sess = None

    def get_params(self):
        # epoch and learning rate exists in all models
        return {
            'epoch': self.epoch,
            'learning_rate': self.learning_rate
        }

    def set_params(self, **parameters):
        # this function is common for all children classes
        for parameter, value in parameters.items():
            if hasattr(self,parameter):
               setattr(self, parameter, value)
            else:
                raise AttributeError('Class {} does not have parameter {}'.format(
                 self.name, parameter  
                ))
        return self

    def build_model(self):
        # used to create placeholders and optimizer based on parameters set
        # called after setting the parameters
        pass

    def fit(self):
        pass


    def predict(self,X):
        pass

    def load(self, model_path):
        # model_path=parent_folder/model.ckpt
        saver = tf.train.Saver()
        saver.load(self.sess, model_path)

    def save(self, model_path):
        # model_path=parent_folder/model.ckpt
        saver = tf.train.Saver()
        saver.save(self.sess, model_path)


class LSTM(BaseModelDl):
    def __init__(self, datasampler):
        super(LSTM, self).__init__()
        self.datasampler = datasampler
        self.name = 'lstm'
        self.num_layers = 1
        self.size_layer = 128
        self.timestamp = 5
        self.dropout_rate = 0.7
        self.future_day = 50
        self.learning_rate = 0.01
        self.feat_size = 1
        self.output_size = 1
        self.forget_bias = 0.1
        self.model = None


    def get_params(self):
        return {
            'num_layers': self.num_layers,
            'size_layer': self.size_layer,
            'dropout_rate': self.dropout_rate,
            'epoch': self.epoch,
            'learning_rate': 0.01 ,
            'output_size': self.output_size,
            'feat_size': self.feat_size,
            'forget_bias': self.forget_bias
        }


    def build_model(self):
        def lstm_cell(size_layer):
            return tf.nn.rnn_cell.LSTMCell(size_layer, state_is_tuple = False)

        rnn_cells = tf.nn.rnn_cell.MultiRNNCell(
                    [lstm_cell(self.size_layer) for _ in range(self.num_layers)],
                    state_is_tuple = False,)
                    
        self.X = tf.placeholder(tf.float32, (None, None, self.feat_size))
        self.Y = tf.placeholder(tf.float32, (None, self.output_size))
        drop   = tf.contrib.rnn.DropoutWrapper(rnn_cells, output_keep_prob = self.forget_bias)
        self.hidden_layer = tf.placeholder( tf.float32, 
                                            (None, num_layers * 2 * size_layer))
        self.outputs, self.last_state = tf.nn.dynamic_rnn(
            drop, self.X, initial_state = self.hidden_layer, dtype = tf.float32
        )
        self.logits    = tf.layers.dense(self.outputs[-1], output_size)
        self.cost      = tf.reduce_mean(tf.square(self.Y - self.logits))
        self.optimizer = tf.train.AdamOptimizer(learning_rate).minimize(self.cost)

        self.sess    = tf.InteractiveSession()
        self.sess.run(tf.global_variables_initializer())

    
    def fit(self):
        for i in range(self.epoch):
            init_value = np.zeros((1, self.num_layers * 2 * self.size_layer))
            for batch_x, batch_y in self.datasampler.train_batch_sampler():
                last_state, _, loss = sess.run(
                    [self.last_state, self.optimizer, self.cost],
                    feed_dict = {
                        self.X: batch_x,
                        self.Y: batch_y,
                        self.hidden_layer: init_value,
                    },
                )
                init_value = last_state
                total_loss += loss
            total_loss /= self.datasampler.get_n_samples_per_batch()
            if (i + 1) % 100 == 0:
                print('epoch:', i + 1, 'avg loss:', total_loss)

    def predict(self,):
        # takes a sampler as the one in datasampler class
        # in this function it should take a sampler 
