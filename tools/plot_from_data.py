import argparse
import json
import os
import plotly.express as px


class SynthData:
    def __init__(self):
        self.data = None
        self.processor = None
        self.board = None
        self.luts = None
        self.max_freq = None
        self.used_luts = None

    def load_data(self, path):
        try:
            with open(path, 'r') as f:
                self.data = json.load(f)
            self.processor = self.data['processor']
            self.board = self.data['board']
            self.luts = self.data['luts']
            self.used_luts = self.luts.pop('used')
            self.max_freq = int(self.data['max_freq_mhz'])
        except Exception as e:
            print(f'File {path} could not be loaded: {e}')
            raise e


if __name__ == '__main__':
    # create a plot with frequency vs luts with all json files in the directory
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--path',
        '-p',
        help='Path to the directory containing the json files',
        default='.',
    )
    data = []
    json_path = arg_parser.parse_args().path
    for file in os.listdir(json_path):
        if file.endswith('.json'):
            try:
                synth = SynthData()
                synth.load_data(os.path.join(json_path, file))
                data.append(synth)
            except Exception as e:
                print(f'Error processing {file}: {e}')
    if not data:
        print('No files were processed')
        exit(1)

    # if there are multiple processors with the same frequency and lut on the
    # same board, remove all as they are not connected to the shell
    data = [
        x
        for x in data
        if not any(
            y
            for y in data
            if x.board == y.board
            and x.max_freq == y.max_freq
            and x.used_luts == y.used_luts
            and x.processor != y.processor
        )
    ]

    # make a png for every board
    for board in set([x.board for x in data]):
        fig = px.scatter(
            x=[x.max_freq for x in data if x.board == board],
            y=[x.used_luts for x in data if x.board == board],
            text=[x.processor for x in data if x.board == board],
            labels={'x': 'Frequency (MHz)', 'y': 'Used LUTs'},
            title=f'Frequency vs LUTs',
            color=[x.processor for x in data if x.board == board],
        )
        fig.update_traces(textposition='top center')
        fig.update_layout(legend_title_text='Processor')
        fig.write_html(f'performance_comparison_{board}.html')
        fig.write_image(f'performance_comparison_{board}.png')
