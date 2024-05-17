import cv2
import os

def fill_to_length(string: str, length: int, ch: str = "0") -> str:
    if len(string) > length:
        raise RuntimeError("length of `string` shouldn't be greater than `length`")
    return ch*(length-len(string))+string

def split_img(path: str, 
              subwidth: int = 64, 
              subheight: int = 64, 
              output_folder: str = "./", 
              num_start: int = 0, 
              num_length: int = 2, 
              except_pos: list[tuple[int, int]] = []) -> None:
    """
    use height*width = 3*4 as the example, output order is (assume `num_start = 0`):\\
    0 1  2  3 \\
    4 5  6  7 \\
    8 9 10 11 \\
    every size must be divisible
    """
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    basename = path.split(".")[-1]
    height, width, channels = image.shape
    count = num_start
    for i in range(height // subheight):
        for j in range(width // subwidth):
            if (i, j) in except_pos:
                continue
            cropped_image = image[i*subheight:(i+1)*subheight, j*subwidth:(j+1)*subwidth]
            print(count)
            cv2.imwrite(os.path.join(output_folder, 
                                     fill_to_length(str(count), num_length) + "." + basename), 
                        cropped_image)
            count += 1

def crop_img(path, top_left, height, width, output_folder = "./", output_filename = "0"):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    basename = path.split(".")[-1]
    cropped_image = image[top_left[1]:(top_left[1]+height), top_left[0]:(top_left[0]+width)]
    cv2.imwrite(os.path.join(output_folder, output_filename + "." + basename), cropped_image)


output_folder = r"D:\Projects\Python\pygame\pygame-rpg-2\Dev\Graphics\objects"
file_path = r"D:\Projects\Python\pygame\pygame-rpg-2\Dev\Graphics\edit\Graphics-old\maptile\outside04_resized.png"
# split_img(file_path, subwidth=32, subheight=32, num_length=3, output_folder=output_folder)
crop_img(file_path, (448, 0), 128, 64, output_folder=output_folder, output_filename="46")
