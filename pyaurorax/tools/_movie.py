# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
from tqdm.contrib.concurrent import process_map as tqdm_process_map
from concurrent.futures import ProcessPoolExecutor


def __process_frame(fname):  # pragma: nocover-ok
    return {
        "fname": fname,
        "img": cv2.imread(fname, cv2.IMREAD_UNCHANGED),
    }


def movie(aurorax_obj, input_filenames, output_filename, n_parallel, fps, progress_bar_disable):
    # read in all frames
    #
    # NOTE: we do with using multiprocessing, but we need to be very
    # careful to ensure that the frames are being added to the list
    # in order. This preserves the order of the file list that was
    # supplied.
    frame_list = []
    if (n_parallel == 1):
        # don't do anything special, just a basic loop
        if (progress_bar_disable is True):
            # no progress bar
            for fname in input_filenames:
                img = cv2.imread(fname)
                frame_list.append(img)
        else:
            # with progress bar
            for fname in aurorax_obj._tqdm(input_filenames, desc="Reading files: ", unit="files"):
                img = cv2.imread(fname)
                frame_list.append(img)
    else:
        # multiple workers, do it in a multiprocessing loop
        if (progress_bar_disable is True):
            with ProcessPoolExecutor(max_workers=n_parallel) as executor:
                for result in executor.map(__process_frame, input_filenames):
                    frame_list.append(result["img"])
        else:
            results = tqdm_process_map(
                __process_frame,
                input_filenames,
                max_workers=n_parallel,
                chunksize=1,
                desc="Reading files: ",
                unit="files",
                tqdm_class=aurorax_obj._tqdm,
            )
            for result in results:
                frame_list.append(result["img"])

    # get dimensions of images so we can initialize the video writer
    #
    # NOTE: we assume that all images are the same size. Perhaps we can
    # put a check in while we read all the images in?
    if (len(frame_list) == 0):
        raise IOError("No images read in. Check that filenames were indeed supplied.")
    elif (len(frame_list[0].shape) == 2 or len(frame_list[0].shape) == 3):
        width = frame_list[0].shape[0]
        height = frame_list[0].shape[1]
    else:  # pragma: nocover
        # some unexpected image shape
        raise IOError("Unexpected shape of image data. Found shape %s, but was expecting only 2 or 3 dimensions." % (frame_list[0].shape))

    # initialize videowriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # type: ignore
    frame_size = (height, width)
    writer = cv2.VideoWriter(output_filename, fourcc, fps, frame_size)

    # write the frames
    if (progress_bar_disable is True):
        # no progress bar
        for i in range(0, len(frame_list)):
            writer.write(frame_list[i])
    else:
        # with progress bar
        for i in aurorax_obj._tqdm(range(0, len(frame_list)), desc="Encoding frames: ", unit="frames"):
            writer.write(frame_list[i])

    # close the writer
    writer.release()
