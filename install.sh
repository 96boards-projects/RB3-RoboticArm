# KEEP UBUNTU OR DEBIAN UP TO DATE

sudo apt -y update
sudo apt -y upgrade
sudo apt -y dist-upgrade
sudo apt -y autoremove


# INSTALL THE DEPENDENCIES

# Build tools:
sudo apt install -y build-essential cmake qt5-default libvtk6-dev libqt5opengl5-dev python3-pyqt5.qtopengl python3-opengl zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libopenexr-dev libgdal-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev libxine2-dev libtbb-dev libeigen3-dev libatlas-base-dev libclblas-dev libgstreamer1.0-0 libgstreamer-plugins-*-dev vtk6 python-vtk6 python3-pip python3-dev python3-tk python3-numpy python3-scipy python3-pyaudio ant default-jdk doxygen unzip wget python2-pip python2-dev python2-tk python2-numpy python2-scipy python2-pyaudio xterm


# Python:
pip3 install wheel
pip2 install wheel

# INSTALL THE LIBRARY (YOU CAN CHANGE '3.2.0' FOR THE LAST STABLE VERSION)

cd ~
wget -O opencv.zip https://github.com/ric96/opencv-aarch64/archive/3.2.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.2.0.zip
unzip opencv_contrib.zip

cd opencv-aarch64-3.2.0
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE -DBUILD_SHARED_LIBS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_opencv_apps=OFF -DBUILD_DOCS=OFF -DBUILD_PERF_TESTS=OFF -DBUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=/usr/local -DENABLE_PRECOMPILED_HEADERS=OFF -DWITH_LIBV4L=ON -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=OFF -DWITH_GDAL=ON -DWITH_XINE=ON -DWITH_OPENMP=ON -DWITH_GSTREAMER=ON -DWITH_OPENCL=ON -DWITH_LIBV4L=OFF -DWITH_V4L=ON -DWITH_DSHOW=ON -DOPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.2.0/modules ../

make -j 8
sudo make install
sudo ldconfig

#install the imutils (which depend on the OpenCV just built)
sudo -H pip3 install setuptools --upgrade
pip3 install imtools imutils adafruit-pca9685 SoundRecognition pymemcache collections-extended difflib
pip2 install imtools imutils adafruit-pca9685 SoundRecognition pymemcache collections-extended difflib

# EXECUTE SOME OPENCV EXAMPLES AND COMPILE A DEMONSTRATION

# To complete this step, please visit 'http://milq.github.io/install-opencv-ubuntu-debian'.

