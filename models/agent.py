import os
from .feature import Extractor
from .value import ValueNet
from .policy import PolicyNet
from const import *


class Player:

    def __init__(self):
        if CUDA:
            self.extractor = Extractor(INPLANES, OUTPLANES_MAP).cuda()
            self.value_net = ValueNet(OUTPLANES_MAP, OUTPLANES).cuda()
            self.policy_net = PolicyNet(OUTPLANES_MAP, OUTPLANES).cuda()
        else:
            self.extractor = Extractor(INPLANES, OUTPLANES_MAP)
            self.value_net = ValueNet(OUTPLANES_MAP, OUTPLANES)
            self.policy_net = PolicyNet(OUTPLANES_MAP, OUTPLANES)    
        
        self.passed = False
    

    def save_models(self, state, current_time):
        """ Save the models """

        for model in ["extractor", "policy_net", "value_net"]:
            self._save_checkpoint(getattr(self, model), model,\
                                state, current_time)


    def _save_checkpoint(self, model, filename, state, current_time):
        """ Save a checkpoint of the models """

        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), \
                            '..', 'saved_models', current_time)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        filename = os.path.join(dir_path, "{}-{}.pth.tar".format(state['version'], filename))
        state['model'] = model.state_dict()
        torch.save(state, filename)


    def load_models(self, path, models):
        """ Load an already saved model """

        names = ["extractor", "policy_net", "value_net"]
        for i in range(0, len(models)):
            checkpoint = torch.load(os.path.join(path, models[i]))
            model = getattr(self, names[i])
            model.load_state_dict(checkpoint['model'])
            return checkpoint

