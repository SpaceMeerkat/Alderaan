from torch.utils import data as data
from torchvision import transforms
import os
from astropy.io import fits
from skimage.transform import resize

IMG_EXTENSIONS = [
    ".fits"
]


def is_image_file(filename):
    """
    Helper Function to determine whether a file is an image file or not
    :param filename: the filename containing a possible image
    :return: True if file is image file, False otherwise
    """
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def make_dataset(dir):
    """
    Helper Function to make a dataset containing all images in a certain directory
    :param dir: the directory containing the dataset
    :return: images: list of image paths
    """
    images = []
    assert os.path.isdir(dir), '%s is not a valid directory' % dir

    for root, _, fnames in sorted(os.walk(dir)):
        for fname in fnames:
            if is_image_file(fname):
                path = os.path.join(root, fname)
                images.append(path)

    return images


def default_fits_loader(file_name: str, img_size: tuple, slice_index):
    file = fits.open(file_name)
    _data = file[1].data
    _data = resize(_data[slice_index], img_size)

    # _data = fits.get_data(file_name).resize(img_size)

    # add channels
    if len(_data.shape) < 3:
        _data = _data.reshape((*_data.shape, 1))
    # TODO: Extract Label from Cube (there is no attribute file[0].header["label"])
    _label = _data

    return _data, _label


class FITSCubeDataset(data.Dataset):
    def __init__(self, data_path, cube_length, transforms, img_size):
        self.data_path = data_path
        self.transforms = transforms
        self.img_size = img_size
        self.cube_length = cube_length

        self.img_files = make_dataset(data_path)

    def __getitem__(self, index):
        cube_index = index // self.cube_length
        slice_index = index % self.cube_length
        _img, _label = default_fits_loader(self.img_files[cube_index], self.img_size, slice_index)
        if self.transforms is not None:
            _data = (self.transforms(_img), _label)

        else:
            _data = (_img, _label)

        return _data

    def __len__(self):
        return len(self.img_files)*self.cube_length


if __name__ == '__main__':
    CUBE_LENGTH = 640
    dataset = FITSCubeDataset("PATH_TO_DATA_DIR", transforms.ToTensor(), (64, 64), CUBE_LENGTH)
    data_loader = data.DataLoader(dataset, batch_size=1)

    last_data, last_label = None, None
    for idx, tmp in enumerate(data_loader):
        print(idx)
        _last_data, last_label = tmp[0], tmp[1]