import numpy as np
import torch

from reversiAPI.players.models.models import TheModelClass


def load_model(file_path):
    model = TheModelClass(65, 128, 64)
    model.load_state_dict(torch.load(file_path))
    model.eval()
    return model


class PlayerDqn(object):
    def __init__(self, stone_color, file_path, display=True):
        self.stone_color = stone_color
        self.model = load_model(file_path)
        self.display = display

    def put_stone(self, reversi_packages):
        with torch.no_grad():
            input_array = np.append(
                np.array(self.stone_color),
                np.array(reversi_packages.get_board_status(self.stone_color))
            )
            input_data = torch.from_numpy(input_array).type(torch.FloatTensor)
            input_data_unsqueezed = torch.unsqueeze(input_data, 0)
            q_values = np.array(self.model(input_data_unsqueezed)).reshape(-1)

        puttable_index = reversi_packages.get_stone_putable_pos(self.stone_color)
        stone_put_index = puttable_index[0]
        for index in puttable_index:
            if q_values[stone_put_index] < q_values[index]:
                stone_put_index = index
        if self.display:
            print(stone_put_index + 1, self.stone_color)

        return stone_put_index
