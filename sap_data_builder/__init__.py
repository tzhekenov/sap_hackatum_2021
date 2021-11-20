import sentiment_processor


class DataVisualizer:

    def __init__(self):
        pass

    @staticmethod
    def visualize_time_series(data, text: str):
        # 1) get sentiment
        # 2) build graph from data
        # 3) generate visuals

        sentiment = sentiment_processor.process(text)
        pass
