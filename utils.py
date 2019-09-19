import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import io
from io import BytesIO
from blurred_gan import WGANGP


def create_result_subdir(result_dir: str, run_name: str) -> str:
    import glob
    from itertools import count
    import os
    paths = glob.glob(os.path.join(result_dir, f"*-{run_name}"))
    run_ids = map(lambda p: int(os.path.basename(p).split("-")[0]), paths)
    run_id = max(run_ids, default=0) + 1
    path = os.path.join(result_dir, f"{run_id:02d}-{run_name}")
    print(f"Creating result subdir at '{path}'")
    os.makedirs(path)
    return path


def run_id(path_string):
    return int(path_string.split("/")[-2].split("-")[0])


def epoch(path_string):
    return int(path_string.split("/")[-1].split("_")[1].split(".")[0])


def locate_model_file(result_dir: str, run_name: str):
    import glob
    import os
    paths = glob.glob(os.path.join(result_dir, f"*-{run_name}/model_*.h5"))
    if not paths:
        return None

    paths = sorted(paths, key=run_id, reverse=True)
    latest_run_id = run_id(paths[0])

    paths = list(filter(lambda p: run_id(p) == latest_run_id, paths))
    paths = sorted(paths, key=epoch, reverse=True)
    return paths[0]


@tf.function
def normalize_images(images):
    return (images + 1) / 2


def plot_to_image(figure):
    """Converts the matplotlib plot specified by 'figure' to a PNG image and
    returns it. The supplied figure is closed and inaccessible after this call."""
    
    # Save the plot to a PNG in memory.
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    # Closing the figure prevents it from being displayed directly inside
    # the notebook.
    plt.close(figure)
    buf.seek(0)
    # Convert PNG buffer to TF image
    image = tf.image.decode_png(buf.getvalue(), channels=4)
    # Add the batch dimension
    image = tf.expand_dims(image, 0)
    return image


def samples_grid(samples):
    """Return a grid of the samples images as a matplotlib figure."""
    # Create a figure to contain the plot.
    figure = plt.figure()
    for i in range(64):
        # Start next subplot.
        plt.subplot(8, 8, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        x = samples[i]
        if x.shape[-1] == 1:
            x = np.reshape(x, [*x.shape[:-1]])
        plt.imshow(x)
    plt.tight_layout(pad=0)
    return figure

