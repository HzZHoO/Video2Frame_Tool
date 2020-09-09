import os
import shutil
import cv2


def video2frames(input_path, output_path):
    verbose = True  # print more info

    if not os.path.exists(input_path):
        print("Input video file '{}' is not found".format(input_path))
        return 1

    if os.path.exists(output_path):
        if verbose:
            print("Remove existing output folder '{}'".format(output_path))
        shutil.rmtree(output_path)

    os.makedirs(output_path)

    cap = cv2.VideoCapture()
    cap.open(input_path)
    if not cap.isOpened():
        print("Failed to open input video")
        return 1

    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if verbose:
        print("This video '{name}' have {num} frames".format(num=frameCount, name=input_path))

    frameId = 0  # initial frame ID
    while frameId < frameCount:
        ret, frame = cap.read()  # get one frame from the video
        if not ret:
            print("Failed to get the frame {f}".format(f=frameId))
            continue

        fname = "{:06d}.png".format(frameId)  # name of one frame
        ofname = os.path.join(output_path, fname)  # save path of one frame
        ret = cv2.imwrite(ofname, frame)  # save one frame
        if not ret:
            print("Failed to write the frame {f}".format(f=frameId))
            continue

        frameId += 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameId)

    return 0


if __name__ == "__main__":

    print("Start Video2Frames script ...")
    ret = video2frames(r"C:\OpenCV\6.mp4", r"C:\OpenCV\6")
    exit(ret)
